import logging
import os
import sys, urllib
import msgpack
import socket
import time
import threading

class TreasureDataLogRecordFormatter:
    def __init__(self):
        self.hostname = socket.gethostname()

    def format(self, record):
        data = {
          'sys_host' : self.hostname,
          'sys_name' : record.name,
          'sys_module' : record.module,
          'sys_lineno' : record.lineno,
          'sys_levelno' : record.levelno,
          'sys_levelname' : record.levelname,
          'sys_filename' : record.filename,
          'sys_funcname' : record.funcName,
          'sys_exc_info' : record.exc_info,
          'msg' : record.msg,
        }
        if 'sys_exc_info' in data and data['sys_exc_info']:
            data['sys_exc_info'] = self.formatException(data['sys_exc_info'])
        return data

class TreasureDataHandler(logging.Handler):
    '''
    Logging Handler for td-agent.
    '''
    def __init__(self,
           host='127.0.0.1',
           port=24224,
           db='log',
           table='default',
           bufmax=1*1024*1024,
           verbose=False):

        self.host = host
        self.port = port
        self.db = db
        self.table = table
        self.bufmax = bufmax
        self.verbose = verbose

        self.pendings = None
        self.packer = msgpack.Packer()
        self.fmt = TreasureDataLogRecordFormatter()
        self.lock = threading.Lock()
        try:
            self.socket = self._connect()
        except:
            # will be retried in emit()
            self.socket = None

        logging.Handler.__init__(self)

    def __del__(self):
        self._close()

    def emit(self, record):
        if record.levelno < self.level: return
        bytes = self._make_packet(self.fmt.format(record))
        self._send(bytes)

    def _reconnect(self):
        if not self.socket:
            self.socket = self._connect()

    def _connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        sock.connect((self.host, self.port))
        return sock

    def _close(self):
        if self.socket:
            self.socket.close()
        self.socket = None

    def _make_packet(self, data):
        tag = "td.%s.%s" % (self.db, self.table)
        packet = [ tag, long(time.time()), data ]
        if self.verbose:
            print packet
        return self.packer.pack(packet)

    def _send(self, bytes):
        self.lock.acquire()
        try:
            self._send_internal(bytes)
        finally:
            self.lock.release()

    def _send_internal(self, bytes):
        # buffering
        if self.pendings:
            self.pendings += bytes
            bytes = self.pendings

        try:
            # reconnect if possible
            self._reconnect()

            # send message
            total = len(bytes)
            nsent = 0
            while nsent < total:
                n = self.socket.send(bytes[nsent:])
                if n <= 0:
                    raise RuntimeError("socket connection broken")
                nsent += n

            # send finished
            self.pendings = None
        except:
            # close socket
            self._close()
            # clear buffer if it exceeds max bufer size
            if self.pendings and (len(self.pendings) > self.bufmax):
                self.pendings = None
            else:
                self.pendings = bytes

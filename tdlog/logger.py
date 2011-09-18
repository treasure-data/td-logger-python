import logging
import os
import sys, urllib
import msgpack
import socket
import time

class TreasureDataLogRecordFormatter:
    def __init__(self):
        self.hostname = socket.gethostname()

    def format(self, record):
        data = {
          'host' : self.hostname,
          'name' : record.name,
          'module' : record.module,
          'lineno' : record.lineno,
          'levelno' : record.levelno,
          'levelname' : record.levelname,
          'filename' : record.filename,
          'funcname' : record.funcName,
          'exc_info' : record.exc_info,
        }
        if 'exc_info' in data and data['exc_info']:
            data['exc_info'] = self.formatException(data['exc_info'])
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

        # packet for td-agent TCP input channel
        packet = self._make_packet(self.fmt.format(record))
        if self.verbose:
            print packet
        data = self.packer.pack(packet)

        # buffering
        if self.pendings:
            self.pendings.append(data)
            data = self.pendings

        try:
            # reconnect if possible
            self._reconnect()

            # send message
            total = len(data)
            nsent = 0
            while nsent < total:
                n = self.socket.send(data[nsent:])
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
                self.pendings = data

    def _reconnect(self):
        if not self.socket:
            self._connect()

    def _connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        return sock

    def _close(self):
        if self.socket:
            self.socket.close()
        self.socket = None

    def _make_packet(self, data):
        tag = "td.%s.%s" % (self.db, self.table)
        packet = [ tag, long(time.time()), data ]
        return packet

import logging
import os
import sys, urllib
import msgpack
import socket
import time

class TreasureDataHandler(logging.Handler):
    '''
    Logging Handler for td-agent.
    '''
    def __init__(self,
           host='127.0.0.1',
           port=24224,
           db='logging',
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

        data = self._format_record(record)
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
            # clear buffer if it exceeds max bufer size
            if self.pendings and (len(self.pendings) > self.bufmax):
                self.pendings = None
            # close socket
            self._close()

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

    def _format_record(self, record):
        data = record._raw.copy()
        if 'exc_info' in data and data['exc_info']:
            data['exc_info'] = self.formatException(data['exc_info'])
        tag = "td.%s.%s" % (self.db, self.table)

        packet = [ tag, long(time.time()), data ]
        if self.verbose:
            print packet

        return self.packer.pack(packet)

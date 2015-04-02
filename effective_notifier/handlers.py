# -*- coding:utf-8 -*-
import struct
import json

from effective_notifier.connection import EffectiveConnection
from effective_notifier.exceptions import EffectiveError, PacketParseError, InvalidProtocolError, InvalidEventError
from effective_notifier.managers import ProtocolManager


class EffectiveConnectionHandler(object):

    def __init__(self, socket, address_set):
        self.protocol_manager = ProtocolManager.instance()
        self.connection = EffectiveConnection(socket, address_set)
        self.send(json.dumps(dict(a=1)))
        self.handle()

    def handle(self):
        from gevent import socket

        while True:
            raw_data = self._read(4)
            if not raw_data:
                self.connection.socket.shutdown(socket.SHUT_WR)
                self.connection.socket.close()
                break
            length = struct.unpack('>I', raw_data)[0]
            data = self._read(length)
            try:
                data = json.loads(data)
            except ValueError, e:
                raise PacketParseError(e.message)
            except TypeError, e:
                self.connection.socket.shutdown(socket.SHUT_WR)
                self.connection.socket.close()
                break
            try:
                self.on_data(data)
            except EffectiveError, e:
                self._error_response(e)

    def send(self, data):
        if isinstance(data, dict):
            data = json.dumps(data)
        data = (struct.pack('>I', len(data)) + data)
        self.connection.socket.send(data)

    def on_data(self, data):
        self.connection.update()

        protocol_name = data.get('protocol', '')
        try:
            protocol_class = self.protocol_manager.protocols[protocol_name]
        except KeyError:
            message = "'%s' protocol doesn't exits." % protocol_name
            raise InvalidProtocolError(message=message)
        try:
            protocol_handler = protocol_class(self)
        except TypeError:
            # TODO handler instance create error
            pass

        event_name = data.get('event', '')
        func_name = 'on_%s' % event_name
        if hasattr(protocol_handler, func_name):
            func = getattr(protocol_handler, func_name)
            func(data)
        else:
            message = "'%s' event doesn't exits." % event_name
            raise InvalidEventError(message=message)

    def _read(self, length):
        data = ''
        while len(data) < length:
            packet = self.connection.socket.recv(length - len(data))
            if not packet:
                return None
            data += packet
        return data

    def _error_response(self, error):
        data = dict(status=dict(code=error.code, message=error.message))
        self.send(data)


class EffectiveBaseProtocolHandler(object):

    def __init__(self, connection_handler):
        self.connection_handler = connection_handler
# -*- coding:utf-8 -*-
from effective_notifier.server import EffectiveServer
from effective_notifier.handlers import EffectiveConnectionHandler as ConnectionHandler, \
    EffectiveBaseProtocolHandler


class PingPongHandler(EffectiveBaseProtocolHandler):

    def on_ping(self, data):
        print 'on ping'

protocols = {
    'ping-pong': PingPongHandler
}

EffectiveServer.run(protocol_dict=protocols)
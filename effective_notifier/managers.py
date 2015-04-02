# -*- coding:utf-8 -*-
from effective_notifier.decorators import Singleton


@Singleton
class ProtocolManager(object):
    protocols = {}

    def add_protocol(self, name, handler_class):
        self.protocols[name] = handler_class

    def add_protocols_from_dict(self, handler_dict):
        self.protocols.update(handler_dict)
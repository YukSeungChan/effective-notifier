# -*- coding:utf-8 -*-
class EffectiveError(Exception):

    def __init__(self, code=None, message=''):
        code = self.__class__.__name__ if not code else code
        super(EffectiveError, self).__init__(message)
        self.code = code


class PacketParseError(EffectiveError):
    pass


class InvalidProtocolError(EffectiveError):
    pass


class InvalidEventError(EffectiveError):
    pass


class ProtocolParseError(EffectiveError):
    pass

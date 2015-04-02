# -*- coding:utf-8 -*-
from gevent.server import StreamServer

from effective_notifier.managers import ProtocolManager
from effective_notifier.handlers import EffectiveConnectionHandler


class EffectiveServer(StreamServer):

    def __init__(self, *args, **kwargs):
        super(EffectiveServer, self).__init__(*args, **kwargs)
        self.protocol_manager = ProtocolManager.instance()


    @classmethod
    def run(cls, host='0.0.0.0', port=1234, protocol_dict={}):
        # TODO logging, configuration, redis, aws(sqs, sns)...
        server = cls((host, port), EffectiveConnectionHandler)
        server.protocol_manager.add_protocols_from_dict(protocol_dict)
        print 'Effective-Notifier started on %s:%i...' % (host, port)
        server.serve_forever()
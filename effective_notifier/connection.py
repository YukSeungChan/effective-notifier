# -*- coding:utf-8 -*-
import uuid

from datetime import datetime


class EffectiveConnection(object):

    def __init__(self, socket, address_set):
        self.id = str(uuid.uuid4()).replace('-', '')
        self.socket = socket
        self.ip = address_set[0]
        self.port = address_set[1]
        self.created_at = datetime.now()
        self.updated_at = None

    def update(self):
        self.updated_at = datetime.now()
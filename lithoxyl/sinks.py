# -*- coding: utf-8 -*-

import sys
import json


class AggSink(object):
    "A 'dummy' sink that just aggregates the messages."
    def __init__(self):
        self.messages = []

    def handle_start(self, message):
        pass

    def handle(self, message):
        self.messages.append(message)


_MSG_ATTRS = ('name', 'level', 'status', 'message',
              'start_time', 'end_time', 'duration')


class StructuredFileSink(object):
    def __init__(self, fileobj=None):
        self.fileobj = fileobj or sys.stdout

    def handle(self, message):
        msg_data = dict(message.data)
        for attr in _MSG_ATTRS:
            msg_data[attr] = getattr(message, attr, None)
        json_str = json.dumps(msg_data, sort_keys=True)
        self.fileobj.write(json_str)
        self.fileobj.write('\n')

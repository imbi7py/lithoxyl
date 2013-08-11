# -*- coding: utf-8 -*-

import os
import sys

# TODO: should separators (i.e., newline) be handled here or in the Formatter?


class StreamEmitter(object):
    def __init__(self, stream=None, errors=None, newline=os.linesep):
        if stream is None:
            stream = sys.stderr
        elif stream == 'stdout':
            stream = sys.stdout
        elif stream == 'stderr':
            stream = sys.stderr
        self.stream = stream
        self.encoding = getattr(stream, 'encoding', None) or 'UTF-8'
        self.errors = errors or 'backslashreplace'
        # TODO: try values for encoding and errors out (otherwise
        # problems can get detected way too late)
        self.newline = newline

    def emit_entry(self, entry):
        if isinstance(entry, unicode):
            entry = entry.encode(self.encoding, self.errors)
        try:
            self.stream.write(entry)
            if self.newline:
                self.stream.write(self.newline)
        except:
            # TODO: something maybe
            # TODO: built-in logging raises KeyboardInterrupts and
            # SystemExits, special handling for everything else.
            raise

    __call__ = emit_entry


class FileEmitter(object):
    def __init__(self, filepath, encoding=None):
        self.filepath = os.path.abspath(filepath)
        self.mode = 'a'
        self.encoding = encoding or 'UTF-8'  # TODO: check encoding?

    def emit_entry(self, entry):
        pass

import functools
from threading import Lock

import gtk


class repeat(object):
    def __init__(self, f):
        self.f = f
        self.id = None
        self.lock = Lock()

    def __call__(self, cls):
        self.f(cls)

    def start(self, cls, frequency):
        self.lock.acquire()
        if not self.id:
            @functools.wraps(self.f)
            def run():
                self.f(cls)
                return True
            self.id = gtk.timeout_add(frequency, run)
        self.lock.release()

    def stop(self):
        self.lock.acquire()
        if self.id:
            gtk.timeout_remove(self.id)
            self.id = None
        self.lock.release()


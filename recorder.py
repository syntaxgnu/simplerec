''' Recorder thread '''
import logging
import subprocess
import threading

class Recorder():
    def __init__(self, address, duration):
        ''' Constructor '''
        self.logging = logging.getLogger('Scheduler')
        self.logging.setLevel(level=logging.DEBUG)
        self.address = address
        self.duration = duration

    def start_recording():
        ''' Function that starts the recording '''

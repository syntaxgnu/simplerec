''' Recorder thread '''
import logging
import subprocess
import threading
import time

class Recorder(threading.Thread):
    def __init__(self, address, duration, filename):
        ''' Constructor '''
        self.process = None
        threading.Thread.__init__(self)
        self.logging = logging.getLogger('Recorder')
        self.logging.setLevel(level=logging.DEBUG)
        self.address = address
        self.duration = duration
        self.filename = filename

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        ''' Handle cleanup of recorder '''
        if self.process is not None:
            self.process.terminate()

    def run(self):
        ''' Function that starts the recording '''
        self.logging.debug('Starting recording')
        self.process = subprocess.Popen(['ffmpeg', '-i', self.address,
        '-sn', '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '20', self.filename])
        waittime = 60 * float(self.duration)
        self.logging.debug('Recording started, waiting for(seconds): ' + str(waittime))
        time.sleep(waittime)
        self.logging.debug('Recording finished')
        self.process.terminate()
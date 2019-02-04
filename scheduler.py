'''
Schedule VLC recording for later
'''
import logging

from apscheduler.schedulers.background import BackgroundScheduler

class Scheduler():
    ''' Class that schedules, starts recording and
        cleans up process after recording is done '''
    def __init__(self, address, datetime, duration):
        ''' Constructor '''
        self.process = None
        self.logging = logging.getLogger('Scheduler')
        self.logging.setLevel(level=logging.DEBUG)
        self.address = address
        self.datetime = datetime
        self.duration = duration

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        ''' Handle cleanup of recorder '''
        if self.process is not None:
            self.process.terminate()

    def record(self):
        ''' Function to start the recording '''
        self.logging.debug('Starting recording')
        self.process = subprocess.Popen(['vlc', '--no-macosx-mediakeys', self.address,
        '--sout="#duplicate{dst=std{access=file,mux=ts,dst=test.ts},dst=nodisplay}"',
        '--sout-keep'])
        self.process.wait(timeout=self.duration)
        self.logging.debug('Recording finished')

    def recorder_thread(self):


    def start_recorder(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.recorder_thread, seconds=self.waittime)
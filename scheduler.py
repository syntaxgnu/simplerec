'''
Schedule VLC recording for later
'''
import logging
import time
from apscheduler.schedulers.background import BackgroundScheduler

import recorder

class Scheduler():
    ''' Class that schedules, starts recording and
        cleans up process after recording is done '''
    def __init__(self, address, rundate, duration):
        ''' Constructor '''
        self.logging = logging.getLogger('Scheduler')
        self.logging.setLevel(level=logging.DEBUG)
        self.address = address
        self.rundate = rundate
        self.duration = duration
        self.recording_started = False

    def start_recorder_thread(self):
        ''' Method that spawn and join the recorder thread '''
        filename = str(self.rundate)
        rec_thread = recorder.Recorder(self.address, self.duration, filename)
        rec_thread.start()
        self.recording_started = True
        rec_thread.join()


    def start_recorder(self):
        ''' Schedule the recorder thread for later '''
        scheduler = BackgroundScheduler()
        self.logging.debug('Scheduling recording at %s', str(self.rundate))
        scheduler.add_job(self.start_recorder_thread, 'date', run_date=self.rundate)
        scheduler.start()
        while self.recording_started is False:
            self.logging.debug('Waiting for scheduler')
            time.sleep(60)

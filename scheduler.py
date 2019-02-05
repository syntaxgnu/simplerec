'''
Schedule VLC recording for later
'''
import logging
import recorder
import time

from apscheduler.schedulers.background import BackgroundScheduler

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

    def _start_recorder_thread(self):
        rec_thread = recorder.Recorder(self.address, self.duration)
        rec_thread.start()
        self.recording_started = True
        rec_thread.join()


    def start_recorder(self):
        scheduler = BackgroundScheduler()
        self.logging.debug('Scheduling recording at ' + str(self.rundate) + ' seconds')
        scheduler.add_job(self._start_recorder_thread, 'date', run_date=self.rundate)
        scheduler.start()
        while self.recording_started == False:
            self.logging.debug('Waiting for scheduler')
            time.sleep(60)
''' Recorder thread '''
import glob
import logging
import os
import subprocess
import threading
import time

class Recorder(threading.Thread):
    ''' The recorder class dumps and reencodes a given video stream '''
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
        # Dump stream
        mkv_filename = self.filename + '.mkv'
        mp4_filename = self.filename + '.mp4'
        self.process = subprocess.Popen(['ffmpeg', '-i', self.address,
                                         '-map', '0', '-sn', '-c:v',
                                         'libx264', '-c:a', 'copy',
                                         mkv_filename])
        waittime = 60 * float(self.duration)
        self.logging.debug('Recording started, waiting for %d seconds', waittime)
        time.sleep(waittime)
        self.logging.debug('Recording finished')
        self.process.terminate()
        self.process.wait()

        # Reencode the dumped stream in two passes
        self.logging.debug('Starting reencoding pass 1')
        reencoding_pass_one = subprocess.Popen(['ffmpeg', '-y', '-i', mkv_filename,
                                                '-c:v', 'libx264', '-b:v',
                                                '2600k', '-pass', '1', '-an',
                                                '-f', 'mp4', '/dev/null'])
        reencoding_pass_one.wait()

        self.logging.debug('Starting reencoding pass 2')
        reencoding_pass_two = subprocess.Popen(['ffmpeg', '-i', mkv_filename,
                                                '-c:v', 'libx264', '-b:v',
                                                '2600k', '-pass', '2',
                                                '-c:a', 'aac',
                                                '-b:a', '128k', mp4_filename])
        reencoding_pass_two.wait()

        # Delete log files and the dumped stream since we now have an encoded mp4 file
        self.logging.debug('Deleting log files and the dumped video stream')
        files_to_delete = glob.glob('ffmpeg2pass*')
        files_to_delete += glob.glob(mkv_filename)
        for file_to_delete in files_to_delete:
            os.remove(file_to_delete)

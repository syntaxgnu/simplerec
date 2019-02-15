''' Main script to execute for the recorder CLI '''
from datetime import datetime
from pprint import pprint
from pathlib import Path
from PyInquirer import prompt
import glob
import logging

import m3uparser
import scheduler

class RecApp():
    ''' The recorder app that parses m3u and sets up recording '''
    def __init__(self, file_name):
        self.m_parser = m3uparser.M3uParser(file_name)

    def get_group_choices(self):
        ''' Get all choices for channel groups '''
        choices = []
        for group in self.m_parser.get_groups():
            choices.append({'name': group})

        return choices

    def get_channel_choices(self, group):
        ''' Get all choices for channels in given group '''
        choices = []
        for choice in self.m_parser.get_channels_from_group(group):
            choices.append({'name': choice})

        return choices

    def get_group(self):
        ''' Show all groups and get the user choice '''
        questions = [
            {
                'type': 'list',
                'message': 'Choose group',
                'name': 'group',
                'choices' : self.get_group_choices()
            }
        ]

        answers = prompt(questions)
        pprint(answers)
        country = answers['group']
        return country

    def get_channel(self, group):
        ''' Show channels from group and get user choice '''
        questions = [
            {
                'type': 'list',
                'message': 'Choose channel',
                'name': 'channel',
                'choices' : self.get_channel_choices(group)
            }
        ]

        answers = prompt(questions)
        pprint(answers)
        channel = answers['channel']
        return channel

    def get_address_from_channel(self, channel):
        ''' Get the stream address '''
        return self.m_parser.get_address_from_channel(channel)

def get_time_and_duration():
    ''' Get time and duration for recording '''
    questions = [
        {
            'type' : 'input',
            'name' : 'datetime',
            'message' : 'Datetime to start recording: ',
            'default' : datetime.now().strftime('%Y-%m-%d %H:%M')
        },
        {
            'type' : 'input',
            'name' : 'duration',
            'message' : 'Duration of recording(mins): '
        }
    ]
    answers = prompt(questions)
    scheduled_datetime = datetime.strptime(answers['datetime'], '%Y-%m-%d %H:%M')
    duration = answers['duration']
    return scheduled_datetime, duration

def locate_m3u_files():
    ''' This function returns a list of the m3u files
        found in working directory and users home directory '''
    m3u_files = glob.glob('*.m3u')
    m3u_files += glob.glob(str(Path.home()) + '/*.m3u')
    return m3u_files

def get_m3u_file():
    ''' Get the m3u file to use '''
    m3u_file = None
    m3u_files = locate_m3u_files()
    if len(m3u_files) > 0:
        questions = [
            {
                'type': 'list',
                'message': 'Choose m3u file',
                'name': 'file',
                'choices' : m3u_files
            }
        ]

        answers = prompt(questions)
        m3u_file = answers['file']
    return m3u_file

def main():
    ''' The main function that runs the show '''
    m3u_file = get_m3u_file()
    if m3u_file is None:
        logging.error('No m3u file found. Please copy an m3u file to working directory or home directory')
    else:
        rec_app = RecApp(m3u_file)
        group_to_record = rec_app.get_group()
        channel_to_record = rec_app.get_channel(group_to_record)
        address_to_record = rec_app.get_address_from_channel(channel_to_record)
        record_rundate, record_duration = get_time_and_duration()
        rec_scheduler = scheduler.Scheduler(address_to_record, record_rundate, record_duration)
        rec_scheduler.start_recorder()

if __name__ == '__main__':
    main()

''' Main script to execute for the recorder CLI '''
from datetime import datetime
from pprint import pprint

from PyInquirer import prompt

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

def main():
    ''' The main function that runs the show '''
    rec_app = RecApp('mega.m3u')
    group_to_record = rec_app.get_group()
    channel_to_record = rec_app.get_channel(group_to_record)
    address_to_record = rec_app.get_address_from_channel(channel_to_record)
    record_rundate, record_duration = get_time_and_duration()
    rec_scheduler = scheduler.Scheduler(address_to_record, record_rundate, record_duration)
    rec_scheduler.start_recorder()

if __name__ == '__main__':
    main()

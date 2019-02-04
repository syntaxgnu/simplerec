from PyInquirer import prompt, print_json
from pprint import pprint

import m3uparser


class RecApp():
    def __init__(self, file_name):
        self.m_parser = m3uparser.m3uParser(file_name)

    def get_group_choices(self):
        ''' Get all choices for channel groups '''
        choices = []
        for group in self.m_parser.get_groups():
            choices.append({'name': group})

        return choices

    def get_channel_choices(self, group):
        ''' Get all choices for channels in given group '''
        choices = []
        for group in self.m_parser.get_channels_from_group(group):
            choices.append({'name': group})

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

    def get_time_and_duration(self):
        ''' Get time and duration for recording '''
        questions = [
            {
                'type' : 'input',
                'name' : 'datetime',
                'message' : 'Datetime to start recording: '
            },
            {
                'type' : 'input',
                'name' : 'duration',
                'message' : 'Duration of recording(mins): '
            }
        ]
        answers = prompt(questions)
        datetime = answers['datetime']
        duration = answers['duration']
        return datetime, duration

if __name__ == '__main__':
    rec_app = RecApp('mega.m3u')
    group = rec_app.get_group()
    channel = rec_app.get_channel(group)
    address = rec_app.get_address_from_channel(channel)
    datetime, duration = rec_app.get_time_and_duration()

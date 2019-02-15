''' Simple parser for m3u playlists '''
import logging
from collections import defaultdict


class M3uParser():
    ''' Class that parses an m3u playlist and stores it in a key value dict '''
    def __init__(self, filename):
        ''' Constructor '''
        logging.getLogger('m3uparser')
        logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')
        self.sources = None
        self.parse_m3u(filename)

    def get_groups(self):
        ''' Get the groups from m3u '''
        groups = []
        for key in self.sources:
            groups.append(key)

        return groups

    def get_channels_from_group(self, group):
        ''' Return channels from given group '''
        channels = []
        if group in self.sources:
            for channel_to_add, _ in self.sources[group]:
                channels.append(channel_to_add)
        return channels

    def get_address_from_channel(self, channel):
        ''' Return address from given channel '''
        address = ''
        for group in self.sources:
            for channel_from_group, addr in self.sources[group]:
                if channel_from_group == channel:
                    address = addr
        return address

    def parse_m3u(self, filename):
        ''' parse the m3u playlist and return as dict '''
        parsed_sources = defaultdict(list)
        with open(filename) as m3u_file:
            all_data = m3u_file.read()
            # Separate entries by splitting on EXTINF and skipping first line
            sources = all_data.split('#EXTINF')
            for source in sources[1:]:
                group = ""
                channel = ""
                channel_found = False
                address = ""
                lines = source.split('\n')
                #First line is metadata, get group from it
                for data in lines[0].split(' '):
                    if 'group-title' in data:
                        group = data.split('"')[1]
                        logging.debug('group: %s', str(group))
                    elif 'tvg-name' in data:
                        channel_found = True
                        channel = data.split('"')[1] + ' '
                    elif channel_found:
                        if '"' in data:
                            channel = channel + data.split('"')[0]
                            channel_found = False
                        else:
                            channel = channel + data + ' '

                # Second line contains only the address
                logging.debug('Channel: %s', str(channel))
                logging.debug('Address: %s', str(lines[1]))
                address = lines[1]
                if group in parsed_sources:
                    parsed_sources[group].append((channel, address))
                else:
                    parsed_sources[group] = [(channel, address)]

        logging.info('Parsed %s groups', str(len(parsed_sources)))
        self.sources = parsed_sources

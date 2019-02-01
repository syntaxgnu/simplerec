''' Simple parser for m3u playlists '''
import logging
from collections import defaultdict


class m3uParser():
    ''' Class that parses an m3u playlist and stores it in a key value dict '''
    def __init__(self, filename):
        ''' Constructor '''
        logging.getLogger('m3uparser')
        logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')
        self.sources = self.parse_m3u(filename)

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
            for ch,_ in self.sources[group]:
                channels.append(ch)
        return channels

    def get_address_from_channel(self, channel):
        ''' Return address from given channel '''
        address = ''
        for group in self.sources:
            for ch, addr in self.sources[group]:
                if ch == channel:
                    address = addr
        return address

    def parse_m3u(self, filename):
        ''' parse the m3u playlist and return as dict '''
        parsed_sources = defaultdict(list)
        with open(filename) as f:
            all_data = f.read()
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
                        logging.debug('group:  ' + str(group))
                    elif 'tvg-name' in data:
                        channel_found = True
                        channel = data.split('"')[1] + ' '
                        logging.debug('not group: ' + str(data))
                    elif channel_found == True:
                        if '"' in data:
                            channel = channel + data.split('"')[0]
                            channel_found = False
                        else:
                            channel = channel + data + ' '

                # Second line contains only the address
                logging.debug('Channel: ' + str(channel))
                logging.debug('Address: ' + str(lines[1]))
                address = lines[1]
                if group in parsed_sources:
                    parsed_sources[group].append((channel, address))
                else:
                    parsed_sources[group] = [(channel, address)]

        logging.info('Parsed ' + str(len(parsed_sources)) + ' groups')
        return parsed_sources
if __name__ == "__main__":
    mp = m3uParser('swero.m3u')
    groups = mp.get_groups()
    for group in groups:
        ch = mp.get_channels_from_group(group)
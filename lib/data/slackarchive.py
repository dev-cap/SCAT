import requests
import json
import os
from config import *


class DataLogsLoader(object):

    def __init__(self, domain):
        """
        This method initialises the domain and origin_header variable for the rest of methods to use.
        :param self
        :param domain: It is the domain name of the team of which the logs have to be downloaded.
        """
        self.domain = domain
        self.origin_header = {"referer": ORIGIN_HEADER_LINK % self.domain}

    def fetch_team(self):
        """
        This method uses the SlackArchive API endpoint to fetch the metadata of the team that belongs to a domain.
        :param self
        :return: A dict containing the metadata of the team that belongs to the domain passed as the parameter.
        """
        url = TEAM_API % self.domain
        session = requests.Session()
        teams = session.get(url, headers=self.origin_header)
        return json.loads(teams.content.decode('utf-8'))['team'][0]

    def fetch_channels(self, team_id):
        """
        This method uses the SlackArchive API endpoint to fetch all the channels that are in a team along
        with the relevant channel metadata.
        :param self
        :param team_id: The unique team identifier as returned by the fetch_team method.
        :return: A dict containing all the channels that are in the team identified by team_id, along with
        relevant channel metadata.
        """
        url = CHANNEL_API % team_id
        session = requests.Session()
        channels = session.get(url, headers=self.origin_header)
        return json.loads(channels.content.decode('utf-8'))['channels']

    def fetch_messages(self, team_id, channel_id, offset):
        """
        This method returns a list of messages from a channel according to the range specified by the size
        and offset parameters.
        :param self
        :param team_id: The unique team identifier as returned by the fetch_team method.
        :param channel_id: The unique channel identifier as returned by the fetch_channel method.
        :param offset: The number of messages to skip while fetching, in a reverse-chronological order. An
        offset of 5 with a size of 100 will fetch the 100 messages after the 5 latest messages in a channel.
        :return: A dict containing a list of messages from the specified channel, in a reverse-chronological
        order, according to the range specified by the size and offset parameters.
        """
        size = SIZE
        url = MESSAGES_API % (size, team_id, channel_id, offset)
        session = requests.Session()
        messages = session.get(url, headers=self.origin_header)
        return json.loads(messages.content.decode('utf-8'))['messages']

    def fetch_users(self, team_id, channel_id, offset):
        """
        This method returns a list of users from a channel according to the range specified by the size
        and offset parameters.
        :param self
        :param team_id: The unique team identifier as returned by the fetch_team method.
        :param channel_id: The unique channel identifier as returned by the fetch_channel method.
        :param offset: The number of messages to skip while fetching, in a reverse-chronological order. An
        offset of 5 with a size of 100 will fetch the 100 messages after the 5 latest messages in a channel.
        :return: A dict containing a list of messages from the specified channel, in a reverse-chronological
        order, according to the range specified by the size and offset parameters.
        """
        size = SIZE
        url = MESSAGES_API % (size, team_id, channel_id, offset)
        session = requests.Session()
        messages = session.get(url, headers=self.origin_header)
        return json.loads(messages.content.decode('utf-8'))['related']['users']


class DataToJson(object):

    def __init__(self, team_name):
        """
        This method initialises the team_name variable and instantiates an object of
        DataLogsLoader() class.
        :param self
        :param team_name: It is the team name of which the data logs have to downloaded.
        """
        self.team_name = team_name
        self.data_loader = DataLogsLoader(self.team_name)

    def team_to_json(self):
        """
        This method writes the team data logs into a file data/team-name/team.json
        :param self
        """
        self.team_data = self.data_loader.fetch_team()
        write_to_json(DESTINATION_FOLDER + '%s/'  % self.team_name, 'team.json', self.team_data)

    def channels_to_json(self):
        """
        This method writes the channels data log of the given team to data/team-name/channels.json
        :param self
        """
        self.channels_data = self.data_loader.fetch_channels(self.team_data['team_id'])
        write_to_json(DESTINATION_FOLDER + '%s/' % self.team_name, 'channels.json', self.channels_data)

    def messages_to_json(self):
        """
        This method writes the messages data logs of each channel of the team in json files.
        These files are kept in data/team-name/messages/channel-name.json
        :param self
        """
        list_messages = []
        for channel in self.channels_data:
            for offset in range(0, MESSAGES_RANGE, SIZE):
                self.messages_data = self.data_loader.fetch_messages(self.team_data['team_id'], channel['channel_id'], offset)
                list_messages += self.messages_data

            print("Completing %s" % channel['name'])
            write_to_json(DESTINATION_FOLDER_MESSAGES  % self.team_name, '/%s.json' % channel['name'], list_messages)

    def users_to_json(self):
        """
        This method writes the user data logs to json files of each channel in the team to json files.
        These files are kept in data/team-name/users/channel-name.json
        :param self
        """
        list_users = {}
        for channel in self.channels_data:
            for offset in range(0, MESSAGES_RANGE, SIZE):
                self.users_data = self.data_loader.fetch_users(self.team_data['team_id'], channel['channel_id'], offset)
                list_users = dict(list(list_users.items()) + list(self.users_data.items()))

            print('Completing ' + channel['name'])

            write_to_json(DESTINATION_FOLDER_USERS  % self.team_name, '/%s.json' % channel['name'], list_users)



def write_to_json(destination, file_name, data_to_write):
    """
    This function writes the data_to_write to a specified destination(json file).
    This first pretty prints the json and then writes.
    :param destination: The path of file to which the data is to be written
    :param data_to_write: The data which is to be written on the json file.
    """
    if not os.path.exists(destination):
        os.makedirs(destination)

    with open(destination + file_name, 'w') as write_file:
        write_file.write(json.dumps(data_to_write, indent=4, sort_keys=True))


# Uncomment the following and run the script to download the data logs for desired team.
# team = DataToJson('syple')
# team.team_to_json()
# team.channels_to_json()
# team.messages_to_json()
# team.users_to_json()

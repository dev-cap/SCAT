import json
from lib.data.slackarchive import DataLogsLoader, DataToJson
from config import *

class TestDataLogsLoader(object):


    def test_fetch_team(self):
        """
        This method tests the fetch_team() method in the DataLogsLoader() class.
        :return: AssertionError if test fails
        """
        team_object = DataLogsLoader('syple')
        team_data = team_object.fetch_team()
        assert isinstance(team_data, dict)
        required_fields = ["domain", "name", "team_id"]
        for field in required_fields:
            assert field in team_data


    def test_fetch_channels(self):
        """
        This method tests the fetch_channels() method in the DataLogsLoader() class.
        :return: AssertionError if test fails
        """
        team_object = DataLogsLoader('syple')
        team_data = team_object.fetch_team()
        channels_data = team_object.fetch_channels(team_data['team_id'])
        assert isinstance(channels_data, (list, dict))
        assert isinstance(channels_data[0], dict)
        required_fields = ["channel_id", "name", "team", "is_archived", "num_members"]
        for field in required_fields:
            assert field in channels_data[0]


    def test_fetch_messages(self):
        """
        This method tests the fetch_messages() method in the DataLogsLoader() class.
        :return: AssertionError if test fails
        """
        team_object = DataLogsLoader('syple')
        team_data = team_object.fetch_team()
        channels_data = team_object.fetch_channels(team_data['team_id'])
        messages_data = team_object.fetch_messages(team_data['team_id'], channels_data[0]['channel_id'], 0)
        assert isinstance(messages_data, (list, tuple))
        assert isinstance(messages_data[0], dict)

        message_fields = ['user', 'team', 'text', 'channel', 'ts']
        message_dict = list(messages_data[0])
        for field in message_fields:
            assert field in message_dict


    def test_fetch_users(self):
        """
        This method tests the fetch_users() method in the DataLogsLoader() class.
        :return: AssertionError if test fails
        """
        team_object = DataLogsLoader('syple')
        team_data = team_object.fetch_team()
        channels_data = team_object.fetch_channels(team_data['team_id'])
        users_data = team_object.fetch_users(team_data['team_id'], channels_data[0]['channel_id'], 0)
        assert isinstance(users_data, dict)

        user_fields = ['user_id', 'name', 'team']
        user_dict = list(users_data.values())[0]
        for field in user_fields:
            assert field in user_dict


class TestDataToJson(object):


    def test_team_to_json(self):
        """
        This method tests the team_to_json() method in the DataToJson() class.
        :return: AssertionError if test fails
        """
        data_object = DataToJson('syple')
        data_object.team_to_json()
        assert isinstance(data_object.team_data, dict)
        with open(DESTINATION_FOLDER + 'syple/team.json', 'r') as test_file:
            test_data = test_file.read()
            assert isinstance(test_data, str)
            test_data = json.loads(test_data)
            assert isinstance(test_data, dict)
            assert test_data['domain'] == 'syple'
            assert test_data['team_id'] == 'T02G1FPFC'

    def test_channels_to_json(self):
        """
        This method tests the team_to_json() method in the DataToJson() class.
        :return: AssertionError if test fails
        """
        data_object = DataToJson('syple')
        data_object.team_to_json()
        data_object.channels_to_json()
        assert isinstance(data_object.channels_data, (list, dict))
        with open(DESTINATION_FOLDER + 'syple/channels.json', 'r') as test_file:
            test_data = test_file.read()
            assert isinstance(test_data, str)
            test_data = json.loads(test_data)
            assert isinstance(test_data, (list,dict))
            assert test_data[0]['channel_id'] == data_object.channels_data[0]['channel_id']

    def test_messages_to_json(self):
        """
        This method tests the team_to_json() method in the DataToJson() class.
        :return: AssertionError if test fails
        """
        data_object = DataToJson('syple')
        data_object.team_to_json()
        data_object.channels_to_json()
        data_object.messages_to_json()
        assert isinstance(data_object.messages_data, (list, dict))
        with open(DESTINATION_FOLDER + 'syple/messages/general.json', 'r') as test_file:
            test_data = test_file.read()
            assert isinstance(test_data, str)
            test_data = json.loads(test_data)
            assert isinstance(test_data, (list,dict))
            assert test_data[0]['channel'] == 'C02G1FPFN'

    def test_users_to_json(self):
        """
        This method tests the team_to_json() method in the DataToJson() class.
        :return: AssertionError if test fails
        """
        data_object = DataToJson('syple')
        data_object.team_to_json()
        data_object.channels_to_json()
        data_object.users_to_json()
        assert isinstance(data_object.users_data, (list, dict))
        with open(DESTINATION_FOLDER + 'syple/users/general.json', 'r') as test_file:
            test_data = test_file.read()
            assert isinstance(test_data, str)
            test_data = json.loads(test_data)
            assert isinstance(test_data, (list,dict))
            assert test_data['U02G0QYAV']['user_id'] == 'U02G0QYAV'

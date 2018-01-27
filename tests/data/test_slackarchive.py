import sys
sys.path.append('../..')

from lib.data.slackarchive import DataLogsLoader, DataToJson

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



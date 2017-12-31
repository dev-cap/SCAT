import lib.data.slackarchive as slackarchive


def test_fetch_team():
    """
    This test the functioning of the SlackArchive API endpoint to fetch the team metadata.
    :return: AssertionError if test fails
    """
    team_data = slackarchive.fetch_team('kubernetes')
    assert isinstance(team_data, dict)
    required_fields = ["domain", "name", "team_id"]
    for field in required_fields:
        assert field in team_data


def test_fetch_channels():
    """
    This tests the function that fetches all the channels that are in a team, and the structure of the
    associated channel metadata.
    :return: AssertionError if test fails
    """
    team_data = slackarchive.fetch_team('kubernetes')
    channels = slackarchive.fetch_channels('kubernetes', team_data['team_id'])
    assert isinstance(channels, (list, tuple))
    assert isinstance(channels[0], dict)
    required_fields = ["channel_id", "name", "team", "is_archived", "num_members"]
    for field in required_fields:
        assert field in channels[0]


def test_fetch_messages():
    """
    This tests the function that fetches a list of messages from a channel according to the range
    specified by the user.
    :return: AssertionError if test fails
    """
    team_data = slackarchive.fetch_team('kubernetes')
    channels = slackarchive.fetch_channels('kubernetes', team_data['team_id'])
    messages = slackarchive.fetch_messages('kubernetes', team_data['team_id'], channels[0]['channel_id'], 5, 0)
    assert isinstance(messages, dict)
    assert isinstance(messages['related']['users'], dict)
    assert isinstance(messages['messages'], (list, tuple))
    assert isinstance(messages['messages'][0], dict)

    user_fields = ["user_id", "name", "team"]
    user_dict = list(messages['related']['users'].values())[0]
    for field in user_fields:
        assert field in user_dict

    message_fields = ['user', 'team', 'text', 'channel', 'ts']
    message_dict = list(messages['messages'][0])
    for field in message_fields:
        assert field in message_dict


test_fetch_messages()

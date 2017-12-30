import requests
import json


def fetch_team(domain):
    """
    This function uses the SlackArchive API endpoint to fetch the metadata of the team that belongs to a domain.
    :param domain: The domain of the Slack team. Eg. 'kubernetes' in 'https://kubernetes.slackarchive.io/'
    :return: A dict containing the metadata of the team that belongs to the domain passed as the parameter.
    """
    url = 'https://api.slackarchive.io/v1/team?domain=%s' % domain
    origin_header = {"referer": "https://%s.slackarchive.io/" % domain}
    s = requests.Session()
    teams = s.get(url, headers=origin_header)
    return json.loads(teams.content.decode('utf-8'))['team'][0]


def fetch_channels(domain, team_id):
    """
    This function uses the SlackArchive API endpoint to fetch all the channels that are in a team along
    with the relevant channel metadata.
    :param domain: The domain of the Slack team. Eg. 'kubernetes' in 'https://kubernetes.slackarchive.io/'
    :param team_id: The unique team identifier as returned by the fetch_team function.
    :return: A dict containing all the channels that are in the team identified by team_id, along with
    relevant channel metadata.
    """
    url = 'https://api.slackarchive.io/v1/channels?team_id=%s' % team_id
    origin_header = {"referer": "https://%s.slackarchive.io/" % domain}
    s = requests.Session()
    channels = s.get(url, headers=origin_header)
    return json.loads(channels.content.decode('utf-8'))['channels']


def fetch_messages(domain, team_id, channel_id, size, offset):
    """
    This function returns a list of messages from a channel according to the range specified by the size
    and offset parameters.
    :param domain: The domain of the Slack team. Eg. 'kubernetes' in 'https://kubernetes.slackarchive.io/'
    :param team_id: The unique team identifier as returned by the fetch_team function.
    :param channel_id: The unique channel identifier as returned by the fetch_channel function.
    :param size: The number of messages to fetch, in a reverse-chronological order.
    :param offset: The number of messages to skip while fetching, in a reverse-chronological order. An
    offset of 5 with a size of 100 will fetch the 100 messages after the 5 latest messages in a channel.
    :return: A dict containing a list of messages from the specified channel, in a reverse-chronological
    order, according to the range specified by the size and offset parameters.
    """
    url = "https://api.slackarchive.io/v1/messages?size=%d&team=%s&channel=%s&offset=%d" % (size, team_id, channel_id, offset)
    origin_header = {"referer": "https://%s.slackarchive.io/" % domain}
    s = requests.Session()
    messages = s.get(url, headers=origin_header)
    return json.loads(messages.content.decode('utf-8'))


if __name__ == "__main__":
    # Frame the test cases along these lines. These are to provide you an example for usage of this module.
    team_data = fetch_team('kubernetes')
    channels = fetch_channels('kubernetes', team_data['team_id'])
    for channel in channels:
        if channel['name'] == 'multi-platform':
            messages = fetch_messages('kubernetes', team_data['team_id'], channel['channel_id'], 100, 0)
    print(messages)
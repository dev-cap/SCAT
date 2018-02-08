"""
This is a driver python script that fetches data from slackarchive.io
It uses the lib/data/slackarchive.py methods to fetch the data logs.
"""

from lib.data.slackarchive import *

if __name__ == '__main__':
    team = DataToJson('syple')
    team.team_to_json()
    team.channels_to_json()
    team.messages_to_json()
    team.users_to_json()

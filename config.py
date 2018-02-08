#### General Configurations File for SCAT

#------------------------------------------------------------------------------------------#
### Configurations for lib/data/slackarchive.py


## slackarchive.io api/links to be used for fetching data logs

# Origin Header Link
ORIGIN_HEADER_LINK = "https://%s.slackarchive.io/"
# Slack Archive Team API
TEAM_API = "https://api.slackarchive.io/v1/team?domain=%s"
# Slack Archive Team's channels API
CHANNEL_API = "https://api.slackarchive.io/v1/channels?team_id=%s"
# Slack Arcihve Team's individual channels' API
MESSAGES_API = "https://api.slackarchive.io/v1/messages?size=%d&team=%s&channel=%s&offset=%d"


## Some constraints for downloading data logs

# Size of the messages data in a single fetch
SIZE = 100
# Range of messages to be downloaded for analysis (including multiple fetches)
MESSAGES_RANGE = 100


## Destination folders for different types of data logs

# Destination of Team's general data (team.json, channels.json)
DESTINATION_FOLDER = './data/'
# Destination of Team's messages
DESTINATION_FOLDER_MESSAGES = './data/%s/messages'
# Destination of Team's users data
DESTINATION_FOLDER_USERS = './data/%s/users'

#--------------------------------------------------------------------------------------------#

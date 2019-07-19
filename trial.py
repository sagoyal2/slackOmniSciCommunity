import os
import json
import requests
import feedparser
import datetime
from slack import WebClient
import sys


def get_real_content(current_summary):
    return current_summary.split("<br />", 1)[1]


def get_date(time):
    dt = datetime.datetime(time[0], time[1], time[2],
                           time[3], time[4], time[5])
    return dt


def get_channel_id(channel_name, channels_list):
    channels = channels_list['channels']
    for channel in channels:
        if channel['name'] == channel_name:
            return channel["id"]


def workspace_time(history, bot_username):
    all_messages = history['messages']
    time = None
    for message in all_messages:
        try:
            if (message['username'] == bot_username):
                for block in message['blocks']:
                    if(block['block_id'] == "DateSection"):
                        time = block['elements'][0]['text'].split(
                            "*Date:* ", 1)[1]
                break
        except:
            pass

    corrected_time = None
    if time is not None:
        corrected_time = datetime.datetime.strptime(
            time, '%a %b %d %Y %H:%M:%S')
    else:
        corrected_time = datetime.datetime.min

    return(corrected_time)


def community_time(feed):
    latestPost = feed['entries'][0]
    corrected_time = get_date(latestPost['published_parsed'])

    return corrected_time


def main():

    # RSS Feed
    community_page = feedparser.parse(
        "https://community.omnisci.com/rssgenerator?UserKey=7f2de571-92e8-49b0-ba12-27413bf99c95")

    # OAuth Token xoxp-XXXXXX....
    slack_client = WebClient(sys.argv[1])
    bot_username = sys.argv[2]
    channel_name = sys.argv[3]

    # needed scopes: channels:history, channels:read, chat:write:bot, incoming-webhook, users:read, chat:write:user
    channels_list = slack_client.channels_list()

    # Assume bot was used in last 100 messages
    history = slack_client.channels_history(
        channel=get_channel_id(channel_name, channels_list), count=100)

    ws_time = workspace_time(history, bot_username)
    comm_time = community_time(community_page)

    if(comm_time > ws_time):

        for entry in reversed(community_page['entries']):
            post_time = get_date(entry['published_parsed'])

            # You only need to check posts that were made most recently relative to the ones that
            # have already been posted on slack
            if(post_time > ws_time):
                myblock = [
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text":  "*" + entry['title'] + "*"
                        },
                        "accessory": {
                            "type": "button",
                            "text": {
                                    "type": "plain_text",
                                "text": "Original Post"
                            },
                            "url": entry['link']
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                                "type": "mrkdwn",
                            "text": get_real_content(entry['summary'])
                        }
                    },
                    {
                        "type": "context",
                        "block_id": "DateSection",
                        "elements": [
                                {
                                    "type": "mrkdwn",
                                    "text": "*Date:* " + post_time.strftime('%a %b %d %Y %H:%M:%S')
                                }
                        ]
                    },
                    {
                        "type": "context",
                        "elements": [
                                {
                                    "type": "mrkdwn",
                                    "text": "*Author:* " + entry['author']
                                }
                        ]
                    }
                ]

                slack_client.chat_postMessage(
                    channel=get_channel_id(channel_name, channels_list),
                    blocks=myblock
                )


if __name__ == "__main__":
    main()

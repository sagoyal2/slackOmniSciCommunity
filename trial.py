import os
import json
import requests
import feedparser
import jsonpickle
import datetime
from slackclient import SlackClient


def get_real_content(current_summary):
    return current_summary.split("<br />", 1)[1]


def get_date(time):
    dt = datetime.datetime(time[0], time[1], time[2],
                           time[3]-4, time[4], time[5])
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
        if (message['username'] == bot_username):
            for block in message['blocks']:
                if(block['block_id'] == "DateSection"):
                    time = block['elements'][0]['text'].split("*Date:* ", 1)[1]
            break

    corrected_time = datetime.datetime.strptime(time, '%a %b %d %Y %H:%M:%S')
    return(corrected_time)


def community_time(feed):
    latestPost = feed['entries'][0]
    corrected_time = get_date(latestPost['published_parsed'])

    return corrected_time


def main():

    community_page = feedparser.parse(
        "https://community.omnisci.com/rssgenerator?UserKey=7f2de571-92e8-49b0-ba12-27413bf99c95")

    slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
    bot_username = "memeLord"

    channels_list = slack_client.api_call("channels.list")
    history = slack_client.api_call(
        "channels.history", channel=get_channel_id("memes", channels_list), count=100)

    ws_time = workspace_time(history, bot_username)  # datetime.datetime.min
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

                slack_client.api_call(
                    "chat.postMessage",
                    channel=get_channel_id("memes", channels_list),
                    text="My message",
                    blocks=myblock
                )


if __name__ == "__main__":
    main()

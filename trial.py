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


# Time from Slack Workspace
def workspace_time(result):

    index = 0
    for message in result['messages']:
        try:
            if (message['subtype'] == "bot_message"):
                break
        except:
            pass
        index += 1

    # In the event the bot has never been used
    if(index == len(result['messages'])):
        corrected_time = datetime.datetime.min
    else:
        time = result['messages'][index]['attachments'][0]['fields'][1]['value']
        corrected_time = datetime.datetime.strptime(time, '%m/%d/%y %H:%M:%S')

    return corrected_time


# Time from Community Page
def community_time(feed):
    latestPost = feed['entries'][0]
    corrected_time = get_date(latestPost['published_parsed'])

    return corrected_time


def main():

    # SLACK_TOKEN = os.environ["SLACK_API_TOKEN"]
    # slack_client = SlackClient(SLACK_TOKEN)

    # webhook_url = 'https://hooks.slack.com/services/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'

    community_page = feedparser.parse(
        "https://community.omnisci.com/rssgenerator?UserKey=7f2de571-92e8-49b0-ba12-27413bf99c95")

    # channels_list = slack_client.api_call("channels.list")
    # result = slack_client.api_call(
    #     "channels.history", channel=get_channel_id("memes", channels_list), count=100)

    slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
    channels_list = slack_client.api_call("channels.list")
    # print(channels_list)

    # slack_client.api_call(
    #     "chat.postMessage",
    #     channel=get_channel_id("memes", channels_list),
    #     text="My message",
    #     blocks=[
    #         {
    #             "type": "section",
    #             "block_id": "section567",
    #             "text": {
    #                 "type": "mrkdwn",
    #                     "text": "This is a section block with an accessory image."
    #             },
    #             "accessory": {
    #                 "type": "image",
    #                 "image_url": "https://pbs.twimg.com/profile_images/625633822235693056/lNGUneLX_400x400.jpg",
    #                 "alt_text": "cute cat"
    #             }
    #         }
    #     ]
    # )

    # ws_time = datetime.datetime.min  # workspace_time(result)
    # comm_time = community_time(community_page)

    # if(comm_time > ws_time):

    #     for entry in reversed(community_page['entries']):
    #         post_time = get_date(entry['published_parsed'])

    #         # You only need to check posts that were made most recently relative to the ones that
    #         # have already been posted on slack
    #         if(post_time > ws_time):

    #             data = {}
    #             data["attachments"] = []

    #             extras = []
    #             extras.append({
    #                 "title": "Post Date",
    #                 "value": post_time.strftime('%m/%d/%y %H:%M:%S'),
    #                 "short": True
    #             })

    #             data["attachments"].append({
    #                 "author_name": entry['author'],
    #                 "text": get_real_content(entry['summary']),
    #                 "title": entry['title'],
    #                 "title_link": entry['link'],
    #                 "color": "#3AA3E3",
    #                 "attachment_type": "default",
    #                 "fields": extras,
    #             })

    #             response = requests.post(webhook_url, data=json.dumps(
    #                 data), headers={'Content-Type': 'application/json'})

    #             # print(json.dumps(data, indent=4))
    #             print('Response: ' + str(response.text))
    #             print('Response code: ' + str(response.status_code))

    #             del data
    #             del extras

    ws_time = datetime.datetime.min  # workspace_time(result)
    comm_time = community_time(community_page)

    if(comm_time > ws_time):

        for entry in reversed(community_page['entries']):
            post_time = get_date(entry['published_parsed'])

            # You only need to check posts that were made most recently relative to the ones that
            # have already been posted on slack
            if(post_time > ws_time):
                myblock = [
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
                                "text": "OriginalPost"
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
                        "elements": [
                                {
                                    "type": "mrkdwn",
                                    "text": "Last updated: " + post_time.strftime('%m/%d/%y %H:%M:%S')
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

    # with open('myJsonFun/input.json', 'r') as f:
    #     data = json.load(f)


if __name__ == "__main__":
    main()

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
    return dt.strftime('%m/%d/%y %H:%M:%S')


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

    time = result['messages'][index]['attachments'][0]['fields'][1]['value']
    corrected_time = datetime.datetime.strptime(time, '%m/%d/%y %H:%M:%S')

    return corrected_time


# Time from Community Page
def community_time(feed):
    latestPost = feed['entries'][0]
    time = get_date(latestPost['published_parsed'])
    corrected_time = datetime.datetime.strptime(time, '%m/%d/%y %H:%M:%S')

    return corrected_time

    # def write_recent_Time():


def main():

    SLACK_TOKEN = os.environ["SLACK_API_TOKEN"]
    slack_client = SlackClient(SLACK_TOKEN)

    webhook_url = 'https://hooks.slack.com/services/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'

    community_page = feedparser.parse(
        "https://community.omnisci.com/rssgenerator?UserKey=7f2de571-92e8-49b0-ba12-27413bf99c95")

    channels_list = slack_client.api_call("channels.list")
    result = slack_client.api_call(
        "channels.history", channel=get_channel_id("memes", channels_list), count=100)

    ws_time = workspace_time(result)
    comm_time = community_time(community_page)

    # count = 0
    # for entry in community_page['entries']:

    #     print()

    #     data = {}
    #     data["attachments"] = []

    #     extras = []
    #     extras.append({
    #         "title": "Date",
    #         "value": entry['published'],
    #         "short": True
    #     })
    #     extras.append({
    #         "title": "Date2",
    #         "value": get_date(entry['published_parsed']),
    #         "short": True
    #     })

    #     data["attachments"].append({
    #         "author_name": entry['author'],
    #         "text": get_real_content(entry['summary']),
    #         "title": entry['title'],
    #         "title_link": entry['link'],
    #         "color": "#3AA3E3",
    #         "attachment_type": "default",
    #         "fields": extras,
    #     })

    #     response = requests.post(webhook_url, data=json.dumps(
    #         data), headers={'Content-Type': 'application/json'})

    #     # print(json.dumps(data, indent=4))
    #     print('Response: ' + str(response.text))
    #     print('Response code: ' + str(response.status_code))

    #     if (count == 0):
    #         break

    #     count += 1

    #     del data
    #     del extras

    # with open('myJsonFun/input.json', 'r') as f:
    #     data = json.load(f)


if __name__ == "__main__":
    main()

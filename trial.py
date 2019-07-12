import os
import json
import requests
import feedparser
import jsonpickle
from slackclient import SlackClient


def get_real_content(current_summary):
    return current_summary.split("<br />", 1)[1]


# def get_channel_id(channel_name):
#     channels = get_channels()  # using channels.list
#     for channel in channels:
#         if channel["name"] == channel_name:
#             return channel["id"]

# def write_recent_Time():


# def read_recent_Time():

# def get_most_recentTime():

def main():

    SLACK_TOKEN = XXXX
    slack_client = SlackClient(SLACK_TOKEN)

    wekbook_url = 'https://hooks.slack.com/services/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'

    NewsFeed = feedparser.parse(
        "https://community.omnisci.com/rssgenerator?UserKey=7f2de571-92e8-49b0-ba12-27413bf99c95")

    channels = slack_client.api_call("channels.list")
    channel_id = None
    for channel in channels['channels']:
        print(channel['name'])
        if channel['name'] == "memes":
            print("here")
            channel_id = channel['id']

    res = slack_client.api_call(
        "channels.history", channel=channel_id, count=200)
    #history = slack_client.api_call("channels.history", channel=channel_id, oldest=oldest, latest=latest)

    count = 0
    for mess in res['messages']:
        # print(mess)
        # break
        try:
            if (mess['subtype'] == "bot_message"):
                print("here")
                print(count)
                break
        except:
            pass
        count += 1

    # print(res['messages'][1]['subtype'] == "bot_message")

    # count = 0
    # for entry in NewsFeed['entries']:

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
    #         "value": entry['published'],
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

    #     response = requests.post(wekbook_url, data=json.dumps(
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

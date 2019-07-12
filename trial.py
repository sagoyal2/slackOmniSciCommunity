import requests
import json


def main():
    print("Hello")

    # url = 'https://hooks.slack.com/services/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'
    # payload = '{ "type": "section", "text": { "type": "plain_text", "text": "This is a plain text section block.", "emoji": false } }, { "type": "section", "text": { "type": "plain_text", "text": "This is a plain text section block.", "emoji": false } }'
    # headers = {'Content-type': 'application/json'}
    # # curl - X POST - H 'Content-type: application/json' - -data '{"text":"Hello, World!"}'
    # # https: // hooks.slack.com/services/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

    # for i in range(10):
    #     res = requests.post(url, data=payload, headers=headers)

    # print(res.text)

    wekbook_url = 'https://hooks.slack.com/services/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'

    # data = {
    #     "attachments": [
    #         {
    #             "fallback": "Required plain-text summary of the attachment.",
    #             "color": "#36a64f",
    #             "pretext": "Optional text that appears above the attachment block",
    #             "author_name": "Bobby Tables",
    #             "author_link": "http://flickr.com/bobby/",
    #             "author_icon": "http://flickr.com/icons/bobby.jpg",
    #             "title": "Slack API Documentation",
    #             "title_link": "https://api.slack.com/",
    #             "text": "Optional text that appears within the attachment",
    #             "image_url": "http://my-website.com/path/to/image.jpg",
    #             "thumb_url": "http://example.com/path/to/thumb.png",
    #             "footer": "Slack API",
    #             "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
    #             "ts": 123456789
    #         }
    #     ]
    # }

    # data = {
    #     "attachments": [
    #         {
    #             "author_name": "Candido Dessanti",
    #             "text": "Ok I'll try to reproduce with such cardinalities, and report back",
    #             "title": "Facing Issue : ALLOCATION failed to find 256000000B free.",
    #             "title_link": "https://community.omnisci.com/communities/community-home/digestviewer/viewthread?GroupId=13&MessageKey=67",
    #             "color": "#3AA3E3",
    #             "attachment_type": "default",
    #             "fields": [
    #                 {
    #                     "title": "Project",
    #                     "value": "Awesome Project"
    #                 },
    #                 {
    #                     "title": "Environment",
    #                     "value": "production"
    #                 }
    #             ],

    #         }
    #     ]
    # }

    with open('input.json', 'r') as f:
        data = json.load(f)

    response = requests.post(wekbook_url, data=json.dumps(
        data), headers={'Content-Type': 'application/json'})

    print('Response: ' + str(response.text))
    print('Response code: ' + str(response.status_code))


if __name__ == "__main__":
    main()

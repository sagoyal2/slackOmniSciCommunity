import feedparser
import jsonpickle


def get_real_content(current_summary):
    return current_summary.split("<br />", 1)[1]


def main():

    NewsFeed = feedparser.parse(
        "https://community.omnisci.com/rssgenerator?UserKey=7f2de571-92e8-49b0-ba12-27413bf99c95")
    #entry = NewsFeed.entries[1]

    # print(entry.keys())
    # print(NewsFeed.keys())
    # # print(NewsFeed['feed']['title'])
    # print(len(NewsFeed['entries']))

    frozen = jsonpickle.encode(NewsFeed, unpicklable=False)
    result = jsonpickle.decode(frozen)

    # print(result)

    # for entry in NewsFeed.entries:
    #     print(entry.title + " : " + entry.updated +
    #           " : " + entry.content[0].value + " \n")

    # print(NewsFeed)

    count = 0
    for entry in NewsFeed['entries']:
        print('Author is: {}, they wrote this on: {}, the content was this: {}, the title is: {}, the link is: {}'.format(
            entry['author'], entry['published'], get_real_content(entry['summary']), entry['title'], entry['link']))

        print()
        print()

        if (count > 5):
            break

        count += 1


if __name__ == "__main__":
    main()

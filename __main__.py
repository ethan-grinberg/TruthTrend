#!/usr/bin/python3.9

from src.zinfo.article_selector import get_summarized_news
from src.zinfo.twitter_bot import TwitterBot

# twitter api keys
APIKEY = 'aSzivrDavDusqmo0B1rWXjwOs'
APISECRETKEY = 'GB3ob9rNnc1jtSL0SJtoSD6bdd8xVlx2NuUYkyyaiKJcgreBYy'
ACCESSTOKEN = '1425899373255331842-OzkV1pmc4gtQjiJOvvgKaLdCpBmOuY'
ACCESSTOKENSECRET = 'stfqHRxGOdEbtY0uH0vSROWjaXwjrFunVBgBu4hlq7pm3'


def main():
    summarized_news = get_summarized_news()

    # authorized twitter bot and tweet all articles
    twitter_bot = TwitterBot(APIKEY, APISECRETKEY, ACCESSTOKEN, ACCESSTOKENSECRET)
    twitter_bot.tweet_all_articles(summarized_news)


if __name__ == "__main__":
    main()

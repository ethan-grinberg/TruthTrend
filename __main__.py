#!/usr/bin/python3.9

from src.zinfo.article_selector import get_summarized_news
from src.zinfo.twitter_bot import TwitterBot
from src.zinfo.news_scraper import NewsScraper
# twitter api keys
from settings import APIKEY, APISECRETKEY, ACCESSTOKEN, ACCESSTOKENSECRET

def main():
    summarized_news = get_summarized_news()

    # authorized twitter bot and tweet all articles
    twitter_bot = TwitterBot(APIKEY, APISECRETKEY, ACCESSTOKEN, ACCESSTOKENSECRET)
    twitter_bot.tweet_all_articles(summarized_news)

if __name__ == "__main__":
    main()

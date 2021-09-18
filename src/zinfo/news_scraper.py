import newspaper
from newsapi.newsapi_client import NewsApiClient
from newsapi.newsapi_exception import NewsAPIException
from datetime import date
import pandas as pd
from settings import news_keys

class NewsScraper:
    def __init__(self):
        self.API_KEYS = news_keys
        self.sort_method = "relevancy"

        self.API_KEY = self.API_KEYS[0]
        self.newsapi = NewsApiClient(api_key=self.API_KEY)

    def set_api_key(self, api_key):
        self.API_KEY = api_key
        self.newsapi = NewsApiClient(api_key=api_key)

    # TODO currently iterates over the same key even if it doesn't work, optimize
    def pick_different_api_key(self, query, q_date, page):
        # switch to next api key
        self.set_api_key(self.API_KEYS[1])

        page_articles = []
        # starts at 1 because first api key was already chosen
        for i in range(1, len(self.API_KEYS)):
            print("switching to " + str(i) + " index of api keys")
            try:
                page_articles = self.newsapi.get_everything(q=query, language='en', from_param=q_date, page=page,
                                                            sort_by=self.sort_method)
                break
            except NewsAPIException as e:
                if i == (len(self.API_KEYS) - 1):
                    raise ValueError("all api keys are used up")

                self.set_api_key(self.API_KEYS[i + 1])

        return page_articles

    def get_all_articles(self, query, q_date):
        articles = []
        # TODO get rid of hard coding, only like this because of developer plan
        for i in range(1, 5):
            page_articles = []
            try:
                page_articles = self.newsapi.get_everything(q=query, language='en', from_param=q_date, page=i,
                                                            sort_by=self.sort_method)
            except NewsAPIException as e:
                print("current key didn't work")
                page_articles = self.pick_different_api_key(query, q_date, i)

            if len(page_articles) == 0:
                break
            else:
                articles.extend(page_articles["articles"])

        return articles

    # TODO work on finding better way to get trending topics and get more related news
    def get_trending_articles_today(self, num_trends=len(newspaper.hot())):
        today = date.today().strftime("%Y-%m-%d")
        # gets trending google searches
        trending_topics = newspaper.hot()

        # gets smaller sample if prompted by user
        if num_trends < len(trending_topics):
            trending_topics = trending_topics[:num_trends]

        print("scraping articles for " + str(num_trends) + " trends on " + today + "...")
        data = []
        for topic in trending_topics:
            articles = self.get_all_articles(topic, today)

            # add all article info for topic to data
            article_info = [(article['publishedAt'], article['title'], article['url'], article["source"]["name"], topic) for article in articles]
            data.extend(article_info)

        # combine data, remove duplicate articles, and drop na
        trending_news = pd.DataFrame(data, columns=["date", "title", "url", "source", "topic"])
        trending_news = trending_news.drop_duplicates(subset=['title'])
        trending_news = trending_news.dropna(subset=["title"])
        print("scraped " + str(len(trending_news)) + " articles")
        return trending_news

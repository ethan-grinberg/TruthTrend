import newspaper
from newsapi.newsapi_client import NewsApiClient
from datetime import date
import pandas as pd


class NewsScraper:
    def __init__(self, api_key):
        self.API_KEY = api_key
        self.newsapi = NewsApiClient(api_key=self.API_KEY)

    def get_all_articles(self, query, q_date):
        articles = []
        # TODO get rid of hard coding, only like this because of developer plan
        for i in range(1, 5):
            page_articles = self.newsapi.get_everything(q=query, language='en', from_param=q_date, page=i)

            if len(page_articles) == 0:
                break
            else:
                articles.extend(page_articles["articles"])

        return articles

    # TODO work on finding better way to get trending topics and get more related news
    def get_trending_articles_today(self, num_trends=len(newspaper.hot())):
        print("scraping articles for " + str(num_trends) + " trends")

        today = date.today().strftime("%Y-%m-%d")
        # gets trending google searches
        trending_topics = newspaper.hot()

        # gets smaller sample if prompted by user
        if num_trends < len(trending_topics):
            trending_topics = trending_topics[:num_trends]

        data = []
        for topic in trending_topics:
            articles = self.get_all_articles(topic, today)

            # add all article info for topic to data
            article_info = [(article['publishedAt'], article['title'], article['url'], topic) for article in articles]
            data.extend(article_info)

        return pd.DataFrame(data, columns=["date", "title", "url", "topic"])

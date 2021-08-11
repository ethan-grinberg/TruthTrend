import newspaper
from newsapi.newsapi_client import NewsApiClient
from datetime import date
import pandas as pd

API_KEY = 'debd522136164978a43f9815fe4dde7d'
newsapi = NewsApiClient(api_key=API_KEY)


def get_all_articles(query, q_date):
    articles = []
    # goes through all pages until there is no news left, 5 usually is the max
    for i in range(1, 5):
        page_articles = newsapi.get_everything(q=query, language='en', from_param=q_date, page=i)

        if len(page_articles) == 0:
            break
        else:
            articles.extend(page_articles["articles"])

    return articles


# TODO work on finding better way to get trending topics and get more related news
def get_trending_articles_today():
    today = date.today().strftime("%Y-%m-%d")
    # gets trending google searches
    trending_topics = newspaper.hot()

    data = []
    for topic in trending_topics:
        articles = get_all_articles(topic, today)

        # add all article info for topic to data
        article_info = [(article['publishedAt'], article['title'], article['url'], topic) for article in articles]
        data.extend(article_info)

    return pd.DataFrame(data, columns=["date", "title", "url", "topic"])

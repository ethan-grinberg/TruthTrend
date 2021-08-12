import pandas as pd
import numpy as np
import os
from datetime import date
from sklearn.metrics import pairwise_distances_argmin_min

from src.zinfo.news_scraper import NewsScraper
from src.zinfo.article_clustering import cluster_articles

NEWS_FILE = 'selected_articles.csv'


def get_mean_vec(vectors, vector_length=300):
    total = np.zeros(vector_length)
    for vec in vectors:
        total += vec

    mean = total / len(vectors)
    return mean


def get_central_vec_title(cluster):
    # get the title vectors for the cluster
    vectors = cluster.vectors.to_list()

    mean_vec = get_mean_vec(vectors)
    index = pairwise_distances_argmin_min(np.array([mean_vec]), vectors)[0][0]

    # returns the best article from the cluster
    return cluster.title.iloc[index]


def get_best_article_all_clusters(clusters, article_df):
    print("selecting best articles out of each cluster")

    all_news = []
    for cluster in clusters.label.unique():
        # unclustered category
        if cluster == -1:
            continue

        # get best article from cluster
        cluster_titles = clusters.loc[clusters.label == cluster]
        best_article = get_central_vec_title(cluster_titles)

        # look up in original df
        cluster_df = article_df.loc[article_df.title == best_article].copy()
        cluster_df["num_articles"] = len(cluster_titles)

        all_news.append(cluster_df)

    return pd.concat(all_news)


def add_news_to_history_file(summarized_news):
    os.chdir("..")
    os.chdir("..")
    os.chdir("data/")

    summarized_news["date"] = date.today()
    existing_news = pd.read_csv(NEWS_FILE)
    combined_news = pd.concat([existing_news, summarized_news])
    combined_news = combined_news.reset_index(drop=True)

    # write all data to file
    combined_news.to_csv(NEWS_FILE, index=False)

    os.chdir("..")
    os.chdir("src/zinfo/")


# function that ties the scraping, clustering, and article selection together
def get_summarized_news(api_key):
    # gets all trending news articles
    scraper = NewsScraper(api_key)
    trending_news = scraper.get_trending_articles_today()
    trending_news = trending_news.drop_duplicates(subset=['title'])

    # put all trending news into clusters and pick most objective article for each one
    clusters = cluster_articles(trending_news)
    summarized_news = get_best_article_all_clusters(clusters, trending_news)
    summarized_news = summarized_news.reset_index(drop=True)

    # add to record file to keep track of all articles uploaded
    add_news_to_history_file(summarized_news.copy())

    return summarized_news

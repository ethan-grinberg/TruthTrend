import pandas as pd
import numpy as np

# cluster stuff
from sklearn.cluster import DBSCAN
from sklearn.metrics import pairwise_distances_argmin_min
from sklearn.neighbors import NearestNeighbors

# nlp stuff
import spacy

nlp = spacy.load('en_core_web_lg')

# summarization
from rake_nltk import Rake

rake_nltk_var = Rake()


def preprocess_text(text):
    doc = nlp(text)
    tokens = [w.lower_ for w in doc if not (w.is_stop or w.is_punct)]
    preproc_text = " ".join(tokens)
    return preproc_text


def get_best_eps_val(vectors, neighbors=2):
    neigh = NearestNeighbors(n_neighbors=neighbors)
    nbrs = neigh.fit(vectors)

    distances, indices = nbrs.kneighbors(vectors)

    # return half of first non zero distance value
    distances = np.sort(distances, axis=0)
    distances = distances[:, 1]
    non_zero = distances.nonzero()

    return distances[non_zero[0][0]] / 2


def cluster_articles(df, min_articles=6):
    sent_vecs = {}
    for title in df.title:
        try:
            doc = nlp(preprocess_text(title))
            sent_vecs.update({title: doc.vector})
        except Exception as e:
            print(e)

    vectors = list(sent_vecs.values())
    titles = list(sent_vecs.keys())

    # create clusters out of news titles
    x = np.array(vectors)

    # finds best eps value for dbscan
    eps = get_best_eps_val(x)

    # clusters articles using dbscan
    dbscan = DBSCAN(eps=eps, min_samples=min_articles, metric='cosine').fit(x)
    clusters = pd.DataFrame({'label': dbscan.labels_, 'title': titles, 'vectors': vectors})

    return clusters


def get_mean_vec(vectors):
    total = np.zeros(300)
    for vec in vectors:
        total += vec

    mean = total / len(vectors)
    return mean


def get_central_vec_title(cluster):
    vectors = cluster.vectors.to_list()

    mean_vec = get_mean_vec(vectors)
    index = pairwise_distances_argmin_min(np.array([mean_vec]), vectors)[0][0]

    return cluster.title.iloc[index]


def get_categorized_news(clusters, article_df):
    summarized_news = []
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

        summarized_news.append(cluster_df)

    return pd.concat(summarized_news)


def label_cluster(row):
    document = row.title

    # extract longest keword
    rake_nltk_var.extract_keywords_from_text(document)
    keyword_extracted = rake_nltk_var.get_ranked_phrases()
    title = max(keyword_extracted, key=len)

    return title


trending_news = get_trending_articles_today(100)
trending_news = trending_news.drop_duplicates(subset=['title'])

# put all trending news into clusters and pick most objective article for each one
clusters = cluster_articles(trending_news)
summarized_news = get_categorized_news(clusters, trending_news)

# summarize each cluster
summarized_news = summarized_news.reset_index(drop=True)
summarized_news["cluster_title"] = summarized_news.apply(label_cluster, axis=1)

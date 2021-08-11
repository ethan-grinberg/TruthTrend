import pandas as pd
import numpy as np

# cluster algorithms
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors

# nlp modules
import spacy
nlp = spacy.load('en_core_web_lg')


# removes stop words and punctuation from title for vectorization
def preprocess_text(text):
    doc = nlp(text)
    tokens = [w.lower_ for w in doc if not (w.is_stop or w.is_punct)]
    preproc_text = " ".join(tokens)
    return preproc_text


# finds optimal epsilon value for dbscan clustering
def get_best_eps_val(vectors, neighbors=2, eps_factor=2):
    neigh = NearestNeighbors(n_neighbors=neighbors)
    nbrs = neigh.fit(vectors)

    distances, indices = nbrs.kneighbors(vectors)

    # return first non zero distance value divided by eps factor
    distances = np.sort(distances, axis=0)
    distances = distances[:, 1]
    non_zero = distances.nonzero()

    return distances[non_zero[0][0]] / eps_factor


def get_best_min_sample_val(num_total_articles, factor=132):
    return int(num_total_articles / factor)


def cluster_articles(df):
    sent_vecs = {}
    # make each article title into a vector
    for title in df.title:
        try:
            doc = nlp(preprocess_text(title))
            sent_vecs.update({title: doc.vector})
        except Exception as e:
            print(e)

    vectors = list(sent_vecs.values())
    x = np.array(vectors)

    # finds best hyper parameters for dbscan
    eps = get_best_eps_val(x)
    min_articles = get_best_min_sample_val(len(df))
    # clusters articles using dbscan
    dbscan = DBSCAN(eps=eps, min_samples=min_articles, metric='cosine').fit(x)

    titles = list(sent_vecs.keys())
    return pd.DataFrame({'label': dbscan.labels_, 'title': titles, 'vectors': vectors})

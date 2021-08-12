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


def get_vectorized_titles(df):
    sent_vecs = {}
    # make each article title into a vector
    for title in df.title:
        try:
            doc = nlp(preprocess_text(title))
            sent_vecs.update({title: doc.vector})
        except Exception as e:
            print(e)

    vectors = list(sent_vecs.values())
    titles = list(sent_vecs.keys())

    return vectors, titles


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
    absolue_min = 2
    if num_total_articles <= absolue_min * num_total_articles:
        return absolue_min
    else:
        return int(num_total_articles / factor)


def cluster_articles(df):
    print("clustering articles")

    vectors, titles = get_vectorized_titles(df)
    x = np.array(vectors)

    # finds best hyper parameters for dbscan
    eps = get_best_eps_val(x)
    min_articles = get_best_min_sample_val(len(df))
    print("eps_val: " + str(eps) + "\n" + "min_samples: " + str(min_articles))

    # clusters articles using dbscan
    dbscan = DBSCAN(eps=eps, min_samples=min_articles, metric='cosine').fit(x)

    return pd.DataFrame({'label': dbscan.labels_, 'title': titles, 'vectors': vectors})

from typing import List, Dict
import pandas as pd
import numpy as np
import string

class_probs = None
term_probs = None
base_terms = None

def train(training_docs: List[Dict]):
    global class_probs
    global term_probs
    global base_terms

    alpha = 0.1
    train_data = pd.DataFrame(training_docs)
    base_terms = get_vocabulary(train_data)
    tf_mat = build_tf(train_data, base_terms)
    y_train = train_data['category']


    class_probs = np.log10(y_train.value_counts() / y_train.shape[0])
    nominator = np.log10(tf_mat.groupby(y_train).sum() + alpha)
    denominator = np.log10(tf_mat.groupby(y_train).sum().sum(axis=1) + alpha * tf_mat.shape[0])
    term_probs = nominator.sub(denominator, axis = 0)


def classify(doc: Dict) -> int:
    terms = list(set(text_to_words(doc['body']) + text_to_words(doc['title'])) & set(base_terms))
    scores = np.zeros(class_probs.shape[0])
    for i in range(scores.shape[0]):
        scores[i] = class_probs.loc[i + 1] + term_probs[terms].sum(axis=1).loc[i + 1]
    return np.argmax(scores) + 1


def text_to_words(text):
    replace_punctuation = str.maketrans(string.punctuation, ' '*len(string.punctuation))
    return text.translate(replace_punctuation).lower().split()


def get_vocabulary(data):
    terms = set()
    for doc_idx in data.index:
        body_words = text_to_words(data.loc[doc_idx].body)
        title_words = text_to_words(data.loc[doc_idx].title)
        terms.update(body_words + title_words)
    return list(terms)


def build_tf(data, terms):
    n = data.shape[0]
    v = len(terms)
    weight_matrix = np.zeros((n, v))

    for doc_idx in data.index:
        doc = data.loc[doc_idx]
        body_words = text_to_words(doc.body)
        title_words = text_to_words(doc.title)
        weight_matrix[doc_idx] = np.zeros(v)
        for w in set(body_words + title_words):
            if w in terms:
                weight_matrix[doc_idx][terms.index(w)] = body_words.count(w) + title_words.count(w)

    return pd.DataFrame(weight_matrix, index=data.index, columns=terms)

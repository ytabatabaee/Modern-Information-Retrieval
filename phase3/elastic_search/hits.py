from elasticsearch import Elasticsearch
from elasticsearch import helpers
import numpy as np
import heapq
from prettytable import PrettyTable


max_ref = 10
num_iter = 5


def find_top_authors(es_address, author_num):
    papers = retrieve_papers(es_address)
    authors, adj_matrix = build_adjacency_matrix(papers)
    hits(adj_matrix, author_num, authors)


def hits(adj_matrix, author_num, authors):
    n = adj_matrix.shape[0]
    h = np.ones(n) / n
    a = np.ones(n) / n
    for iter in range(num_iter):
        a = np.dot(adj_matrix.T, h)
        h = np.dot(adj_matrix, a)
        h = h / np.linalg.norm(h)
        a = a / np.linalg.norm(a)
    best_authors = heapq.nlargest(author_num, zip(a, authors))
    print("-------------------------------------------")
    x = PrettyTable()
    x.field_names = ["Author Name", "Authority Score"]
    for (score, a) in best_authors:
        x.add_row([a, score])
    print(x)


def retrieve_papers(es_address):
    es = Elasticsearch(['http://' + es_address + '/'])
    res = es.search(
        index = 'paper-index',
        body = {
            "query": {
                "bool": {
                    "should": [{
                      "match_all": {
                      }
                    }]
                }}},
        size = 2000)['hits']['hits']
    papers = []
    for i in range(len(res)):
        paper = res[i]['_source']['paper']
        papers.append(paper)
    return papers


def build_adjacency_matrix(papers):
    n = len(papers)
    authors = []
    for i in range(n):
        authors.extend(papers[i]['authors'])
    authors = sorted(list(set(authors)))
    m = len(authors)
    adj_matrix = np.zeros((m, m))

    for i in range(n):
        refs = papers[i]['references'][0:max_ref]
        authors_s =  papers[i]['authors']
        authors_d = []
        for ref in refs:
            ref_id = ref.split('paper/')[1]
            for j in range(n):
                if papers[j]['id'] == ref_id:
                    authors_d.extend(papers[j]['authors'])
        authors_d = list(set(authors_d))
        for a in authors_s:
            for b in authors_d:
                adj_matrix[authors.index(a)][authors.index(b)] = 1
    return authors, adj_matrix

from elasticsearch import Elasticsearch
from elasticsearch import helpers
import numpy as np
from elastic_search.indexing import update_index
import heapq
from prettytable import PrettyTable


max_ref = 10
num_iter = 100

def page_rank(es_address, alpha):
    papers = retrieve_papers(es_address)
    prob_matrix = build_adjacency_matrix(papers)
    v = np.ones((1, len(papers))) / len(papers)
    p = (1 - alpha) * prob_matrix + alpha * v
    for i in range(num_iter):
        v = np.matmul(v, p)
    print('pagerank = ', v[0])
    papers = add_to_papers(v, papers)
    update_index(papers, es_address)
    print('Pagerank added to index successfully!')
    print("-------------------------------------------")
    print("10 Top papers with hightest pagerank")
    x = PrettyTable()
    x._max_width = {"Paper Title" : 80}
    x.field_names = ["Paper Title", "Page Rank"]
    best_papers = heapq.nlargest(10, zip(v[0], [p['title'] for p in papers]))
    for (pr, title) in best_papers:
        x.add_row([title, pr])
    print(x)
    return v


def add_to_papers(pagerank, papers):
    for i in range(len(papers)):
        papers[i]['pagerank'] = pagerank[0][i]
    return papers


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
    prob_matrix = np.zeros((n, n))
    for i in range(n):
        refs = papers[i]['references'][0:max_ref]
        ref_count = 0
        for ref in refs:
            ref_id = ref.split('paper/')[1]
            for j in range(n):
                if papers[j]['id'] == ref_id:
                    ref_count += 1
                    prob_matrix[i][j] = 1
                    break
        if ref_count != 0:
            prob_matrix[i] /= ref_count
        else:
            prob_matrix[i] = 1 / n
    return prob_matrix

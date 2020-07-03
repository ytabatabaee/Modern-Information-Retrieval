from elasticsearch import Elasticsearch
from elasticsearch import helpers
import numpy as np

max_ref = 10

def page_rank(es_address, alpha):
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
    build_adjacency_matrix(papers)


def build_adjacency_matrix(papers):
    n = len(papers)
    prob_matrix = np.zeros((n, n))
    for i in range(len(papers)):
        refs = papers[i]['references'][0:max_ref]
        ref_count = 0
        for ref in refs:
            ref_id = ref.split('paper/')[1]
            for j in range(len(papers)):
                if papers[j]['id'] == ref_id:
                    ref_count += 1
                    prob_matrix[i][j] = 1
                    break
        if ref_count != 0:
            prob_matrix[i] /= ref_count
    return prob_matrix


if __name__ == '__main__':
    res = page_rank('localhost:9200', 0.1)

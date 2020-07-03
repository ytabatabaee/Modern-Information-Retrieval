from elasticsearch import Elasticsearch
from elasticsearch import helpers
import pprint


def search_query(es_address, title, abstract, date, title_weight, abstract_weight, date_weight, use_pagerank):
    es = Elasticsearch(['http://' + es_address + '/'])
    query_constraits = []
    query_constraits.append({
        "match": {
            "title": {
                "query": title,
                "boost": title_weight,
            }
        }})
    query_constraits.append({
        "match": {
            "abstract": {
                "query": abstract,
                "boost": abstract_weight,
            }
        }})
    query_constraits.append({
        "range": {
            "date": {
                "gte": date,
                "boost": date_weight
            }
        }})
    if use_pagerank:
        query_constraits.append({
            "range": {
                "pagerank": {
                    "gte": 0,
                    "boost": 1
                }
            }})

    return es.search(
        index = 'paper-index',
        doc_type = 'paper',
         body = {
            "query": {
                "bool": {
                    "should": query_constraits
                }
            }
        })['hits']


if __name__ == '__main__':
    res = search_query('localhost:9200', '', '', '2015', 1, 1, 1, False)
    print(res)
    pprint(res)

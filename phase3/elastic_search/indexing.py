import sys
import json
from elasticsearch import Elasticsearch
from elasticsearch import helpers


es_address = sys.argv[1]
crawl_result_address = sys.argv[2]
es = None


def create_index():
    global es
    es.indices.create(index='paper-index')
    papers = []
    with open('crawl.json') as fp:
        crawl_res = json.load(fp)
        for paper in crawl_res:
            papers.append({'_index': 'paper-index', 'paper': paper})
    helpers.bulk(es, papers)


def delete_index():
    global es
    es.indices.delete(index="paper-index")


def connect_elasticsearch():
    global es
    address = 'http://' + es_address + '/'
    es = Elasticsearch([address])
    if not es.ping():
        print("Could not connect to Elastic Search at ", address)

if __name__ == '__main__':
    connect_elasticsearch()
    create_index()
    # delete_index()

import sys
import json
from elasticsearch import Elasticsearch
from elasticsearch import helpers


def create_index(es_address, crawled_fp):
    es = connect_to_es(es_address)
    es.indices.create(index='paper-index')
    papers = []
    with open(crawled_fp) as fp:
        crawl_res = json.load(fp)
        for paper in crawl_res:
            papers.append({'_index': 'paper-index', 'paper': paper})
    helpers.bulk(es, papers)
    print("Index created successfully!")


def update_index(papers, es_address):
    delete_index(es_address)
    es = connect_to_es(es_address)
    es.indices.create(index='paper-index')
    new_papers = []
    for paper in papers:
        new_papers.append({'_index': 'paper-index', 'paper': paper})
    helpers.bulk(es, new_papers)


def delete_index(es_address):
    es = connect_to_es(es_address)
    es.indices.delete(index="paper-index")
    print("Index deleted successfully!")


def connect_to_es(es_address):
    address = 'http://' + es_address + '/'
    es = Elasticsearch([address])
    if not es.ping():
        print("Could not connect to Elastic Search at ", address)
        exit(0)
    return es


if __name__ == '__main__':
    create_index('localhost:9200', 'crawl.json')
    # delete_index('localhost:9200')

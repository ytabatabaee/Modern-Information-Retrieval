from elasticsearch import Elasticsearch
from elasticsearch import helpers

num_query = 10

def search_query(es_address, title, abstract, date, title_weight=1, abstract_weight=1, date_weight=1, use_pagerank=False):
    es = Elasticsearch(['http://' + es_address + '/'])
    query_constraits = []
    query_constraits.append({
        "match": {
            "paper.title": {
                "query": title,
                "boost": title_weight,
            }
        }})
    query_constraits.append({
        "match": {
            "paper.abstract": {
                "query": abstract,
                "boost": abstract_weight,
            }
        }})
    query_constraits.append({
        "range": {
            "paper.date": {
                "gte": date,
                "boost": date_weight,
            }
        }})
    if use_pagerank:
        query_constraits.append({
            "range": {
                "pagerank": {
                    "gte": 0,
                    "boost": 10000000,
                }
            }})
    try:
        papers = es.search(
            index = 'paper-index',
            body = {
                "query": {
                    "bool": {
                        "should": query_constraits
                    }
                }
            },
            size = num_query)['hits']['hits']
    except:
        print("Search Failed!")

    print("-------------------------------------------")
    print("Search results for query:")
    print("Title = ", title, " with weight ", float(title_weight))
    print("Abstract = ", abstract, " with weight ", float(abstract_weight))
    print("Date (Starting from) = ", date, " with weight ", float(date_weight))
    print("-------------------------------------------")


    for i in range(len(papers)):
        paper = papers[i]['_source']['paper']
        print("Paper ", str(i + 1), "with score", papers[i]["_score"] + "\n")
        print("* Title: ", paper['title'] + "\n")
        print("* Abstract: ", paper['abstract'] + "\n")
        print("* Authors:", paper['authors'] + "\n")
        print("* Date: ", paper['date'])
        print("-------------------------------------------")



if __name__ == '__main__':
    search_query('localhost:9200', 'Neural', 'Net', '2019', 1, 10, 100, False)

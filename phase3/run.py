import questionary
from elastic_search.indexing import create_index, delete_index
from elastic_search.pagerank import page_rank
from elastic_search.hits import find_top_authors
from elastic_search.search import search_query
from scrapy.crawler import CrawlerProcess
from semantic_scholar_crawler.semantic_scholar_crawler.spiders.article_crawler import ArticleCrawlerSpider
import os

if __name__ == "__main__":
    while True:
        section = questionary.select(
            "Select a section to run:",
            choices=["1. Crawling", "2. Indexing", "3. Page Rank", "4. Search", "5. HITS", "6. Exit"],
        ).ask()

        if section == "1. Crawling":
            try:
                start_urls_count = int(questionary.text("Enter number of start urls: ").ask())
            except:
                print("You should have entered an integer!")
                continue
            if start_urls_count == 0:
                start_urls = ['https://www.semanticscholar.org/paper/The-Lottery-Ticket-Hypothesis%3A-Training-Pruned-Frankle-Carbin/f90720ed12e045ac84beb94c27271d6fb8ad48cf',
                              'https://www.semanticscholar.org/paper/Attention-is-All-you-Need-Vaswani-Shazeer/204e3073870fae3d05bcbc2f6a8e263d9b72e776',
                              'https://www.semanticscholar.org/paper/BERT%3A-Pre-training-of-Deep-Bidirectional-for-Devlin-Chang/df2b0e26d0599ce3e70df8a9da02e51594e0e992']
            else:
                start_urls = []
                for i in range(start_urls_count):
                    start_urls.append(questionary.text("Enter start url " +  str(i+1) + " :").ask())
            try:
                max_crawled = int(questionary.text("Enter number of articles to crawl: ").ask())
            except:
                max_crawled = 2000
                print("You should have entered an integer!")
            process = CrawlerProcess(settings={'FEED_FORMAT': 'json', 'FEED_URI': 'crawl.json'})
            process.crawl(ArticleCrawlerSpider, start_urls=start_urls, max_crawled=max_crawled)
            process.start()


        elif section == "2. Indexing":
            es_address = questionary.text("Enter elastic search host and port as 'host:port': ").ask()
            indexing_choice = questionary.select(
                "Select which indexing task you want to perform:",
                choices=["1. Create Index", "2. Delete Index"],
            ).ask()
            if indexing_choice == "1. Create Index":
                json_address = questionary.text("Enter crawled json file address as 'x.json': ").ask()
                create_index(es_address, json_address)

            if indexing_choice == "2. Delete Index":
                delete_index(es_address)


        elif section == "3. Page Rank":
            es_address = questionary.text("Enter elastic search host and port as 'host:port': ").ask()
            try:
                alpha = float(questionary.text("Enter alpha parameter in pagerank: ").ask())
            except:
                print("You should have entered a number!")
                continue
            page_rank(es_address, alpha)


        elif section == "4. Search":
            es_address = questionary.text("Enter elastic search host and port as 'host:port': ").ask()
            title = questionary.text("Enter query title: ").ask()
            try:
                title_weight = float(questionary.text("Enter title weight: ").ask())
            except:
                print("You should have entered a number!")
                continue
            abstract = questionary.text("Enter query abstract: ").ask()
            try:
                abstract_weight = float(questionary.text("Enter abstract weight: ").ask())
            except:
                print("You should have entered a number!")
                continue
            date = questionary.text("Enter query date: ").ask()
            try:
                date_weight = float(questionary.text("Enter date weight: ").ask())
            except:
                print("You should have entered a number!")
                continue
            use_pagerank = questionary.confirm("Do you want to use pagerank in your search? ").ask()
            search_query(es_address, title, abstract, date, title_weight, abstract_weight, date_weight, use_pagerank)


        elif section == "5. HITS":
            es_address = questionary.text("Enter elastic search host and port as 'host:port': ").ask()
            try:
                n = int(questionary.text("Enter number of top authors: ").ask())
            except:
                print("You should have entered an integer!")
                continue
            find_top_authors(es_address, n)


        elif section == "6. Exit":
            exit(0)

import questionary
from elastic_search.indexing import create_index, delete_index
from elastic_search.pagerank import page_rank
from elastic_search.hits import find_top_authors

if __name__ == "__main__":
    while True:
        section = questionary.select(
            "Select a section to run:",
            choices=["1. Crawling", "2. Indexing", "3. Page Rank", "4. Search", "5. HITS", "6. Exit"],
        ).ask()
        if section == "1. Crawling":
            start_urls_count = int(questionary.text("Enter number of start urls: ").ask())
            start_urls = []
            for i in range(start_urls_count):
                start_urls[i] = questionary.text("Enter start url ", i, " :").ask()
            max_crawled = int(questionary.text("Enter number of articles to crawl: ").ask())
            print(start_urls)
            print(max_crawled)

        elif section == "2. Indexing":
            json_address = questionary.text("Enter crawled json file address: ").ask()
            es_address = questionary.text("Enter elastic search host and port as 'host:port': ").ask()
            indexing_choice = questionary.select(
                "Select which indexing task you want to perform:",
                choices=["1. Create Index", "2. Delete Index"],
            ).ask()
            print(json_address)
            print(es_address)

        elif section == "3. Page Rank":
            es_address = questionary.text("Enter elastic search host and port as 'host:port': ").ask()
            alpha = float(questionary.text("Enter alpha parameter in pagerank: ").ask())
            page_rank(es_address, alpha)


        elif section == "4. Search":
            es_address = questionary.text("Enter elastic search host and port as 'host:port': ").ask()
            title = questionary.text("Enter query title: ").ask()
            title_weight = float(questionary.text("Enter title weight: ").ask())
            abstract = questionary.text("Enter query abstract: ").ask()
            abstract_weight = float(questionary.text("Enter abstract weight: ").ask())
            date = questionary.text("Enter query date: ").ask()
            date_weight = float(questionary.text("Enter date weight: ").ask())
            use_pagerank = questionary.confirm("Do you want to use pagerank in your search? ").ask()

        elif section == "5. HITS":
            es_address = questionary.text("Enter elastic search host and port as 'host:port': ").ask()
            n = int(questionary.text("Enter number of top authors: ").ask())

        elif section == "6. Exit":
            exit(0)

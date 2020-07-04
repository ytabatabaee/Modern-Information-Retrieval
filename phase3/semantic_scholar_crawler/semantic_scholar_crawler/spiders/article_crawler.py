import scrapy
import sys


class ArticleCrawlerSpider(scrapy.Spider):
    name = 'article_crawler'
    allowed_domains = ['https://www.semanticscholar.org/']
    start_urls = ['https://www.semanticscholar.org/paper/The-Lottery-Ticket-Hypothesis%3A-Training-Pruned-Frankle-Carbin/f90720ed12e045ac84beb94c27271d6fb8ad48cf',
                  'https://www.semanticscholar.org/paper/Attention-is-All-you-Need-Vaswani-Shazeer/204e3073870fae3d05bcbc2f6a8e263d9b72e776',
                  'https://www.semanticscholar.org/paper/BERT%3A-Pre-training-of-Deep-Bidirectional-for-Devlin-Chang/df2b0e26d0599ce3e70df8a9da02e51594e0e992']
    max_crawled = 2000
    max_ref = 10
    crawled_set = set()


    def parse(self, response):
        global crawled_set
        if len(self.crawled_set) >= self.max_crawled:
            return
        if response.status != 200:
            return
        content = self.parse_paper_content(response)
        if content['id'] in self.crawled_set:
            return
        self.crawled_set.add(content['id'])
        yield content
        if len(self.crawled_set) >= self.max_crawled:
            return
        for ref in content['references'][:self.max_ref]:
            yield scrapy.Request(url=ref, callback=self.parse, dont_filter=True)


    def parse_paper_content(self, response):
        id = response.url.split('paper/')[1]
        title = response.xpath("//meta[@name='citation_title']/@content").get()
        authors = response.xpath("//meta[@name='citation_author']/@content").getall()
        date = response.xpath("//meta[@name='citation_publication_date']/@content").get()
        abstract = response.xpath("//meta[@name='description']/@content").get()
        references = response.xpath("//div[@class='citation-list__citations']//div/div/h2/a/@href").getall()
        references = list(set([self.allowed_domains[0][:-1] + ref for ref in references]))
        return {'id': id, 'title': title, 'authors': authors, 'date': date, 'abstract': abstract, 'references': references}

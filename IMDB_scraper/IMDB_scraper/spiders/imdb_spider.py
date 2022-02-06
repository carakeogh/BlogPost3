# to run
# scrapy crawl imdb_spider -o movies.csv

import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'

    start_urls = ['https://www.imdb.com/title/tt2467372/?ref_=fn_al_tt_1']

    def parse(self, response):
        next_page = response.css("li.ipc-metadata-list__item a").attrib["href"]

        if next_page:
            next_page = response.urljoin(next_page)
            
            yield scrapy.Request(next_page, callback = self.parse_full_credits)


    def parse_full_credits(self, response):
        pass

    def parse_actor_page(self, response):
        pass
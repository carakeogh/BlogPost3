# to run
# scrapy crawl imdb_spider -o movies.csv

import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'

    start_urls = ['https://www.imdb.com/title/tt2467372/?ref_=fn_al_tt_1']

    def parse(self, response):
        next_page = response.css("li.ipc-metadata-list__item a").attrib["href"]

        if next_page:
            cast_page = response.urljoin(next_page)
            
            yield scrapy.Request(cast_page, callback = self.parse_full_credits)

    def parse_full_credits(self, response):
        next_credit = [a.attrib["href"] for a in response.css("td.primary_photo a")]
        #next_credit = response.css("table.cast_list tr")[1:]

        for credit in next_credit:
            if credit:
                next_link = response.urljoin(credit)
            
                yield scrapy.Request(next_link, callback = self.parse_actor_page)
    
    def parse_actor_page(self, response):
        name_box = response.css("h1.header")
        actor_name = name_box.css("span.itemprop::text").get()
        
        for film in response.css("div.filmo-category-section b"):

            movie_or_TV_name = film.css("::text").get()

            if movie_or_TV_name:
                yield {
                    "actor" : actor_name, 
                    "movie_or_TV_name" : movie_or_TV_name
                }

        
# to run
# scrapy crawl imdb_spider -o movies.csv

import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'

    start_urls = ['https://www.imdb.com/title/tt2467372/?ref_=fn_al_tt_1']

    def parse(self, response):
        """
        This function assumes it starts on the IMDB home page of a movie or TV show and then
        navigates to the "Cast and Crew" IMDB page. When it arrives at this page, the function 
        calls parse_full_credits(self, response). This function does not return any data.
        """
        
        #finds the "Cast and Crew" link on the home page
        next_page = response.css("div.SubNav__SubNavContent-sc-11106ua-3.cKmYsV").css("li.ipc-inline-list__item a")[0].attrib["href"]

        if next_page:
            cast_page = response.urljoin(next_page)
            
            #follows the link to Cast and Crew page; calls parse_full_credits 
            yield scrapy.Request(cast_page, callback = self.parse_full_credits)

    
    def parse_full_credits(self, response):
        """
        This function assumes it starts on the "Cast and Crew" IMDB page for a given movie
        or TV show. It yields a scrapy.Request for each actor listed on the page and 
        calls parse_actor_page(self, response). This function does not return any data.
        """
        
        #creates a list of relative paths for each actor
        next_credit = [a.attrib["href"] for a in response.css("td.primary_photo a")]

        #loop through an iterable of actors
        for credit in next_credit:
            if credit:
                next_link = response.urljoin(credit)
                
                #follows the link to actor's actor page; calls parse_actor_page
                yield scrapy.Request(next_link, callback = self.parse_actor_page)
    
    def parse_actor_page(self, response):
        """
        This function assumes it starts on the IMDB page of an actor. It gets the name 
        of the actor and the names of the films and/or tv shows the actor has been in.
        The function yields this information in the form of a dictionary.
        """

        #get actor's name from the header of IMDB page
        name_box = response.css("h1.header")
        actor_name = name_box.css("span.itemprop::text").get()
        
        #loop through an iterable of films and TV shows
        for film in response.css("div.filmo-category-section b"):

            #get name of film or TV show actor was in
            movie_or_TV_name = film.css("::text").get()

            #dictionary with the name of the actor and the film/TV show they were in
            ## as key value pairs
            if movie_or_TV_name:
                yield {
                    "actor" : actor_name, 
                    "movie_or_TV_name" : movie_or_TV_name
                }

        
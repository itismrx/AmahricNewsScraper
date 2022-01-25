import scrapy 
from scrapy.http.request import Request

class AddisMaledaSpider(scrapy.Spider):
    name = 'addismaleda'

    start_urls= [
        'https://addismaleda.com/archives/category/zena/yeletzena',
        'https://addismaleda.com/archives/category/zena/tenetane',
        'https://addismaleda.com/archives/category/amdoch/metanie-habet',
        'https://addismaleda.com/archives/category/amdoch/mahebere-poleteica',
        'https://addismaleda.com/archives/category/art-and-life/heywetna-tibebe'
    ]

    def parse(self,response):
        links = response.css('div>header.news-list-header>h2.entry-title>a::attr(href)').getall() 
        for link in links:
            yield Request(link,self.articleExtractor)

        next_page = response.css('a.next.page-numbers::attr(href)').get() 

        if next_page is not None:
            yield response.follow(next_page,callback = self.parse)


    def articleExtractor(self,response):
        headline = response.css('header>h1.entry-title::text').get()        
        date = response.css('time::text').get()  
        views= response.css('div.single-post-social>div.single-post-view-count::text').get()[7:] 
        category = response.css('a.post-category-link::text').get()   
        article =  response.css('div.entry-content>p::text,div.entry-content>p>em>strong::text,div.single-post-content>div.entry-content>div>div::text').getall() 
        link = response.request.url

        yield {
            'headline' : headline,
            'category' : 'መዝናኛ',
            'date' : date,
            'views': views,
            'article' : article,
            'link' :link
        }



    
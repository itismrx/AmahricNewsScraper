import scrapy
from scrapy.http.request import Request

class BBCSpider(scrapy.Spider):
    name = 'soccer'
    start_urls= [
        "https://soccerethiopia.net/football/category/news-2/"
    ]

    def parse(self,response):
        links = response.css('h2.entry-title>a::attr(href)').getall()
        for link in links:

            yield Request(link,callback=self.articleExtractor)

        next_page = response.css('div.nav-links>a.next.page-numbers::attr(href)').get()   

        if next_page is not None:
            yield response.follow(next_page,callback = self.parse)


    def articleExtractor(self,response):
        yield{
            'headline' : response.css('div.entry-header>h1.entry-title::text').get(),
            'category' : 'ስፖርት',
            'date' : response.css('time::text').get(),
            'views': 'Unknown',
            'article' : response.css('div.entry-content>div.entry-the-content>p::text,div.entry-content>div.entry-the-content>p>i::text,div.entry-content>div.entry-the-content>p>b::text').getall(),
            'link' : response.request.url
        }
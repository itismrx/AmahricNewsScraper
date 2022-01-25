import scrapy
from scrapy.http.request import Request

class PressSpider(scrapy.Spider):
    name = 'press'
    start_urls= [
        'https://www.press.et/Ama/?cat=8',
        'https://www.press.et/Ama/?cat=14',
        'https://www.press.et/Ama/?cat=7',
        'https://www.press.et/Ama/?cat=18',
        'https://www.press.et/Ama/?cat=28'
    ]
    
    def parse(self,response):
        links = response.css('h3.entry-title.td-module-title>a::attr(href)').getall() 
        category =response.css('h1.entry-title.td-page-title::text').get() 
        for link in links:
            yield Request(link,callback=self.articleExtractor,meta={'category':category})

        next_page = response.css('div.page-nav>a::attr(href)').getall()[-1] 

        if next_page is not None:
            yield response.follow(next_page,callback = self.parse)


    def articleExtractor(self,response):
        yield {
            'headline' :  response.css('header.td-post-title>h1.entry-title::text').get(),
            'category' : response.meta['category'],
            'date' :  response.css('time.entry-date::text').get(),
            'views':  response.css('div.td-post-views>span::text').get(),
            'article' : response.css('div.td-post-content>p::text').getall()  ,
            'link' : response.request.url
        }
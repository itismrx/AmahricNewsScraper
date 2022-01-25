import scrapy
from scrapy.http.request import Request

class ReporterCrawler(scrapy.Spider):

    name = 'reporter'

    start_urls = ['https://www.ethiopianreporter.com/zena?page=1']

    def parse(self,response):
        links = response.css('div.post-block>div.post-content>h3.post-title>a::attr(href)').getall() 
        for link in links:
            link = 'https://www.ethiopianreporter.com' + link   

            yield Request(link,self.articlePicker)

        next_page = 'https://www.ethiopianreporter.com/zena'+response.css('li.pager__item.pager__item--next>a::attr(href)').get() 
        if next_page is not None:
            yield response.follow(next_page,self.parse)

    def  articlePicker(self,response):
        category = response.css('div>span.post-categories>a::text').get()
        headline = response.css('div>h1.post-title>span::text').get()  
        date = response.css('div.post-meta>span.post-created::text').get()  
        article = response.css('div.node__content>div.field.field--name-body span::text').getall()    
        if article == []:
            article = response.css('div.node__content p::text').getall()   
        link = response.request.url

        yield{
            'headline':headline,
            'category':category,
            'view' : 'Unknown',
            'date' : date,
            'article':article,
            'link' : link
        }

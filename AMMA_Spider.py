import scrapy
from scrapy.http.request import Request

class AmmaSpider(scrapy.Spider):
    name = 'amma'
    
    
    allowed_domians = ['https://www.amharaweb.com/']

    start_urls = [
        'https://www.amharaweb.com/category/%e1%8b%9c%e1%8a%93/',
        'https://www.amharaweb.com/category/sport/',
        'https://www.amharaweb.com/category/entertainment/'
        ]

    def parse(self,response):
        links =  response.css('div.td-ss-main-content>div div.td_module_1>h3.entry-title.td-module-title>a::attr(href)').getall()
        for link in  links:
            yield scrapy.Request(link,callback=self.articlePicker)
    
        next_page = response.css('div.page-nav>a::attr(href)')[-1].get() 
        
        if next_page is not None:
            
            yield response.follow(next_page,callback=self.parse)
    
    def articlePicker(self,response):
        category = response.css('ul.td-category>li.entry-category>a::text').getall() 
        date = response.css('header.td-post-title>div.td-module-meta-info>span.td-post-date>time::text').get() 
        view = response.css('header.td-post-title>div.td-module-meta-info>div.td-post-views>span::text').get()      
        headline = response.css('header.td-post-title>h1.entry-title::text').get()
        article = response.css('div.oygrvhab.hcukyx3x.c1et5uql.ii04i59q>div::text, div.td-post-content p::text,div.td-post-content>div>div>span::text').getall() 
        
        yield {
            'headline' : headline,
            'category' : category,
            'view' : view,
            'date' : date,
            'article' : article,
            'link'  : response.request.url
        }


       
import scrapy 
from scrapy.http.request import Request

class WaltaSpider(scrapy.Spider):
    name = 'walta'

    start_urls= [
        "https://waltainfo.com/am/category/ዜና/page/1/"

    ]

    def parse(self,response):
        # time.sleep(2)
        links = response.css('div.col-sm-6.post-col>div.post>header.entry-header>h2.entry-title>a::attr(href)').getall()
        for link in links:
            yield Request(link,self.articleExtractor)

        next_page = response.css('div.nav-links a.next::attr(href)').get()  

        if next_page is not None:
            yield response.follow(next_page,callback = self.parse)


    def articleExtractor(self,response):
        headline = response.css('header.entry-header>h1.entry-title::text').get()
        date = response.css('div.entry-meta>div.date>a::text').get() 
        views= 'Unknown'
        category = response.css('ul.trail-items>li>a>span::text')[2:].getall() 
        article = response.css('div.entry-content>p::text').getall() 
        link = response.request.url

        yield {
            'headline' : headline,
            'category' : category,
            'date' : date,
            'views': views,
            'article' : article,
            'link' :link
        }



    
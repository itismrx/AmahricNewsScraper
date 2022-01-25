import scrapy 
from scrapy.http.request import Request

class Al_Ain_Spider(scrapy.Spider):
    name = 'alain'

    start_urls= [
        'https://am.al-ain.com/infographics/page-1.html'
    ]

    def parse(self,response):
        # time.sleep(2)
        links = response.css('h2.card-title>a::attr(href)').getall()
        for link in links:
            yield Request(link,self.articleExtractor)

        next_page = 'https://am.al-ain.com'+response.css('div.row>div.col-12.mainbtn>a.btn::attr(href)').get() 

        if next_page is not None:
            yield response.follow(next_page,callback = self.parse)


    def articleExtractor(self,response):
        headline = response.css('div>h2.subtitle::text').get()  
        date = response.css('time::text').get() 
        views= 'Unknown'
        category = response.css('div>span>a::text').get() 
        article =response.css('div.details>p::text').getall()  
        link = response.request.url

        yield {
            'headline' : headline,
            'category' : category,
            'date' : date,
            'views': views,
            'article' : article,
            'link' :link
        }



    
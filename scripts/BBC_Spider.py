import scrapy
from scrapy.http.request import Request

class BBCSpider(scrapy.Spider):
    name = 'bbc'
    start_urls= [
        'https://www.bbc.com/amharic/topics/c7zp57r92v5t',
        'https://www.bbc.com/amharic/topics/c6vzykjwggkt'
    ]

    def parse(self,response):
        links = response.css('a.qa-story-image-link::attr(href)').getall()   
        for link in links:
            link = 'https://www.bbc.com' + link

            yield Request(link,callback=self.articleExtractor)

        next_page = response.css('a.qa-pagination-next-page::attr(href)').get()  

        if next_page is not None:
            next_page = 'https://www.bbc.com' + next_page
            yield response.follow(next_page,callback = self.parse)


    def articleExtractor(self,response):
        yield{
            'headline' : response.css('h1.css-1al79w4-Headline.e1yj3cbb0::text').get(),
            'category' : 'መዝናኛ',
            'date' : response.css('time::text').get(),
            'views': 'Unknown',
            'article' : response.css('div.css-oywjep-GridComponent.e57qer20>p>b::text').getall() + response.css('div.css-oywjep-GridComponent.e57qer20>p::text').getall() , 
            'link' : response.request.url
        }
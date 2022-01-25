import scrapy
from scrapy.http.request import Request

class AddisAdmas(scrapy.Spider):
    name = 'addisadmas'
    start_urls= [
        'https://www.addisadmassnews.com/index.php?option=com_k2&view=itemlist&layout=category&task=category&id=14&Itemid=211'
    ]

    def parse(self,response):
        links = response.css('div.catItemHeader>h3.catItemTitle>a::attr(href)').getall() 
        category = response.css('div.itemListCategory>h2::text').get()   
        for link in links:
            link = 'https://www.addisadmassnews.com' + link

            yield Request(link,callback=self.articleExtractor,meta={'category':category})

        next_page = 'https://www.addisadmassnews.com' + response.css('a.next::attr(href)').get() 

        if next_page is not None:
            
            yield response.follow(next_page,callback = self.parse)


    def articleExtractor(self,response):
        yield{
            'headline' : response.css('h2.itemTitle::text').get()    ,
            'category' : response.meta['category'],
            'date' : response.css('span.itemDateCreated::text').get() ,
            'views': response.css('span.itemHits>b::text').get(),
            'article' : response.css('div.itemFullText>p::text').getall()    ,
            'link' : response.request.url
        }
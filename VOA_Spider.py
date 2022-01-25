import scrapy 

class VoaSpider(scrapy.Spider):
    name = 'voa'

    start_urls = [
        'https://amharic.voanews.com/z/3169',
        'https://amharic.voanews.com/z/3737',
        'https://amharic.voanews.com/z/3661'
    ]

    def parse(self,response):
        links = response.css('div.media-block-wrap>div.row>ul>li>div.media-block>a::attr(href)').getall()    
        for link in links:
            link = 'https://amharic.voanews.com/' + link
            yield scrapy.Request(link,callback=self.articleExtractor)

        next_page = 'https://amharic.voanews.com/' + response.css('div.media-block-wrap>p.btn--load-more>a.btn.link-showMore::attr(href)').get()  
        
        if next_page is not None:
            yield response.follow(next_page,callback = self.parse)


    def articleExtractor(self,response):
        date = response.css('div.published>span.date>time::text').get()[1:-1] 
        article =  response.css('div.content-floated-wrap>div.wsw>p::text').getall() 
        headline = response.css('h1.title.pg-title::text').get()[1:-1] 
        category = 'World News'
        link = response.request.url
        views = "Unknown"
        yield{
            'headline' : headline,
            'category' : category,
            'date' : date,
            'views' : views,
            'article' : article,
            'link' : link

        } 
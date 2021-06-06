import scrapy
import datetime
import re

class ClarinSpider(scrapy.Spider):
    name ='Clarin'
    start_urls = [
        'https://www.clarin.com/ultimo-momento/',
        'https://www.clarin.com/economia/',
        'https://www.clarin.com/politica/',
        'https://www.clarin.com/mundo/',
        'https://www.clarin.com/deportes/',
        'https://www.clarin.com/opinion/',

    ]
    custom_settings = {
        #'FEED_URI': 'clarin.json',
        'FEED_FORMAT': 'json',
        'MEMUSAGE_LIMIT_MB': 2048,
        'MEMUSAGE_NOTIFY_MAIL': ['sistemastesis10@gmail.com'],
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'NicolePirca',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse(self,response):
        
        links_to_notices =response.xpath('//div[@class="box-notas"]//a/@href').getall()  
        print(links_to_notices)
        for link in links_to_notices:
            yield response.follow(link, callback= self.parse_link, cb_kwargs= {'url':response.urljoin(link)})
    
    def parse_link(self, response, **kwargs):

        link = kwargs['url']
        title = response.xpath('//div[@class="title"]//h1[@id="title"]/text()').get()
        paragraph = response.xpath('//div[@itemprop="description"]//h2/text()').get()
        fecha = response.xpath('//div[@class="breadcrumb col-lg-6 col-md-12 col-sm-12 col-xs-12"]//span/text()').get()
        noticia = response.xpath('//div[@class="body-nota"]//p//../text()').getall()
        dateSplit=fecha.split(' ')
        yield {
            'social': 'El Clarin',
            'title': title,
            'descripcion': paragraph,
            'fecha': dateSplit[0],
            'link': link,
            'calificacion': '',
            'noticia': ''.join(noticia)
        }
   
       #with open('resultados.html','w',encoding='utf-8') as f:
           # f.write(response.text)

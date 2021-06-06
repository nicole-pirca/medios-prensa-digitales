import scrapy
import datetime
import re

class ComercioSpider(scrapy.Spider):
    name ='Comercio'
    start_urls = [
        'https://elcomercio.pe/mundo/',
        'https://elcomercio.pe/economia/',
        'https://elcomercio.pe/politica/',
        'https://elcomercio.pe/lima/',
        'https://elcomercio.pe/ultimas-noticias/',
        'https://elcomercio.pe/opinion/',
        'https://elcomercio.pe/peru/'
        
    ]
    custom_settings = {
        #'FEED_URI': 'comercio.json',
        'FEED_FORMAT': 'json',
        'MEMUSAGE_LIMIT_MB': 2048,
        'MEMUSAGE_NOTIFY_MAIL': ['sistemastesis10@gmail.com'],
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'CarolOna',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse(self,response):
        
        links_to_notices =response.xpath('//h2[@class="story-item__content-title overflow-hidden"]//a//@href').getall()
        print(links_to_notices)
        for link in links_to_notices:
            yield response.follow(link, callback= self.parse_link, cb_kwargs= {'url':response.urljoin(link)})
    
    def parse_link(self, response, **kwargs):
   
        link = kwargs['url']
        title = response.xpath('//h1[@class="sht__title"]/text()').get()
        paragraph = response.xpath('//h2[@class="sht__summary"]/text()').get()
        fecha = response.xpath('//div[@class="story-contents__author-date f  story-contents__author-top "]//time[@datetime]/text()')[1].get()
        noticia = response.xpath('//div[@class="story-contents__content  "]//p[@class="story-contents__font-paragraph "]//../text()').getall()
        sin_actualizado = re.sub('(\W|^)Actualizado\sel(\W|$)', '',fecha)
        sinpalabras= re.sub('(?i)(\W|^)(a.m|p.m)(\W|$)','',sin_actualizado)
        dateSplit=sinpalabras.split(' ')
        yield {     
            'social': 'El Comercio',
            'title': title,
            'descripcion': paragraph,
            'fecha' : dateSplit[0],
            'link': link,
            'calificacion': '',
            'noticia': ''.join(noticia)
        }
   

       #with open('resultados.html','w',encoding='utf-8') as f:
           # f.write(response.text)

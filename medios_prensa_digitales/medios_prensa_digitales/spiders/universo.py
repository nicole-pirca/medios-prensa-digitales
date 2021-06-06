import scrapy
import datetime
import re

class UniversoSpider(scrapy.Spider):
    name ='Universo'
    start_urls = [
        'https://www.eluniverso.com/noticias/politica/',
        'https://www.eluniverso.com/ultimas-noticias/',
        'https://www.eluniverso.com/opinion/',
        'https://www.eluniverso.com/deportes/',
        'https://www.eluniverso.com/noticias/economia/',
        'https://www.eluniverso.com/noticias/internacional/',
        'https://www.eluniverso.com/noticias/ecuador/'
    ]
    custom_settings = {
        #'FEED_URI': 'universo.json',
        'FEED_FORMAT': 'json',
        'MEMUSAGE_LIMIT_MB': 2048,
        'MEMUSAGE_NOTIFY_MAIL': ['sistemastesis10@gmail.com'],
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'CarolOna',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse(self,response):
        
        links_to_notices =response.xpath('//h2[@class="text-lg m-0 font-bold font-primary"]//@href').getall()
        print(links_to_notices)
        for link in links_to_notices:
            yield response.follow(link, callback= self.parse_link, cb_kwargs= {'url':response.urljoin(link)})
    
    def parse_link(self, response, **kwargs):
        today = datetime.date.today().strftime('%d-%m-%Y')
        link = kwargs['url']
        title = response.xpath('//h1[@class="text-lg md:text-2xl lg:text-3xl font-bold font-primary"]/text()').get()
        paragraph = response.xpath('//section[@class="px-2"]//div[@class="region region-content | grid grid-cols-12 col-span-12 lg:col-span-8 auto-rows-max"]//p/text()').get()
        fecha = response.xpath('//section[@class="px-2"]//div[@class="byline | font-secondary text-xs text-grey-700 flex space-x-1 divide-x"]//p[@class="date | flex items-center font-secondary text-xs text-grey-700 dark:text-silver-300 m-0"]//time/text()').get()
        noticia = response.xpath('//section[@class="article-body prose prose-sm sm:prose mx-auto space-y-3 font-primary"]//p[@class="prose-text"]//../text()').getall()
        dateSplit=fecha.split(' ')
        day= dateSplit[0]
        month_sin_coma= dateSplit[2].replace(",", "")
        month= getmonth(month_sin_coma)
        year=dateSplit[3]
        fullDate=day+'/'+month+'/'+year

        yield {
            
            'social': 'El Universo',
            'title': title,
            'descripcion': paragraph,
            'fecha': fullDate,
            'link': link,
            'calificacion': '',
            'noticia': ''.join(noticia)
        }
def getmonth(month):

    if month == 'enero':
        return'01'
    elif month == 'febrero':
        return'02'
    elif month == 'marzo':
        return'03'
    elif month == 'abril':
        return'04'
    elif month == 'mayo':
        return'05'
    elif month == 'junio':
        return'06'
    elif month == 'julio':
        return'07'
    elif month == 'agosto':
        return'08'
    elif month == 'septiembre':
        return'09'
    elif month == 'octubre':
        return'10'
    elif month == 'noviembre':
        return'11'
    elif month == 'diciembre':
        return'12'
    else:
        return'no es un mes'
       #with open('resultados.html','w',encoding='utf-8') as f:
           # f.write(response.text)

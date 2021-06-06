import scrapy
import datetime


class UniversalSpider(scrapy.Spider):
    name ='Universal'
    start_urls = [
        'https://www.eluniversal.com.mx/mundo',
        'https://www.eluniversal.com.mx/nacion',
        'https://www.eluniversal.com.mx/metropoli',
        'https://www.eluniversal.com.mx/estados',
        'https://www.eluniversal.com.mx/opinion',
        'https://www.eluniversal.com.mx/cartera',
        'https://www.eluniversal.com.mx/espectaculos',
        'https://www.eluniversal.com.mx/cultura',
        'https://www.eluniversal.com.mx/ciencia-y-salud',
        'https://www.eluniversal.com.mx/minuto-x-minuto',     
    ]
    custom_settings = {
        #'FEED_URI': 'universal.json',
        'FEED_FORMAT': 'json',
        'MEMUSAGE_LIMIT_MB': 2048,
        'MEMUSAGE_NOTIFY_MAIL': ['sistemastesis10@gmail.com'],
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'NicolePirca',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse(self,response):
        
        links_to_notices =response.xpath('//h2[@class="ce3-Tipo1_Titulo "]//a//@href').getall()
        print(links_to_notices)
        for link in links_to_notices:
            yield response.follow(link, callback= self.parse_link, cb_kwargs= {'url':response.urljoin(link)})
    
    def parse_link(self, response, **kwargs):
        today = datetime.date.today().strftime('%d-%m-%Y')
        link = kwargs['url']
        title = response.xpath('//h1[@class="h1 "]/text()').get()
        paragraph = response.xpath('//h2[@class="h2"]/text()').get()
        fecha = response.xpath('//span[@class ="ce12-DatosArticulo_ElementoFecha"]/text()').get()
        noticia = response.xpath('//div[@class="field field-name-body field-type-text-with-summary field-label-hidden"]//p//../text()').getall()
        yield {
            'social': 'El Universal',
            'title': title,
            'descripcion': paragraph,
            'fecha': fecha,
            'link': link,
            'calificacion': '',
            'noticia': ''.join(noticia)
        }
   
       #with open('resultados.html','w',encoding='utf-8') as f:
           # f.write(response.text)

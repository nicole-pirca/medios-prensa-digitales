import scrapy
import datetime

class TiempoSpider(scrapy.Spider):
    name ='Tiempo'
    #10 items    
    start_urls = [
        'https://www.eltiempo.com/mundo',
        'https://www.eltiempo.com/cultura',
      #  'https://www.eltiempo.com/tecnosfera',
        'https://www.eltiempo.com/vida',
        'https://www.eltiempo.com/salud',
      #  'https://www.eltiempo.com/deportes',
        'https://www.eltiempo.com/economia'
        'https://www.eltiempo.com/justicia',
        'https://www.eltiempo.com/bogota',
        'https://www.eltiempo.com/colombia'
    ]
    custom_settings = {
        #'FEED_URI': 'tiempo.json',
        'FEED_FORMAT': 'json',
        'MEMUSAGE_LIMIT_MB': 2048,
        'MEMUSAGE_NOTIFY_MAIL': ['sistemastesis10@gmail.com'],
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'Carol',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse(self,response):
        
        links_to_notices =response.xpath('//article[@class="content_grid home-seccion"]//meta/@itemid').getall() 
        for link in links_to_notices:
            yield response.follow(link, callback= self.parse_link, cb_kwargs= {'url':response.urljoin(link)})
    
    def parse_link(self, response, **kwargs):
        today = datetime.date.today().strftime('%d-%m-%Y')
        link = kwargs['url']
        title = response.xpath('//div[@class="titulo-principal-bk"]//h1[@class="titulo"]/text()').get()
        paragraph = response.xpath('//div[@class="epigraph-container lead"]//p/text()').get()
        noticia = response.xpath('//div[@class="modulos public-side"]//p[@class="contenido"]//../text()').getall()
        fecha = response.xpath('//div[@class="articulo-autor autor-container "]//div[@class="img_info h-seccion"]//div[@class="author_data"]//span[@class="publishedAt"]/text()').get()
        dateSplit=fecha.split(' ')
        day= dateSplit[0]
        month= getmonth(dateSplit[2])
        year=dateSplit[3]
        year_sincoma= year.replace(",", "")
        fullDate=day+'/'+month+'/'+year_sincoma

        yield {
            'social': 'El Tiempo',
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
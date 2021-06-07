# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MediosPrensaDigitalesItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    descripcion = scrapy.Field()
    fecha = scrapy.Field()
    link = scrapy.Field()
    calificacion = scrapy.Field()
    noticia = scrapy.Field()
    pass

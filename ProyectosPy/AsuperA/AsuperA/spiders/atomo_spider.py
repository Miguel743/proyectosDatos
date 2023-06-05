# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 23:00:48 2023

@author: Miguel_Perez_Diaz
"""
import scrapy
from scrapy.loader.processors import MapCompose
from datetime import datetime as dt_dt


class ArticulosAtomo(scrapy.Spider):

    name = "articulosAtomo"

    start_urls = [
        "https://atomoconviene.com/atomo-ecommerce/3-almacen",
        "https://atomoconviene.com/atomo-ecommerce/85-limpieza",
        "https://atomoconviene.com/atomo-ecommerce/83-perfumeria",
        "https://atomoconviene.com/atomo-ecommerce/833-ofertas"
    ]

    def quitarPesos(self, texto):
        return texto.replace("$", "")

    def parse(self, response):

        articulos = response.xpath(
            '//div[@id="js-product-list"]//div[@class="product-description product__card-desc"]')
        for articulo in articulos:
            yield{
                'dia_hora_extraccion': dt_dt.now(),
                'descripcion': articulo.xpath('./h2/a/text()').get(),
                'precio': articulo.xpath('./div[1]/span[2]/text()').get(),
                'categoria': response.url.split("/")[-1]

            }

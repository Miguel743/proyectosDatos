# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 11:36:23 2023

@author: Miguel_Perez_Diaz
"""
import scrapy
from datetime import datetime as dt_dt


class ArticulosSuperA(scrapy.Spider):

    name = "articulosSuperA"

    start_urls = [
        "https://supera.com.ar/categoria-producto/almacen/",
        "https://supera.com.ar/categoria-producto/limpieza/",
        "https://supera.com.ar/categoria-producto/perfumeria/",
        "https://supera.com.ar/ofertas/",
    ]

    def parse(self, response):

        articulos = response.xpath(
            '//ul[@class="products elementor-grid columns-4"]/li')
        for articulo in articulos:
            yield{
                'timestamp': dt_dt.now(),
                'descripcion': articulo.xpath('./a/h2/text()').get(),
                'precio': articulo.xpath('./a/span[@class="price"]/span/bdi/text()').get(),
                'categoria': response.url.split("/")[-2]

            }

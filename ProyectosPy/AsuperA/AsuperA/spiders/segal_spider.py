# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 23:46:48 2023

@author: Miguel_Perez_Diaz
"""
import scrapy
from datetime import datetime as dt_dt


class ArticulosSegal(scrapy.Spider):

    name = "articulosSegal"

    start_urls = [
        "https://www.casa-segal.com/categoria-producto/almacen/",
        "https://www.casa-segal.com/categoria-producto/limpieza/",
        "https://www.casa-segal.com/categoria-producto/perfumeria/"
    ]

    def parse(self, response):

        articulos = response.xpath(
            '//div[@id="primary"]//ul[contains(@class,"products products-container")]/li//div[@class="product-content"]')
        for articulo in articulos:
            yield{
                'dia_hora_extraccion': dt_dt.now(),
                'descripcion': articulo.xpath('./a/h3/text()').get(),
                'precio': articulo.xpath('./span[@class="price"]//bdi/text()').get(),
                'categoria': response.url.split("/")[-2]

            }

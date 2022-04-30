from scrapy.shell import inspect_response
from typing import List
import scrapy


class ProperatiSpider(scrapy.Spider):
    name = 'properati'
    allowed_domains = ['www.properati.com.ar']
    start_urls = ['https://www.properati.com.ar/s/capital-federal/departamento/alquiler']
    base_url = 'https://www.properati.com.ar'
    page = 1

    def get_images(self,response,*args, **kwargs):
        image_list =response.xpath('//img[contains(@src,"http")]//@src').getall()[:-1]
        yield {
            'images':image_list,
            **kwargs
        }

    def parse(self, response):
        #The pages doesnt give any clue about if a next page exist, so we calculated based on the max result.
        #I know this is not the best solution but, this page is kinda tricky
        results = response.xpath('//div[@class="sc-ciSkZP eFbreg page-counter"]//text()').get()
        results_number = int(results.split()[4])
        self.max_page = (results_number//30)+1

        for item in response.xpath('//div[@class="CardWrapper-sc-6ce7as-12 comlbB"]'):
            url = f'{self.base_url}{item.xpath(".//a//@href").get()}'
            
            price =  item.xpath('.//span[@class="sc-pNWdM hQvubf"]//text()').extract()
            price = ''.join(price)
            
            expenses = item.xpath('.//span[@class="StyledMaintenanceFees-sc-6ce7as-6 bVeCwP"]//text()').extract()
            expenses = ''.join(expenses[0:5:2])

            location = item.xpath('.//span[@class="StyledLocation-sc-6ce7as-7 dxIVBd"]//text()').get()
            address = item.xpath('.//h2//text()').get()

            extras = item.xpath('.//div[@class="StyledInfoIcons-sc-6ce7as-9 kbmWJE"]//span//text()').extract()

            info = {
                'price':price,
                'url':url,
                'expenses':expenses,
                'location':location,
                'address':address,
                'extras':extras
            }
            yield scrapy.Request(url,self.get_images,cb_kwargs=info)

        if self.page<= self.max_page:
            self.page +=1
            yield response.follow(f'{self.start_urls[0]}?page={self.page}', self.parse)



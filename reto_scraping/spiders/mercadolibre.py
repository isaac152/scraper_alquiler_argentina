from scrapy.shell import inspect_response
import scrapy


class MercadolibreSpider(scrapy.Spider):
    name = 'mercadolibre'
    allowed_domains = ['inmuebles.mercadolibre.com.ar']
    start_urls = ['https://inmuebles.mercadolibre.com.ar/departamentos/alquiler/capital-federal/']

    #Descomentar para mas exactitud. [Tardará mucho más]
    #custom_settings = {
    #    'DOWNLOAD_DELAY':4,
    #    'RETRY_HTTP_CODES':[403],
    #    'RETRY_TIMES':5,
    #    'CONCURRENT_REQUESTS_PER_DOMAIN':4
    #}

    def parse_item(self,response):        
        self.logger.info(response.url)
        images_urls=response.xpath('//figure/img/@data-src').extract()
        price = response.xpath('//div[@class="ui-pdp-price__second-line"]//text()').get()
        expenses=response.xpath('//tr//text()[contains(.,"ARS")]').get()
        extras =response.xpath('//div[@class="ui-pdp-highlighted-specs-res"]//text()').extract()
        extras = [extra.strip() for extra in extras if extra.strip()!='']
        location = response.xpath('//li[@class="andes-breadcrumb__item"]//text()').extract()
        location = ', '.join(location[-2:])
        address = response.xpath('//figure/following-sibling::div[@class="ui-pdp-media__body"]/p//text()').get()
        yield {
                'images':images_urls,
                'price':price,
                'url':response.url,
                'expenses':expenses,
                'location':location,
                'address':address,
                'extras':extras
            }


    def parse(self, response):
        for item in response.xpath('//li[@class="ui-search-layout__item"]'):
            url = item.xpath('.//a/@href').get()
            yield scrapy.Request(url=url,callback=self.parse_item,dont_filter=True)   
    
        next_page = response.xpath('//a[@title="Siguiente"]/@href').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
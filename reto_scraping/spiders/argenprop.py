import scrapy

class ArgenPropSpider(scrapy.Spider):
    name = 'argenprop'
    allowed_domains = ['argenprop.com']
    start_urls = ['https://www.argenprop.com/departamento-alquiler-localidad-capital-federal']
    base_url = 'https://www.argenprop.com'

    def parse(self, response):
        for item in response.xpath('//div[@class="listing__item "]'):
            image_list = item.xpath('.//div/ul[@class="card__photos"]/li/img[contains(@data-src,"http")]/@data-src').extract()
            url = f'{self.base_url}{item.xpath("a//@href").get()}'
            price =item.xpath('.//p[@class="card__price"]//text()').extract()
            price = ''.join([p.strip() for p in price[1:]])
            expenses =item.xpath('.//p[@class="card__expenses"]//@title').get()
            address=item.xpath('normalize-space(.//h2//text())').get()
            location = item.xpath('.//p[@class="card__title--primary"]//text()').get()
            extras = item.xpath('.//ul[@class="card__main-features"]/li/span/text()').extract()
            extras = [extra.strip() for extra in extras]
            yield {
                'images':image_list,
                'price':price,
                'url':url,
                'expenses':expenses,
                'location':location,
                'address':address,
                'extras':extras
            }
        next_page =response.xpath("//a[@rel='next']/@href").get()
        if next_page is not None:
            yield response.follow(self.base_url+next_page, self.parse)

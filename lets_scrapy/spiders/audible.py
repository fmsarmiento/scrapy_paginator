import scrapy


class AudibleSpider(scrapy.Spider):
    name = 'audible'
    allowed_domains = ['www.audible.com']
    # start_urls = ['http://www.audible.com/search']

    def start_requests(self):
        yield scrapy.Request(url='http://www.audible.com/search', callback=self.parse, headers= {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'})

    def parse(self, response):
        #1. Get xpath of the container
        product_container = response.xpath("//div[@class='adbl-impression-container ']/li")
        #2. For each container, get the title, author and length
        for product in product_container:
            book_title = product.xpath('.//h3[contains(@class,"bc-heading")]/a/text()').get()
            book_author = product.xpath('.//li[contains(@class,"authorLabel")]/span/a/text()').getall()
            book_length = product.xpath('.//li[contains(@class,"runtimeLabel")]/span/text()').get()
            # Return the output to scrapy
            yield {
                'title':book_title,
                'author':book_author,
                'length':book_length,
                # 'User-Agent':response.request.headers['User-Agent'],
            }
        # Get container for pagination, then get the next button
        pagination = response.xpath('//ul[contains(@class,"pagingElements")]')
        next_page_url = response.xpath('.//span[contains(@class,"nextButton")]/a/@href').get()
        # If there is a next page, go to it, then proceed to do parse again
        if next_page_url:
            yield response.follow(url=next_page_url, callback=self.parse, headers= {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'})
        else:
            quit()
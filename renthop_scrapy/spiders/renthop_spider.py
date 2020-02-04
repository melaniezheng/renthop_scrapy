from scrapy import Spider, Request
from renthop_scrapy.items import RenthopItem
import re

class RenthopSpider(Spider):
    name = 'renthop_spider'
    allowed_domains = ['www.renthop.com']
    start_urls = ['https://www.renthop.com/search/nyc?min_price=0&max_price=7000&q=&sort=hopscore&search=0']

    def parse(self, response):
        # Find the total number of pages in the result so that we can decide how many urls to scrape next
        total_page = int(response.xpath('/html/body/div[4]/div[1]/div[1]/div[4]/div[2]/span[1]/text()[2]').extract()[0].split(' ')[2])

        # List comprehension to construct all the urls
        result_urls = [f'https://www.renthop.com/search/nyc?min_price=0&max_price=7000&q=&sort=hopscore&search=0&page={x}' for x in range(1,total_page)]
        # Yield the requests to different search result urls, 
        # using parse_result_page function to parse the response.
        for url in result_urls:
            print(f"URL: {url}")
            yield Request(url=url, callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        # find all listings
        try:
            listings = response.xpath('//div[@class="search-info pr-4 pl-4 pr-md-0 pl-md-4 py-2 py-md-0"]')
        except Exception as e:
            print(f"Error loading listings: {e}")
        for listing in listings:
            try:
                address = listing.xpath('.//a/text()').extract_first()
            except:
                address = ""
            try:
                neighborhood = listing.xpath('.//div[@class="font-size-9 overflow-ellipsis"]/text()').extract()[0].split(',')[0].strip()
            except:
                neighborhood = ""
            try:
                borough = listing.xpath('.//div[@class="font-size-9 overflow-ellipsis"]/text()').extract()[0].split(',')[-1].strip()
            except:
                borough = ""
            try:
                url = listing.xpath('./div[1]/a').extract_first().split('href=')[1].split('"')[1]
            except:
                url = ""
            try:
                price = listing.xpath('./div[2]//td[@class="font-size-11 b"][1]/text()').extract_first().strip()
            except:
                price = ""
            try:
                bedroom = listing.xpath('./div[2]//td[@class="font-size-11 b"][2]/span/text()').extract_first().strip().replace('\n',"")
            except:
                bedroom = ""
            try:
                bathroom = listing.xpath('./div[2]//td[@class="font-size-11 b"][3]/span/text()').extract_first().strip()
            except:
                bathroom = ""
            try:
                no_fee = listing.xpath('.//div[@class="font-size-9"]/div[1]/text()').extract_first().strip()
                if no_fee == "No Fee":
                    no_fee = True
            except:
                no_fee = ""
            
            item = RenthopItem()
            item['url'] = url
            item['address'] = address
            item['neighborhood'] = neighborhood
            item['borough'] = borough
            item['price'] = price
            item['bedroom'] = bedroom
            item['bathroom'] = bathroom
            item['no_fee'] = no_fee

            yield item
            
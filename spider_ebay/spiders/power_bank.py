import scrapy
from scrapy_selenium import SeleniumRequest

class PowerBankSpider(scrapy.Spider):
    name = "power_bank"
    allowed_domains = ["ebay.com"]
    page_limit = 10  # Limit to 10 pages
    current_page = 1  # Start on page 1

    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.ebay.com/sch/i.html?_nkw=camping+solar+power+bank&_sacat=0&_from=R40&_trksid=p2334524.m570.l1311",
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        # Extract product details
        products = response.xpath('//li[contains(@class, "s-item")]')
        for product in products:
            title = product.xpath('.//span[@role="heading" and @aria-level="3"]/text()').get()
            price = product.xpath('.//span[contains(@class, "s-item__price")]/text()').get()
            url = product.xpath('.//a[contains(@class, "s-item__link")]/@href').get()

            if title and price:
                yield {
                    'title': title.strip() if title else 'N/A',
                    'price': price.strip() if price else 'N/A',
                    'url': url.strip() if url else 'N/A'
                }

        # Check if we have reached the page limit
        if self.current_page < self.page_limit:
            # Handle pagination: look for the "Next" button and follow the next page link
            next_page = response.xpath('//a[@class="pagination__next"]/span/text()').get()
            if next_page and next_page.lower() == "next":
                next_page_url = response.urljoin(response.xpath('//a[@class="pagination__next"]/@href').get())
                self.current_page += 1
                yield SeleniumRequest(url=next_page_url, wait_time=5, callback=self.parse)

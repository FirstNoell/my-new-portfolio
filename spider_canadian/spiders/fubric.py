import scrapy
from scrapy_selenium import SeleniumRequest

class FubricSpider(scrapy.Spider):
    name = "fubric"
    allowed_domains = ["www.amazon.com"]
    start_urls = [
        "https://www.amazon.com/s?k=canadian+fabric+by+the+yard&crid=3KNRKJ4I5STKX&sprefix=canadian+fubric%2Caps%2C316&ref=nb_sb_ss_ts-doa-p_2_15"
    ]

    def start_requests(self):
        # Use SeleniumRequest to render JavaScript on the page
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=5,
                screenshot=False,  # Turn off screenshots if not needed
                dont_filter=True  # Don't filter requests for pagination
            )

    def parse(self, response):
        self.logger.info(f"Scraping URL: {response.url}")

        # Use XPath to extract product data from the page
        products = response.xpath('//div[contains(@class, "s-main-slot")]/div[contains(@class, "s-result-item")]')
        for product in products:
            title = product.xpath('.//h2//span/text()').get()
            price = product.xpath('.//span[contains(@class, "a-price-whole")]/text()').get()
            url = product.xpath('.//h2/a/@href').get()
            ratings = product.xpath('.//span[contains(@class, "a-icon-alt")]/text()').get()

            yield {
                'title': title.strip() if title else 'No Title',
                'price': price.strip() if price else 'Not Available',
                'url': response.urljoin(url) if url else 'No URL',
                'ratings': ratings.strip() if ratings else 'No Ratings'
            }

        # Handle pagination - extract the "Next" page URL using a generalized XPath
        next_page = response.xpath('//li[@class="s-pagination-item s-pagination-next"]/a/@href').get()
        if next_page:
            # Follow the next page URL and scrape it
            yield SeleniumRequest(
                url=response.urljoin(next_page),
                callback=self.parse,
                wait_time=5,
                dont_filter=True
            )

 eBay Solar Power Bank Scraper
 Overview
A Scrapy spider powered by Selenium that scrapes eBay listings for "camping solar power banks". It handles dynamic content and pagination, extracting essential product data across multiple pages.
 Tech Stack
•	Python, Scrapy, Scrapy-Selenium, XPath
 Key Features
•	Dynamic Rendering: Uses Selenium WebDriver to load JavaScript content fully.
•	Pagination: Follows the "Next" button automatically (up to 10 pages).
•	Data Cleaning: Uses .strip() to ensure consistent text formatting.
•	Error Handling: Skips entries missing a title or price for cleaner output.
 Output Sample
•	title — e.g., "Solar Charger 30000mAh Waterproof Power Bank"
•	price — e.g., "$29.99"
•	URL — Direct eBay product link
 Run the Spider

scrapy crawl power_bank -o power_bank_listings.json



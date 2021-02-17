import scrapy

from scrapy.loader import ItemLoader
from ..items import EurobankpbItem
from itemloaders.processors import TakeFirst


class EurobankpbSpider(scrapy.Spider):
	name = 'eurobankpb'
	start_urls = ['https://www.eurobankpb.lu/en/Media/NewsAndEvents#']

	def parse(self, response):
		post_links = response.xpath('//a[@class="promo-card__all-link"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="article__body"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//p[@class="article__date"]/text()').get()

		item = ItemLoader(item=EurobankpbItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()

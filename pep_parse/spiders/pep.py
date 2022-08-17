import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        pep_links = response.css(
            'section[id=numerical-index] tr td:nth-child(2) a::attr(href)'
        ).getall()

        for pep_link in pep_links:
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        number, name = response.css(
            'h1.page-title::text'
        ).get().split(' – ', 1)

        data = {
            'number': number.replace('PEP ', ''),
            'name': name,
            'status': response.css('dt:contains("Status") + dd::text').get()
        }

        yield PepParseItem(data)

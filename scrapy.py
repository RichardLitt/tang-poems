import scrapy


class AuthorSpider(scrapy.Spider):
    name = 'author'

    start_urls = [
        'http://www.chinese-poems.com/bo.html',
        'http://www.chinese-poems.com/du.html',
        'http://www.chinese-poems.com/dm.html',
        'http://www.chinese-poems.com/hy.html',
        'http://www.chinese-poems.com/lb.html',
        'http://www.chinese-poems.com/li.html',
        'http://www.chinese-poems.com/yu.html',
        'http://www.chinese-poems.com/lzy.html',
        'http://www.chinese-poems.com/myc.html',
        'http://www.chinese-poems.com/meng.html',
        'http://www.chinese-poems.com/oyx.html',
        'http://www.chinese-poems.com/su.html',
        'http://www.chinese-poems.com/tao.html',
        'http://www.chinese-poems.com/wang.html',
        'http://www.chinese-poems.com/others.html'
    ]

    def parse(self, response):
        # follow links to author pages
        for href in response.css('.author + a::attr(href)').extract():
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_author)

        # follow pagination links
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text'),
        }

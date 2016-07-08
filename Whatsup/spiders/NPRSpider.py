from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from datetime import datetime
from Whatsup.items import Article


class NPRSpider(CrawlSpider):
    name = "NPR"
    allowed_domains = ["npr.org"]
    today = datetime.today().strftime("%m-%d-%Y")
    start_urls = [
        'http://www.npr.org/sections/news/archive?date=%s' % today,
    ]
    rules = (
        Rule(LinkExtractor(allow=("/sections/*/",))),
        Rule(LinkExtractor(allow=('/\d+/\d+/\d+/\d+/*',)), callback='parse_item'),
    )

    def _get_first_element(self, css_selector_extracted, default=''):
        if len(css_selector_extracted) > 0:
            return css_selector_extracted[0]
        return default

    def parse_item(self, response):
        article = Article()
        article['title'] = self._get_first_element(response.css('article.story>.storytitle>h1::text').extract())
        article['url'] = response.url
        article['slug'] = self._get_first_element(response.css('article.story>h3.slug>a::text').extract())

        content = self._get_first_element(response.css('article.story>#storytext').extract())
        article['content'] = content

        article['image_urls'] = response.css(
            'article.story>#storytext>div.bucketwrap.image.large>.imagewrap>img::attr(src)').extract()

        article['date'] = self._get_first_element(
            response.css('article.story>#story-meta time::attr(datetime)').extract())

        article['audio'] = self._get_first_element(
            response.css('article.story>.story-tools>#primaryaudio>li.audio-tool-download>a::attr(href)').extract())
        return article

import scrapy
import datetime
import re
from vietnambiz.items import CompanyItem, CompanyProfileItem

class PeterParkerSpider(scrapy.Spider):
    name = "peter_parker"

    def start_requests(self):
        urls = ['http://www.vietnambiz.org/']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        crawled_at = datetime.datetime.now().strftime("%y-%m-%d")
        source = response.css('title ::text').extract_first()
        SET_SELECTOR = '.cathome'
        for item in response.css(SET_SELECTOR):
            INDUSTRY_SELECTOR = '::text'
            URL_SELECTOR = '::attr(href)'
            url = item.css(URL_SELECTOR).extract_first()
            company = CompanyItem()

            company['source'] = source
            company['industry'] = item.css(INDUSTRY_SELECTOR).extract_first()
            company['url'] = url
            company['crawled_at'] = crawled_at

            yield company
            yield response.follow(url, self.parseCompanyProfile)


    def parseCompanyProfile(self, response):
        created_at = datetime.datetime.now().strftime("%y-%m-%d")
        source = response.css('title ::text').extract_first()
        industry = response.css('.boxTitle div ::text').extract_first()
        SET_SELECTOR = '.tablecontent tr'
        elements = response.css(SET_SELECTOR)
        for index in range(int(len(elements)/7)):
            first_index = index*7
            url = elements[first_index].css('td a ::attr(href)').extract_first()

            if url:
                request = scrapy.Request(url, callback=self.parseCompanyProfileDetail)
                request.meta['data'] = {
                    'source': source,
                    'company_name': elements[first_index].css('td a ::attr(title)').extract_first(),
                    'company_url': url,
                    'uid': url,
                    'company_website': elements[first_index+1].css('td a ::attr(href)').extract_first(),
                    'company_description': elements[first_index+5].css('td ::text').extract_first(),
                    'industry': industry,
                    'country': 'Vietnam',
                    'created_at': created_at
                }
                yield request

        if response.css('.paging[disabled] ::text').extract_first() == '1':
            for index, page in enumerate(response.css('.paging::attr(href)').extract()):
                if index > 0:
                    yield response.follow('http://www.vietnambiz.org'+page, self.parseCompanyProfile)

    def parseCompanyProfileDetail(self, response):
        data = response.meta['data']
        content = [(re.sub(r'[^\x00-\x7f]',r'', s)).strip().lstrip(' ').lstrip(' ') for i, s in enumerate(response.css('.boxContent tr').xpath(".//td[contains(., ' ')]/descendant-or-self::text()").extract())]

        image_url = response.css('.tablecontent tr td img ::attr(src)').extract_first()
        if 'product' in image_url:
            data['company_logo'] = 'http://www.vietnambiz.org/'+image_url
        else:
            data['company_logo'] = None

        data['company_emails'] = [parseValueAfterColon(content[i+1]) for i, s in enumerate(content) if ("mail" in s and parseValueAfterColon(content[i+1]) != '' and '@' in parseValueAfterColon(content[i+1]))] + [parseValueAfterColon(s) for i, s in enumerate(content) if ("mail" in s.lower() and parseValueAfterColon(s) != '' and '@' in parseValueAfterColon(s))]

        data['company_street_address'] = getFirst([parseValueAfterColon(s) for i, s in enumerate(content) if ("add" in s.lower() and parseValueAfterColon(s) != '')])

        data['company_phone_number'] = [phoneFormat(parseValueAfterColon(s)) for i, s in enumerate(content) if (("tel" in s.lower() or "phone" in s.lower()) and len(re.sub("[^0-9]", '', phoneFormat(parseValueAfterColon(s)))) > 5 and ' , ' not in phoneFormat(parseValueAfterColon(s)))]

        data['company_fax_number'] = [phoneFormat(parseValueAfterColon(s)) for i, s in enumerate(content) if ("fax" in s.lower()  and len(re.sub("[^0-9]", '', phoneFormat(parseValueAfterColon(s)))) > 5 and ' , ' not in phoneFormat(parseValueAfterColon(s)))]

        data['number_of_employees'] = getFirst([parseValueAfterColon(s) for i, s in enumerate(content) if ("number" in s.lower() and "employees" in s.lower() and parseValueAfterColon(s) != '')])

        data['type_of_business'] = getFirst([parseValueAfterColon(s) for i, s in enumerate(content) if ("type" in s.lower() and "business" in s.lower() and parseValueAfterColon(s) != '')])

        data['major_brands'] = getFirst([parseValueAfterColon(s) for i, s in enumerate(content) if ("major" in s.lower() and "brand" in s.lower() and parseValueAfterColon(s) != '')])

        data['revenue'] = getFirst([parseValueAfterColon(s) for i, s in enumerate(content) if ("turnover" in s.lower() and parseValueAfterColon(s) != '')] + [parseValueAfterColon(content[i+1]) for i, s in enumerate(content) if ("turnover" in s.lower() and parseValueAfterColon(s) != '')])

        company_profile = CompanyProfileItem(data)

        yield company_profile

def parseValueAfterColon(s=''):
    position = None
    positions = [pos for pos, char in enumerate(s) if char == ':']
    if len(positions) > 0:
        position = positions[0]+1
    if isinstance(position, int):
        return s[position:].lstrip().lstrip()
    else:
        return ''

def getFirst(a_list=[]):
    if len(a_list)>0:
        return a_list[0]

def phoneFormat(number):
    return re.sub("[^0-9\\\\\(\)-, ]", '', number)

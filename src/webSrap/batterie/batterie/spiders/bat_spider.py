import scrapy

# scrapy crawl bat_spider
# scrapy crawl bat_spider -O data.json
# scrapy crawl bat_spider -O data.csv


class bat_spider(scrapy.Spider):
    name = "bat_spider"
    allowed_domains = ["www.listentech.com", "secondlifestorage.com"]
    start_urls = [
        "https://www.listentech.com/product-category/radio-frequency/150mhz/accessories-150mhz/batteries-150mhz/"
    ]

    def parse(self, response):
        yield scrapy.Request(
            "https://www.listentech.com/product-category/radio-frequency/150mhz/accessories-150mhz/batteries-150mhz/",
            callback=self.parse_0,
        )

        yield scrapy.Request(
            "https://secondlifestorage.com/index.php?pages/cell-database/",
            callback=self.parse_1,
        )

    def parse_0(self, response):
        list = response.css("ul.products")
        elements = list.css("li")
        print("START")
        for product in elements:
            title = product.css(".product-preview-description::text").extract()[0]
            link = product.css("a.woocommerce-LoopProduct-link::attr(href)").extract()[
                0
            ]
            data = yield scrapy.Request(link, callback=self.parse_data)
            yield {"titre_batterie": title, "data": data}
        # print("FINISH")

    def parse_data(self, response):
        title = response.css("h1.product_title::text , span.sku::text ").extract()

        summary = response.css('div[id="refHTML"]::text').extract()
        if summary == []:
            summary = response.css(
                "div.listen-product-content__content-block > p::text"
            ).extract()

        content_high = response.css(
            ".listen-accordion-content > article#highlights > .listen-accordion-item__container > ul > li::text"
        ).extract()
        # print("highlights: ",content_high)
        content_also_recei = response.css(
            ".listen-accordion-content > article#also-needed > .listen-accordion-item__container > .grid.listen-isotop-grid > .element-item.region-dynamic-element.receiver > div > h3 > a::text"
        ).extract()
        # print("also needed receiver: ",content_also_recei)
        content_also_trans = response.css(
            ".listen-accordion-content > article#also-needed > .listen-accordion-item__container > .grid.listen-isotop-grid > .element-item.region-dynamic-element.transceiver > div > h3 > a::text"
        ).extract()
        # print("also needed transceiver: ",content_also_trans)
        content_spec = response.css(
            ".listen-accordion-content > article#specs > .listen-accordion-item__container > div > div > div > table"
        ).extract()
        # print("spec: ",content_spec)
        content_faq = response.css(
            ".listen-accordion-content > article#faqs > .listen-accordion-item__container > div > div"
        )
        # print("faq: ")

        FaQ = []
        for questions in content_faq:
            print(questions.extract())
            Q = questions.css("h4 ::text").extract()[1]
            A = questions.css("div > div::text").extract()[0]

            FaQ.append([Q, A])
            link = questions.css("a").get()
            if link is not None:
                href = questions.css("a::attr(href)").extract()[0]
                # res = questions.css("a::text").extract()[0]
                A = yield scrapy.Request(href, callback=self.parse_warranty)

        yield {
            "title": title,
            "summary": summary,
            "highlights": content_high,
            "needed_receiver": content_also_recei,
            "needed_transceiver": content_also_trans,
            "spec": content_spec,
            "FaQ": FaQ,
        }

    def parse_warranty(self, response):
        title_list = response.css(
            "div.elementor-widget-wrap.elementor-element-populated > div.elementor-element.elementor-widget-heading > div > h2::text"
        ).extract()
        txt_list = response.css(
            "div.elementor-widget-wrap.elementor-element-populated > div.elementor-element.elementor-widget-text-editor > div > p::text"
        ).extract()
        idx = 1
        for T in title_list:
            yield {"Warrenty_title": T, "Warrenty_txt": txt_list[idx]}
            idx += 1

    def parse_1(self, response):
        content = response.css(".bbTable")
        liste = content.xpath("//table/tr")
        rows = liste.xpath(".//td")
        # print(rows)
        # total = []
        batterie = []
        idx = 0
        for line in rows:
            txt = line.xpath("text()").extract()
            link = line.css("a::attr(href)").extract()
            # print(txt)
            if len(link) > 0:
                print(link)
                # data = yield scrapy.Request(link[0], callback=self.parse_viewMore)

            if txt == []:
                if batterie != []:
                    if idx == 0:
                        batterie = batterie[5:]
                    idx += 1
                    yield {
                        "Brand": batterie[0],
                        "Model": batterie[1],
                        "Formfactor": batterie[2],
                        "Wrap Color": batterie[3],
                        "Ring Color": batterie[4],
                    }
                batterie = []
            else:
                batterie.append(txt[0])

    def parse_viewMore(self, response):
        content = response.css(".bbWrapper")
        liste = content.xpath("//table/tr")
        rows = liste.xpath(".//td")
        tableau = []
        for line in rows:
            txt = line.xpath("text()").extract()
            if txt != []:
                tableau.append(txt)
        tableau = tableau[:7]
        # title = line.xpath("//b//text()").extract()[6:]
        # table = []
        # idx = 0
        yield {
            "Brand": tableau[0],
            "Model": tableau[1],
            "Capacity": tableau[2],
            "Voltage": tableau[3],
            "Charging": tableau[4],
            "Discharging": tableau[5],
            "Description": tableau[6],
        }

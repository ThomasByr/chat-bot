import argparse

# import scrapy
from scrapy.crawler import CrawlerProcess
from .batterie.batterie.spiders import bat_spider

# python webScrap.py --output data.json


def run_spider(output_filename: str):
    process = CrawlerProcess(
        settings={"FEED_FORMAT": "json", "FEED_URI": output_filename}
    )
    process.crawl(bat_spider.bat_spider)
    process.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Scrapy Spider")
    parser.add_argument("--output", help="Output filename", default="output.json")
    args = parser.parse_args()
    run_spider(args)

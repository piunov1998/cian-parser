import URLgenerator
from searchpageparser import searchParser
from flatpageparser import offerParser

class Parser:

    def __init__(self) -> None:
        print('Parser activated!')


    def run(self, start_page = 1, end_page = 2) -> dict:
        db = {}
        print('Creating DB...')
        for page in range(start_page, end_page + 1):
            print('Generating URL...')
            url = URLgenerator.generate_url(page)
            for offer_link in searchParser.get_data(searchParser, url):
                print(f'Parsing {offer_link}')
                db.update({offer_link : offerParser.get_data(offerParser, offer_link)})
        return db


    # def data_formatter(self, url: str, data: dict) -> dict:
    #     self.db[url] = offerParser.get_data(offerParser, url)
        
import URLgenerator, time, random, sys
from pageparser import offerParser, searchParser

class Parser:

    def __init__(self) -> None:
        print('Parser activated!')


    def run(self, start_page = 1, end_page = 2) -> dict:
        db = {}
        print('Creating DB...')
        for page in range(start_page, end_page + 1):
            print('Generating URL...')
            url = URLgenerator.generate_url(page)
            search_results = searchParser.get_data(searchParser, url)
            if len(search_results) == 0:
                sys.exit('Capcha detected. Breaking work..')
            for offer_link in search_results:
                print(f'Parsing {offer_link}')
                db.update({offer_link : offerParser.get_data(offerParser, offer_link)})
                time.sleep(5.0 + random.randint(0, 3) + random.random())
        return db
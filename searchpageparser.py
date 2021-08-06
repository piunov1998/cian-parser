from bs4 import BeautifulSoup
import requests

class searchParser:

    def __init__(self) -> None:
        pass

    
    def download_page(url: str) -> BeautifulSoup:
        session = requests.Session()
        session.headers = {'Accept-Language': 'ru'}
        page = session.get(url=url)
        html = page.text
        try:
            search_page = BeautifulSoup(html, 'lxml')
        except:
            search_page = BeautifulSoup(html, 'html.parser')
        return search_page


    def offers_parse(page: BeautifulSoup) -> list:
        offers = page.select('div[data-name="Offers"] > article[data-name="CardComponent"]')
        offers_links = []
        for offer in offers:
            print('Scaning for url')
            href = offer.select_one('div[data-name="LinkArea"] > a')
            link = href.get('href')
            offers_links.append(link)
        print(f'Found {len(offers_links)} offers')
        return offers_links


    def get_data(self, url: str) -> list:
        print(f'Parsing {url}')
        return self.offers_parse(self.download_page(url))

#print(searchParser.offers_parse(serachParser.download_page('https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&object_type%5B0%5D=1&offer_type=flat&region=1&room1=1&room2=1')))
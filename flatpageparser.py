from typing import Dict
import requests, re
from bs4 import BeautifulSoup
from ast import literal_eval

class offerParser:
    
    
    def __init__(self):
        self.html = ''
        self.script = None

    
    def download_page(self, url : str) -> BeautifulSoup:
        session = requests.Session()
        session.headers = {'Accept-Language': 'ru'}
        page = session.get(url=url)

        self.html = page.text

        try:
            offer_page = BeautifulSoup(self.html, 'lxml')
        except:
            offer_page = BeautifulSoup(self.html, 'html.parser')
        return offer_page


    def parse_page(self, page : BeautifulSoup) -> dict:
    #totalArea
        try:
            text_offer = page.select("div[data-name='Description'] > div > div:nth-child(2)")[0].text
            comm = (text_offer[: text_offer.find("Общая")])
            comm_meters = float((re.findall(r'\d+', comm)[0]).replace(',', '.'))
        except IndexError:
            text_offer = page.select("div[data-name='Description'] > div")[0].text
            comm = (text_offer[: text_offer.find("Общая")])
            comm_meters = float((re.findall(r'\d+', comm)[0]).replace(',', '.'))
        except:
            comm_meters = -1


        #Kitchen
        try:
            text_offer = page.select("div[data-name='Description'] > div > div:nth-child(2)")[0].text
            kitchen = (text_offer[text_offer.find("Кухня")-6: text_offer.find("Кухня")])
            kitchen_meters = float((re.findall(r'\d+', kitchen)[0]).replace(',', '.'))
        except IndexError:
            text_offer = page.select("div[data-name='Description'] > div > div")[0].text
            if "Кухня" in text_offer:
                kitchen = (text_offer[text_offer.find("Кухня")-6: text_offer.find("Кухня")])
                kitchen_meters = float((re.findall(r'\d+', kitchen)[0]).replace(',', '.'))
            else:
                kitchen_meters = -1
        except:
            kitchen_meters = -1


        #Floor
        try:
            description = page.select("div[data-name='Description'] > div > div > div")
            for block in description:
                if 'Этаж' in block.text:
                    floor_info = (block.text[: block.text.find("Этаж")]).split(' из ')
            #text_offer = page.select("div[data-name='Description'] > div > div > div")[3].text
            #floor_info = (text_offer[text_offer.find("Этаж")-5: text_offer.find("Этаж")]).split(' из ')
            floor, total_floor = int(floor_info[0]), int(floor_info[1])
        except IndexError:
            text_offer = page.select("div[data-name='Description'] > div > div > div")[3].text
            if "Этаж" in text_offer:
                floor_info = (text_offer[text_offer.find("Этаж")-5: text_offer.find("Этаж")]).split(' из ')
                floor, total_floor = int(floor_info[0]), int(floor_info[1])
            else:
                floor, total_floor = -1, -1
        except:
            floor, total_floor = -2, -2


        #Material
        try:
            text_offer = page.select("div[data-name='NewbuildingAdvantagesContainer'] > ul[data-name='NewbuildingSpecifications']")[0].text
            cursor = text_offer.find("Тип дома")
            house_material = (text_offer[cursor + 8: cursor + 8 + 5])
        except IndexError:
            try:
                text_offer = page.select("div[data-name='BtiContainer'] > div[data-name='BtiHouseData']")[0].text
                if not "Тип дома" in text_offer:
                    house_material = -1
                else:
                    cursor = text_offer.find("Тип дома")
                    house_material = (text_offer[cursor + 8: cursor + 8 + 5])
            except IndexError:
                house_material = None
        except Exception as error:
            house_material = error


        #Year
        try:
            text_offer = page.select("div[data-name='BtiContainer'] > div[data-name='BtiHouseData']")[0].text
            year = int(text_offer[text_offer.find("Год постройки")+13: text_offer.find("Год постройки") + 17])
        except:
            year = -1

        coords = re.findall(r'"coordinates":{"lng":\d+\.\d+,"lat":\d+\.\d+}', self.html)
        if len(coords) < 1:
            latitude, longitude = None, None
        else:
            lat_lng = literal_eval('{' + coords[0] + '}')
            latitude = lat_lng['coordinates']['lat']
            longitude = lat_lng['coordinates']['lng']

        data = {
            'totalArea' : comm_meters,
            'kitchenArea' : kitchen_meters,
            'wallsMaterial' : house_material,
            'year' : year,
            'floorNumber': floor,
            'floorsTotal': total_floor,
            'latitude': latitude,
            'longitude': longitude
        }

        return data

    
    def get_data(self, url : str) -> dict:
        return self.parse_page(self, self.download_page(self, url))
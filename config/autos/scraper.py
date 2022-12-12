from typing import Optional, List, Dict
from datetime import datetime
import httpx
from parsel import Selector


class Scraper:

    def __init__(self, url: str) -> None:
        self.url = url
        self.title_xpath='div/div/a/span/text()'
        self.year_xpath='div/div/a/text()'
        self.price_xpath='div[@class="price-ticket"]'
        self.miliage_xpath='div[@class="definition-data"]/ul/li/text()'
        self.state_number_xpath='div[@class="definition-data"]\
                            /div[@class="base_information"]\
                            /span[contains(@class, "state-num")]'
    
    def get_html(self) -> Optional[str]:
        """ Returns html page as str """

        response = httpx.get(url=self.url)
        return response.text if response.status_code == 200 else None


    def scrap_all_cars_on_page(self) -> List:
        """ Searching all {div.content} and calling {scrap_single_car} """

        text = self.get_html()
        if text:
            selector = Selector(text=text)
            cars = selector.xpath('//div[@class="content"]') 
            return self.scrap_single_car(cars=cars)   
        else:
            print('Bad response...')

    
    def scrap_single_car(self, cars: Selector) -> List:
        """ Takes list[div.content] as argument and scrapes car data from every div.
            Retrurns List with dictionaries
        """ 

        cars_list = list()
        
        for car in cars:
            car_data = dict()
            car_data['href'] = car.xpath('div/div/a').attrib['href']
            car_data['title'] = car.xpath(self.title_xpath).get().strip()
            car_data['year'] = int(' '.join(car.xpath(self.year_xpath).getall()).strip())
            car_data['price'] = int(car.xpath(self.price_xpath).attrib['data-main-price'])
            car_data['mileage'] = self.get_milliage(car=car)
            car_data['state_number'] = self.get_state_number(car=car)
            cars_list.append(car_data)

        return cars_list

    
    def get_milliage(self, car: Selector) -> Optional[int]:
        miliage_div = car.xpath(self.miliage_xpath).get().split(' ')
        miliage = miliage_div[1]
        if miliage.isnumeric():
            return int(miliage) * 1000


    def get_state_number(self, car: Selector) -> Optional[str]:
        state_number_block = car.xpath(self.state_number_xpath)
        if state_number_block:
            return state_number_block.xpath('text()').get().strip()

        
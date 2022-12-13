from typing import Optional, List
import httpx
from parsel import Selector

from autos.serializers import NewCarSerializer


class Scraper:

    def __init__(self) -> None:
        self.title_xpath='div/div/a/span/text()'
        self.year_xpath='div/div/a/text()'
        self.price_xpath='div[@class="price-ticket"]'
        self.miliage_xpath='div[@class="definition-data"]/ul/li/text()'
        self.state_number_xpath='div[@class="definition-data"]\
                            /div[@class="base_information"]\
                            /span[contains(@class, "state-num")]'
    
    def get_html(self, url: str) -> Optional[str]:
        """ Returns html page as str """

        response = httpx.get(url=url)
        return response.text if response.status_code == 200 else None


    def scrap_all_cars_on_page(self, url: str) -> List:
        """ Searching all {div.content} and calling {scrap_single_car} """

        text = self.get_html(url=url)
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

        
    def insert_into_database(self, url: str) -> NewCarSerializer:
        """ Inserts all cars into database. Returns the most expensive car """

        cars_list = self.scrap_all_cars_on_page(url=url)
        top_car = NewCarSerializer(data=cars_list[0])
        if top_car.is_valid():
            top_car.save()
        for car in cars_list[1:]:
            new_car = NewCarSerializer(data=car)
            if new_car.is_valid():
                new_car.save()
                top_car = self.compare_prices(car_1=top_car, car_2=new_car)
        return top_car

    
    def compare_prices(self, car_1: NewCarSerializer, car_2: NewCarSerializer) -> NewCarSerializer:
        """ Returns car with highest price (returns 1st car if prices are equals """

        return car_2 if car_2.validated_data['price'] > car_1.validated_data['price'] else car_1

        
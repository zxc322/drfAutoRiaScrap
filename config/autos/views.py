from rest_framework.views import APIView
from rest_framework.response import Response

from autos.models import Car
from autos.scraper import Scraper
from autos.serializers import NewCarSerializer, CarSerializer


class ScrapPage(APIView):

    def get(self, request, pk):
        scrap_url = f"https://auto.ria.com/uk/car/used/?page={pk}"
        cars_list = Scraper(url=scrap_url).scrap_all_cars_on_page()
        the_most_expensive = NewCarSerializer(data=cars_list[0])
        the_most_expensive.is_valid()
        for car in cars_list:
            new_car = NewCarSerializer(data=car)
            if new_car.is_valid():
                new_car.save()
                if new_car.validated_data['price'] > the_most_expensive.validated_data['price']:
                    the_most_expensive = new_car
        
        return Response(the_most_expensive.validated_data)

    

class GetAllCars(APIView):

    def get(self, request):
        cars = Car.objects.all()
        serialized = CarSerializer(cars, many=True)
        return Response(serialized.data)

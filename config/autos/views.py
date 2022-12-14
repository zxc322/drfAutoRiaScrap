from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from autos.services.scraper import Scraper
from autos.services.auto_filters import AutoFilter
from autos.serializers import CarSerializer


class ScrapPage(APIView):

    def get(self, request, pk):
        scrap_url = f"https://auto.ria.com/uk/car/used/?page={pk}"
        the_most_expesice_car = Scraper().insert_into_database(url=scrap_url)      
        return Response(the_most_expesice_car.validated_data)


class GetAllCars(APIView):

    def get(self, request):
        queryset = AutoFilter(params=request.META.get('QUERY_STRING')).apply_filters()
        serializer = CarSerializer(queryset, many=True)
        return Response(serializer.data)
        
            

    
    

    
        

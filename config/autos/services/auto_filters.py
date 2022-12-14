import json
from json.decoder import JSONDecodeError
from typing import Any
from rest_framework.exceptions import APIException
from django.db.models.query import QuerySet

from autos.models import Car


class AutoFilter:

    def __init__(self, params: str = None) -> None:
        self.allowed_params = ('price', 'year', 'state_number', 'mileage', 'order_by', 'page', 'limit')
        self.order_by_allowed_values = ('price', '-price', 'year', '-year', 'mileage', '-mileage')
        self.params = params
        self.filters = dict()
        self.queryset = Car.objects.all()
        self.parse_params()

    
    def parse_params(self):
        if self.params:
            params_list = self.params.split('?')
            for k_v in params_list:
                k, v = k_v.split('=')
                if k in self.allowed_params:
                    try:
                        self.filters.update({k:json.loads(v)})
                    except JSONDecodeError:
                        self.filters.update({k:v})

    def range_validator(self, obj: Any, param: str) -> None:
        if not isinstance(obj, list) or  len(obj) != 2:
            raise APIException(detail=f'{param} value must be a list and contains 2 integer inside')

    
    def filter_by_state_number(self) -> None:
        if self.filters['state_number'] == True:
            self.queryset = self.queryset.filter(state_number__isnull=False)
        elif self.filters['state_number'] == False:
            self.queryset = self.queryset.filter(state_number__isnull=True)
        else:
            raise APIException(detail='Wrong state_number value. Expected values: [true, false]')


    def filter_by_price(self) -> None:
        price_range = self.filters['price']
        self.range_validator(obj=price_range, param='Price')
        self.queryset = self.queryset.filter(price__range=(price_range[0], price_range[1]))


    def filter_by_year(self) -> None:
        year_range = self.filters['year']
        self.range_validator(obj=year_range, param='Year')
        self.queryset = self.queryset.filter(year__range=(year_range[0], year_range[1]))


    def filter_by_mileage(self) -> None:
        mileage_range = self.filters['mileage']
        self.range_validator(obj=mileage_range, param='Mileage')
        self.queryset = self.queryset.filter(mileage__range=(mileage_range[0], mileage_range[1]))


    def order_by_(self):
        ordering_field = self.filters['order_by']
        if ordering_field not in self.order_by_allowed_values:
            raise APIException(detail=f'Order_by field is not allowed.\
                 Allowed fields: "{self.order_by_allowed_values}"')
        self.queryset = self.queryset.order_by(ordering_field)

    
    def paginated_queryset(self) -> None:
        page = self.filters.get('page')
        limit = self.filters.get('limit')
        if not limit or not isinstance(limit, int):
            limit = 10
        if not page or not isinstance(page, int) or page < 1:
            page = 1
        start = (page-1) * limit
        return self.queryset[start:start+limit]



    def apply_filters(self) -> QuerySet:
        if self.filters.get('state_number'):
            self.filter_by_state_number()

        if self.filters.get('price'):
            self.filter_by_price()

        if self.filters.get('year'):
            self.filter_by_year()

        if self.filters.get('mileage'):
            self.filter_by_mileage()

        if self.filters.get('order_by'):
            self.order_by_()
        
        return self.paginated_queryset()
        
    
    
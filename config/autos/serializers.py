from rest_framework import serializers
from autos.models import Car


class NewCarSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    year = serializers.IntegerField()
    price = serializers.IntegerField()
    mileage = serializers.IntegerField(required=False, allow_null=True)
    state_number = serializers.CharField(required=False, allow_null=True, max_length=30)
    href = serializers.CharField(max_length=300)

    def create(self, validated_data):
        return Car.objects.get_or_create(**validated_data) 

    
class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'

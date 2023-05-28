from rest_framework import serializers
from .models import Weather, ParsingTask


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = '__all__'


class ParsingTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParsingTask
        fields = '__all__'

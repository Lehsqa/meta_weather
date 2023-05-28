from rest_framework import viewsets, views, status

from .cron import reschedule
from .models import Weather, ParsingTask
from .serializers import WeatherSerializer, ParsingTaskSerializer
from rest_framework.response import Response
from .utils import update_weather


class WeatherViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Weather.objects.all()
    serializer_class = WeatherSerializer


class UpdateWeatherView(views.APIView):
    def get(self, request, format=None):
        # Создание новой задачи парсинга
        task = ParsingTask.objects.create(status='Scheduled')

        try:
            # Запуск задачи обновления погоды
            update_weather()

            # Обновление статуса задачи на 'Done'
            task.status = 'Done'
            task.save()

            return Response({"message": "Weather information has been updated."})
        except Exception as e:
            # Обновление статуса задачи на 'In Progress'
            task.status = 'In Progress'
            task.save()

            # Возвращение сообщения об ошибке
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ParsingTaskViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ParsingTask.objects.all()
    serializer_class = ParsingTaskSerializer


class UpdateWeatherTimeView(views.APIView):
    def get(self, request, format=None):
        # Получение нового времени обновления из запроса
        new_time = request.GET.get('time')
        print(new_time)

        if not new_time:
            return Response({"error": "Invalid time value."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Изменение времени обновления
            reschedule(new_time)
            return Response({"message": "Weather update time has been changed."})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

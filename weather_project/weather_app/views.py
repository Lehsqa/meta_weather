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
        # Creating a new parsing task
        task = ParsingTask.objects.create(status='Scheduled')

        try:
            # Starting the weather update task
            update_weather()

            # Update task status to 'Done'
            task.status = 'Done'
            task.save()

            return Response({"message": "Weather information has been updated."})
        except Exception as e:
            # Update task status to 'In Progress'
            task.status = 'In Progress'
            task.save()

            # Return of an error message
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ParsingTaskViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ParsingTask.objects.all()
    serializer_class = ParsingTaskSerializer


class UpdateWeatherTimeView(views.APIView):
    def get(self, request, format=None):
        # Obtaining a new update time from a request
        new_time = request.GET.get('time')
        print(new_time)

        if not new_time:
            return Response({"error": "Invalid time value."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Changing the update time
            reschedule(new_time)
            return Response({"message": "Weather update time has been changed."})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

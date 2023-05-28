from django.apps import AppConfig


# Main app
class WeatherAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'weather_app'

    # When app is ready, scheduler job is running
    def ready(self):
        from .cron import start
        start()

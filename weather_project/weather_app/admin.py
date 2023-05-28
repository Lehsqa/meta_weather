from django.contrib import admin
from .models import Weather, ParsingTask

# Register your models here.
admin.site.register(Weather)
admin.site.register(ParsingTask)

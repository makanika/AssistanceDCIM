from django.contrib import admin
from .models import Rack, SensorData, PDUFeed, CrossConnect

admin.site.register(Rack)
admin.site.register(SensorData)
admin.site.register(PDUFeed)
admin.site.register(CrossConnect)


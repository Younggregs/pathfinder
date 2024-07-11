from django.contrib import admin

from flightfinder.models import Airline, Airport, JourneyPath, Flight

# Register your models here.
class AirlineAdmin(admin.ModelAdmin):
  list_display = ['name', 'slug']
  search_fields = ('name', 'slug')
  ordering = ('name',)
  
admin.site.register(Airline, AirlineAdmin)

class AirportAdmin(admin.ModelAdmin):
  list_display = ['name', 'code']
  search_fields = ('name', 'code')
  ordering = ('name',)
  
admin.site.register(Airport, AirportAdmin)

class JourneyPathAdmin(admin.ModelAdmin):
  list_display = ['origin', 'destination', 'airline']
  search_fields = ('origin', 'destination', 'airline')
  ordering = ('origin',)
  
admin.site.register(JourneyPath, JourneyPathAdmin)

class FlightAdmin(admin.ModelAdmin):
  list_display = ['flight_number', 'price', 'departure_time']
  search_fields = ('flight_number', 'price', 'departure_time')
  ordering = ('flight_number',)
  
admin.site.register(Flight, FlightAdmin)
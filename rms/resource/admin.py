from django.contrib import admin
from resource.models import *

class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name','type','location', 'owning_dep', 'availability', 'Add_information')

class PriorityAdmin(admin.ModelAdmin):
     list_display = ('Designation','Priority_num')

class Booked_resourceAdmin(admin.ModelAdmin):
    list_display = ('Booked_by','Event_name','Purpose_of_booking', 'all_day_event', 'start_date', 'start_time', 'end_date', 'end_time', 'resource_id','resource_name','resource_type')
	 

admin.site.register(Resource, ResourceAdmin)
admin.site.register(Priority_table, PriorityAdmin)
admin.site.register(Booked_resource,Booked_resourceAdmin)



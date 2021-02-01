from django.contrib import admin
from .models import employee
# Register your models here.
class empregister(admin.ModelAdmin):
    list_display = [
        'start_date','end_date','status','r_date'
    ]

admin.site.register(employee,empregister)
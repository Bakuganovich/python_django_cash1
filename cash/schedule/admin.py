from django.contrib import admin
from schedule.models import Timetable_Day

@admin.register(Timetable_Day)
class Timetable_Admin(admin.ModelAdmin):
    list_display = ['name', 'date']
    search_fields = ['name','date']
    list_filter = ['date']
    fields = [('one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'), 'date']
# Register your models here.

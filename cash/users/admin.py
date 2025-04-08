from django.contrib import admin
from users.models import User, Booking


class BookingTab_Admin(admin.TabularInline):
    model = Booking
    list_display = ['id', 'first_name', 'last_name', 'phone', 'username', 'is_active', 'date_joined']
    extra = 1


@admin.register(User)
class User_Admin(admin.ModelAdmin):
    list_display = ['id','completed_classes','first_name','last_name','phone', 'username', 'course_purchased','date_joined']
    list_editable = ['first_name','last_name','phone', 'course_purchased',]
    search_fields = ['id','first_name','last_name','phone', 'username',]
    list_filter = ['course_purchased','completed_classes','date_joined']

    inlines =  [BookingTab_Admin,]




@admin.register(Booking)
class Booking_Admin(admin.ModelAdmin):
    list_display = ['user__id','user__username', 'user__first_name', 'user__last_name' ,'car_model', 'get_status_display','time', 'date',]
    search_fields = ['user__id','user__username', 'user__first_name', 'user__last_name' ]

    list_filter = ['car_model', 'status','time', 'date', ]

# Register your models here.

from schedule import views
from django.urls import path

app_name = 'schedule'


urlpatterns = [
    path('', views.timetable, name='timetable'),
]
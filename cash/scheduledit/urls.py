from scheduledit import views
from django.urls import path

app_name = 'scheduledit'


urlpatterns = [
    path('', views.timetable, name='timetable'),
    path('timetable_add/', views.timetable_add, name='timetable_add'),
    path('timetable_delete/', views.timetable_delete, name='timetable_delete'),
    path('detailed/', views.detailed, name='detailed'),
]
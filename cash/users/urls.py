from django.urls import path
from users import views

app_name = 'authentication'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('profile_student/', views.profile_student, name='profile_student'),
    path('approvall/', views.approvall, name='approvall'),

]
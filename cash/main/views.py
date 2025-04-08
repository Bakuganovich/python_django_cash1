from django.shortcuts import render

def index(request):
    return render(request, 'main/index.html')
# Create your views here.

def info_course(request):
    return render(request, 'main/info_course.html')
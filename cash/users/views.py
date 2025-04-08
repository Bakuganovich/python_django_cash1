from django.shortcuts import render, redirect, reverse, get_object_or_404, get_list_or_404
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse,HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from schedule.models import Timetable_Day
from users.models import User,Booking
from users.forms import UserLoginForm,UserRegistrationForm,ProfileForm
from datetime import datetime
from utils import check_user, user_student
#Пользовательская часть

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserLoginForm()
    context = {'form':form}
    return  render(request, 'users/authentication.html', context)


def registration(request):
    if request.method=='POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserRegistrationForm()
    context = {'form':form}
    return render(request,'users/registration.html',context)

@login_required
def profile(request):
    if request.POST:
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = ProfileForm(instance=request.user)

    db_booking = Booking.objects.filter(user=request.user,).order_by('date')
    user = get_object_or_404(User,username=request.user.username)
    context = {'title':'Кабинет', 'form':form, 'booking': db_booking,'completed_classes':user.completed_classes}

    return render(request,'users/profile.html',context)

def logout(request):
    auth.logout(request)
    return redirect(reverse('main:index'))


#Админ часть


def profile_student(request):
    if not check_user(request.user):  # Безопасная проверка пользователя
        return HttpResponseNotFound("<h1>Страница не найдена</h1>")

    if request.method == 'GET' :
        student_id = request.GET['id']  # Get the student ID from the POST data
        student = get_object_or_404(User, id=student_id)  # Fetch the student from the database
        form = ProfileForm(instance=student)
        url = '/media/'+str(student.image)
        db_booking = Booking.objects.filter(user=student).order_by('date')
        context = {'url':url, 'form':form, 'booking': db_booking, 'completed_classes':student.completed_classes, }
        return render(request, 'users/student_profile.html', context)

    return HttpResponse("<h1>Метод не поддерживается</h1>", status=405)


def approvall(request):
    if not check_user(request.user):
        return HttpResponseNotFound("<h1>Страница не найдена</h1>")

    if request.method == 'POST':
        date_str = request.POST.get('date')
        model = request.POST.get('model')
        time = request.POST.get('time')
        decision = request.POST.get('decision')
        student_username = request.POST.get('student')

        if not all([date_str, model, time, decision]):  # Проверяем, что все ключи переданы
            return HttpResponse("<h1>Некорректные данные</h1>", status=400)  # 400 Bad Request

        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return HttpResponse("<h1>Неверный формат даты</h1>", status=400)

        booking = get_object_or_404(Booking, car_model=model, date=date_obj, time=time, status='pending')

        if decision == "approved" and student_username:
            user = get_object_or_404(User, username=student_username)
            user.completed_class()
            booking.confirm()

        elif decision == "rejected":
            timetable = get_object_or_404(Timetable_Day, name=model, date=date_obj)
            # Словарь соответствия времени именам полей
            time_field_mapping = {
                '7:00': 'one',
                '8:30': 'two',
                '10:00': 'three',
                '11:30': 'four',
                '13:00': 'five',
                '14:30': 'six',
                '16:00': 'seven',
                '17:30': 'eight',
                '19:00': 'nine',
            }
            setattr(timetable,  time_field_mapping[time] , None)
            timetable.save()

            booking.reject()
        else:
            return HttpResponse("<h1>Некорректное значение decision</h1>", status=400)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


    return HttpResponse("<h1>Метод не поддерживается</h1>", status=405)





# Create your views here.


from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse,HttpResponseNotFound
from schedule.models import Timetable_Day
from users.models import User
from utils import check_user



def timetable(request):
    if not check_user(request.user):  # Безопасная проверка пользователя
        return HttpResponseNotFound("<h1>Страница не найдена</h1>")

    sorted_db= Timetable_Day.objects.all().order_by('date')
    context = {'cars': sorted_db}
    return render(request, 'scheduledit/timetable.html', context)



def timetable_add(request):
    if not check_user(request.user):  # Безопасная проверка пользователя
        return HttpResponseNotFound("<h1>Страница не найдена</h1>")

    if request.method == 'POST':
        name = request.POST['name']
        date = request.POST['date']

        if not(name and date):
            return redirect(reverse('scheduledit:timetable'))

        if  Timetable_Day.objects.filter(name=name, date=date).exists():
            sorted_db = Timetable_Day.objects.all().order_by('date')
            context = {'cars': sorted_db, 'error':'Машина уже забронирована.'}
            return render(request, 'scheduledit/timetable.html', context)

        Timetable_Day.objects.create(name=name, date=date)
        return redirect(reverse('scheduledit:timetable'))



def timetable_delete(request):
    if not check_user(request.user):  # Безопасная проверка пользователя
        return HttpResponseNotFound("<h1>Страница не найдена</h1>")

    if request.method == "POST":
        name = request.POST['name']
        date = request.POST['date']
        entry = Timetable_Day.objects.filter(name=name, date=date).first()
        if entry:
            entry.delete()
            return redirect(reverse('scheduledit:timetable')) # Перенаправляем на страницу расписания
        else:
            return HttpResponse("Запись не найдена", status=404)



def detailed(request):
    if not check_user(request.user):  # Безопасная проверка пользователя
        return HttpResponseNotFound("<h1>Страница не найдена</h1>")

    if request.method == 'GET':
        name = request.GET.get('name')
        date = request.GET.get('date')

        if not name or not date:
            return HttpResponseNotFound("<h1>Некорректные параметры</h1>")

        try:
            db = Timetable_Day.objects.get(name=name, date=date)
        except Timetable_Day.DoesNotExist:
            return HttpResponseNotFound("<h1>Расписание не найдено</h1>")

        time_slots = {
            '07:00:00': db.one,
            '08:30:00': db.two,
            '10:00:00': db.three,
            '11:30:00': db.four,
            '13:00:00': db.five,
            '14:30:00': db.six,
            '16:00:00': db.seven,
            '17:30:00': db.eight,
            '19:00:00': db.nine,
        }

        all_times = []
        for time, user_id in time_slots.items():
            user_info = None
            if user_id:
                user = User.objects.filter(id=user_id).first()  # Безопасный поиск
                if user:
                    user_info = {
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'username': user.username,
                        'phone': user.phone
                    }

            all_times.append({'time': time, 'user_id': user_id, 'user_info': user_info})

        context = {'name': name, 'date': date, 'all_times': all_times}
        return render(request, 'scheduledit/detailed.html', context)

    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
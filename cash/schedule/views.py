from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, HttpResponseNotFound
from schedule.models import Timetable_Day
from users.models import Booking
from datetime import datetime
from utils import user_student

def timetable(request):
    if not user_student(request.user):# Безопасная проверка пользователя
        return render(request, 'main/info_course.html')

    context = {
        'unique_cars': [],
        'unique_dates': [],
        'selected_car': '',
        'selected_date': '',
        'available_times': [],
        'success': '',
    }

    if request.user.is_authenticated:
        unique_cars = Timetable_Day.objects.values_list('name', flat=True).distinct()
        context['unique_cars'] = unique_cars

        if request.method == 'POST':
            selected_car = request.POST['car']
            selected_date = request.POST['date']
            selected_time = request.POST['time']
            # Преобразуем строку в объект даты (если нужно)
            try:
                selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
            except ValueError:
                context['success'] = 'Ошибка формата даты'
                return render(request, 'schedule/timetable.html', context)

            db = Timetable_Day.objects.filter(name=selected_car, date=selected_date).first()
            if db:
                time_slot_map = {
                    '07:00:00': 'one',
                    '08:30:00': 'two',
                    '10:00:00': 'three',
                    '11:30:00': 'four',
                    '13:00:00': 'five',
                    '14:30:00': 'six',
                    '16:00:00': 'seven',
                    '17:30:00': 'eight',
                    '19:00:00': 'nine',
                }
                selected_slot = time_slot_map.get(selected_time)

                if selected_slot and getattr(db, selected_slot) is None:
                    setattr(db, selected_slot, request.user.id)
                    db.save()

                    if not Booking.objects.filter(user=request.user, car_model=selected_car, date=selected_date,time=selected_time, status = 'Ожидайте').exists():
                        Booking.objects.create(user=request.user, car_model=selected_car, date=selected_date,time=selected_time)

                    context['success'] = 'Вы записаны'
                else:
                    context['success'] = 'Вы не записаны. Попробуйте другое время'

        # Обработка AJAX-запросов
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            car = request.GET.get('car')
            date = request.GET.get('date')

            # Возвращаем список дат, если выбрана машина
            if car and not date:
                dates = list(
                    Timetable_Day.objects.filter(name=car)
                    .values_list('date', flat=True)
                    .distinct()
                )
                formatted_dates = [d.strftime('%Y-%m-%d') for d in dates]  # Преобразуем даты в строковый формат
                return JsonResponse({'dates': formatted_dates})

            # Возвращаем список доступного времени, если выбраны машина и дата
            if car and date:
                try:
                    selected_date = datetime.strptime(date, '%Y-%m-%d').date()
                except ValueError:
                    return JsonResponse({'error': 'Некорректная дата'}, status=400)

                db = Timetable_Day.objects.filter(name=car, date=selected_date).first()
                if db:
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
                    available_times = [time for time, value in time_slots.items() if value is None]
                    return JsonResponse({'times': available_times})

        return render(request, 'schedule/timetable.html', context)

    return redirect(reverse('main:index'))

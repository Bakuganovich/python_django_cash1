from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', blank=True, null=True, verbose_name='Аватар')
    phone = models.CharField(max_length=15,verbose_name='Телефон')
    completed_classes = models.IntegerField(blank=True, null=True, verbose_name='Пройденные занятия')
    course_purchased = models.BooleanField(default=False, verbose_name='Курс куплен')

    def completed_class(self):
        if self.completed_classes is None:
            self.completed_classes = 0
        self.completed_classes += 1
        self.save()

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('confirmed', 'Подтверждено'),
        ('rejected', 'Отклонено'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    car_model = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def confirm(self):
        self.status = 'confirmed'
        self.save()

    def reject(self):
        self.status = 'rejected'
        self.save()

    class Meta:
        db_table = 'Booking'
        verbose_name = 'Запись пользователя'
        verbose_name_plural = 'Записи пользователей'

    def __str__(self):
        return f"{self.user.username} - {self.car_model} ({self.date} {self.time})"

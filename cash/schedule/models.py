from enum import unique

from django.db import models

class Timetable_Day( models.Model):
    name = models.CharField(max_length=150, verbose_name='Модель')
    date = models.DateField(max_length=20, verbose_name='Дата')
    one = models.IntegerField(blank=True, null=True,  verbose_name='07:00:00')
    two = models.IntegerField(blank=True, null=True,  verbose_name='08:30:00')
    three = models.IntegerField(blank=True, null=True, verbose_name='10:00:00')
    four = models.IntegerField(blank=True, null=True, verbose_name='11:30:00')
    five = models.IntegerField(blank=True, null=True, verbose_name='13:00:00')
    six = models.IntegerField(blank=True, null=True, verbose_name='14:30:00')
    seven = models.IntegerField(blank=True, null=True, verbose_name='16:00:00')
    eight = models.IntegerField(blank=True, null=True,  verbose_name='17:30:00')
    nine = models.IntegerField(blank=True, null=True,  verbose_name='19:00:00')


    class Meta:
        db_table = 'timetable'
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписание'

    def __str__(self):
        return f'{self.name}'


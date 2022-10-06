from django.db import models


class Task(models.Model):
    summary = models.CharField(max_length=200, null=False, blank=False, verbose_name="Заголовок")
    description = models.TextField(max_length=3000, null=False, blank=False, verbose_name='Описание')
    status = models.ForeignKey('webapp.Status', related_name='task', on_delete=models.PROTECT, verbose_name='Статус')
    type = models.ForeignKey('webapp.Type', related_name='task', on_delete=models.PROTECT, verbose_name='Тип')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время изменения')

    def __str__(self):
        return self.summary


class Status(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, verbose_name="Статус")

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, verbose_name="Тип")

    def __str__(self):
        return self.name

from django.db import models


class Task(models.Model):
    summary = models.CharField(max_length=200, null=False, blank=False, verbose_name="Заголовок")
    description = models.TextField(max_length=3000, null=False, blank=False, verbose_name='Описание')
    status = models.ForeignKey('webapp.Status', related_name='task', on_delete=models.PROTECT, verbose_name='Статус')
    type = models.ForeignKey('webapp.Type', related_name='task', on_delete=models.PROTECT, verbose_name='Тип')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    project = models.ForeignKey('webapp.Project', related_name='project', on_delete=models.CASCADE,
                                verbose_name='Проект',
                                default=1)
    is_deleted = models.BooleanField(default=False, verbose_name='Удален', null=False,)

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


class Project(models.Model):
    start_date = models.DateField(verbose_name="Дата начала")
    finish_date = models.DateField(verbose_name="Дата окончания", null=True, blank=True)
    name = models.CharField(max_length=200, null=False, blank=False, verbose_name="Название")
    description = models.TextField(max_length=3000, null=False, blank=False, verbose_name='Описание')

    def __str__(self):
        return self.name

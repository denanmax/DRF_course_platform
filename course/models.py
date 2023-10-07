# Create your models here.
from django.conf import settings
from django.db import models

from users.models import User


class Course(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название')
    preview = models.ImageField(upload_to='course', verbose_name='Превью', blank=True, null=True)
    description = models.TextField(verbose_name='Описание')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                              verbose_name='Создатель')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Subscriptions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_subscribed = models.BooleanField(default=False, verbose_name='Подписан')
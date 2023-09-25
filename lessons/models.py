from django.db import models

# Create your models here.
from django.db import models


class Lesson(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название')
    preview = models.ImageField(upload_to='lesson', verbose_name='Превью', blank=True, null=True)
    description = models.TextField(verbose_name='Описание')
    url = models.URLField(max_length=150, verbose_name='Ссылка')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
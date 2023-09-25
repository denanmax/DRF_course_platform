from django.db import models

# Create your models here.
from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название')
    preview = models.ImageField(upload_to='course', verbose_name='Превью', blank=True, null=True)
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
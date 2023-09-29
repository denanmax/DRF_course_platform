from django.db import models

# Create your models here.
from django.db import models

from course.models import Course

NULLABLE = {'blank': True, 'null': True}


class Lesson(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название')
    preview = models.ImageField(upload_to='lesson', verbose_name='Превью', blank=True, null=True)
    description = models.TextField(verbose_name='Описание')
    url = models.URLField(max_length=150, verbose_name='Ссылка', default='www.piton.org')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, verbose_name='Course', **NULLABLE,
                               related_name='lesson')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

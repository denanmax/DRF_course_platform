from django.db import models
from django.utils.timezone import now

from course.models import Course
from lessons.models import Lesson, NULLABLE
from users.models import User


# Create your models here.
class Payment(models.Model):
    PAYMENT_TYPE = (
        ('cash', 'наличные'),
        ('transfer', 'перевод')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    date_payment = models.DateField(default=now)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='урок', **NULLABLE)
    payment_amount = models.PositiveIntegerField(verbose_name='сумма оплаты')
    payment_type = models.CharField(choices=PAYMENT_TYPE, verbose_name='тип оплаты', max_length=10)

    stripe_payment_id = models.CharField(max_length=255, verbose_name='id платежа stripe', **NULLABLE,)
    status = models.CharField(max_length=10, verbose_name='статус платежа', default='open',)
    stripe_payment_url = models.TextField(verbose_name='id платежа stripe', **NULLABLE, )

    def __str__(self):
        return f'{self.user} {self.payment_type} {self.date_payment}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
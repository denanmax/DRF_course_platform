from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from course.models import Course, Subscriptions

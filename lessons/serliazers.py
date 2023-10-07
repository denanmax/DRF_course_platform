from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from course.models import Subscriptions
from course.validators import LinkValidator
from lessons.models import Lesson


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [LinkValidator(field='url')]


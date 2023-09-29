from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from course.models import Course
from lessons.models import Lesson


class CourseSerializer(serializers.ModelSerializer):
    number_of_lessons = serializers.SerializerMethodField(read_only=True)
    lessons = SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

    def get_number_of_lessons(self, instance):
        return instance.lesson.all().count()

    def get_lessons(self, course):
        return [el.name for el in Lesson.objects.filter(course=course)]

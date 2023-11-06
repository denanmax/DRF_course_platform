from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from course.models import Subscriptions
from course.validators import LinkValidator
from lessons.models import Lesson
from payment.models import Payment
from payment.serializers import PaymentSerializer


class LessonSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [LinkValidator(field='url')]

    def create(self, validated_data):
        if validated_data.get('payment_amount'):
            print(validated_data)
            payment = validated_data.pop('payment_amount')
            lesson_item = Lesson.objects.create(**validated_data)
            for m in payment:
                Payment.objects.create(**m, lesson=lesson_item)

            return lesson_item
        return validated_data

class LessonPaymentSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'


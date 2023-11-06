from django.conf import settings

from rest_framework import filters, status, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from course.services import get_lesson_or_course
from payment.models import Payment
from payment.serializers import PaymentSerializer


# Create your views here.
class PaymentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['date_payment']
    search_fields = ['course__name', 'lesson__name', 'payment_type']


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_type')
    ordering_fields = ('date_payment', )
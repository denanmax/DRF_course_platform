import stripe
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
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

class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):

        print(request.data.get('payment'))
        payment_data = request.data.get('payment')

        if payment_data is None:
            return Response({'error': 'Payment data is missing.'}, status=status.HTTP_400_BAD_REQUEST)

        lesson_id = payment_data.get('lesson')
        course_id = payment_data.get('course')

        if lesson_id is None or course_id is None:
            return Response({'error': 'Lesson or course ID is missing in payment data.'},
                            status=status.HTTP_400_BAD_REQUEST)

        product = get_lesson_or_course(lesson_id, course_id)

        stripe.api_key = settings.PAY_API_KEY

        response = stripe.PaymentIntent.create(
            amount=payment_data.get('payment'),
            currency="rub",
            automatic_payment_methods={"enabled": True},
        )
        stripe.PaymentIntent.confirm(
            response.id,
            payment_type='pm_card_visa',
        )
        user = self.request.user
        payment_id = response.id
        data = {
            "stripe_payment_id": payment_id,
            "user": user,
            "status": response.status,
            "stripe_payment_url": response.url
        }
        print(response)
        serializer = self.get_serializer(data=data)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_type')
    ordering_fields = ('date_payment', )
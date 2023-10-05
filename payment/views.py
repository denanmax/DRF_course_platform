from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet


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

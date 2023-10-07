from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from course.models import Course, Subscriptions
from course.paginators import ViewsPaginator
from course.permissions import IsNotModerator
from course.serliazers import CourseSerializer, SubscriptionsSerializer


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsNotModerator]
    serializer_class = CourseSerializer
    pagination_class = ViewsPaginator
    queryset = Course.objects.all()

    def get_queryset(self):
        if self.request.user.groups.filter(name='Moderator').exists():
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

class SubscriptionsViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionsSerializer
    queryset = Subscriptions.objects.all()

    def perform_create(self, serializer):
        new_subscription = serializer.save()
        new_subscription.user = self.request.user
        new_subscription.save()
from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from course.paginators import ViewsPaginator
from course.permissions import IsNotModerator, IsOwnerOrModerator
from lessons.models import Lesson
from lessons.serliazers import LessonSerializer, LessonPaymentSerializer
from payment.models import Payment


class LessonCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsNotModerator]
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = LessonSerializer
    pagination_class = ViewsPaginator
    queryset = Lesson.objects.all()

    # def get_queryset(self):
    #     if self.request.user.groups.filter(name='Moderator').exists() or self.request.user.is_superuser:
    #         return Lesson.objects.all()
    #     return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def perform_update(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()

class LessonDestroyAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrModerator, IsNotModerator]
    queryset = Lesson.objects.all()


class LessonPaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.filter(lesson__isnull=False)
    serializer_class = LessonPaymentSerializer

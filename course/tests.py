from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from course.models import Course, Subscriptions
from lessons.models import Lesson
from users.models import User


class LessonCRUDTestCases(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@test.com')
        self.user.set_password('1234')
        self.user.save()
        self.course = Course.objects.create(name='TestCourse', description='TestCourseDescription')
        self.lesson = Lesson.objects.create(
            name='TestLesson',
            description='TestLessonDescription',
            url='https://www.youtube.com',
            owner=self.user,
            course=self.course,
        )
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        data = {
            'name': 'testT',
            'description': 'test',
            'url': 'https://www.youtube.com/feed/history',
            'course': self.course.pk,
            'owner': self.user.pk
        }

        response = self.client.post(
            '/lesson/create/',
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Lesson.objects.all().exists(),
            {'id': 2, 'name': 'testT', 'description': 'test',
             'url': 'https://www.youtube.com', 'owner': 1, 'course': 1}
        )

    def test_list_lesson(self):
        response = self.client.get(
            '/lesson/',
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        print(response.json().get("results"))

        self.assertEqual(
            response.json().get("results"),
            [{'id': self.lesson.pk, 'name': 'TestLesson', 'description': 'TestLessonDescription',
              'preview': None, 'url': 'https://www.youtube.com', 'owner': self.user.pk, 'course': self.course.pk}])

    def test_lesson_update(self):
        data = {
            'name': 'TestLessonUpdated',
            'description': 'TestLessonDescriptionUpdated',
        }

        response = self.client.put(
            path=f'/lesson/update/{self.lesson.pk}/', data=data,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        response = response.json()

        self.assertEqual(response.get('name'), 'TestLessonUpdated')
        self.assertEqual(response.get('description'), 'TestLessonDescriptionUpdated')
        self.assertEqual(response.get('preview'), None)
        self.assertEqual(response.get('url'), 'https://www.youtube.com')
        self.assertEqual(response.get('course'), self.course.pk)
        self.assertEqual(response.get('owner'), self.user.pk)

    def test_lesson_delete(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            f'/lesson/delete/{self.lesson.pk}/',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Lesson.objects.all().exists(),
        )

    def tearDown(self) -> None:
        self.user.delete()
        self.course.delete()
        self.lesson.delete()


class SubscriptionsTestCase(APITestCase):
    def setUp(self) -> None:
        self.course = Course.objects.create(name='test')
        self.user = User.objects.create(email='test@test.ru', password='1234')
        self.data = {
            'user': self.user,
            'course': self.course,
        }

        self.subscription = Subscriptions.objects.create(**self.data)
        self.client.force_authenticate(user=self.user)

    def test_create_subscription(self):
        data = {
            'user': self.user.pk,
            'course': self.course.pk,
        }
        subscription_url = '/subscriptions/'
        print(subscription_url)

        response = self.client.post(subscription_url, data)

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )

        self.assertEqual(
            Subscriptions.objects.all().count(), 2
        )

    def test_list_subscriptions(self):
        subscription_url = '/subscriptions/'
        response = self.client.get(subscription_url)
        print(response.json())

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data), 1
        )

    def test_retrieve_subscription(self):
        subscription_detail_url = reverse('course:subscriptions-detail', kwargs={'pk': self.subscription.pk})

        response = self.client.get(subscription_detail_url)

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        self.assertEqual(
            response.data['user'], self.subscription.user.pk
        )

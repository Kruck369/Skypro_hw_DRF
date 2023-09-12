from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Course, Lesson, Subscription
from users.models import User


class CourseTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_superuser(email='1@test.com', password='testpassword')

        self.course = Course.objects.create(title='Test Course', description='Test Description', owner=self.user)

    def test_crud_lessons(self):
        self.client.force_authenticate(user=self.user)

        # Создаем урок
        lesson_data = {'title': 'Lesson 1', 'description': 'Lesson Description', 'course': self.course.id}
        response = self.client.post(f'/lesson/create/', lesson_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 1)

        # Получаем урок
        lesson_id = response.data['id']
        response = self.client.get(f'/lesson/{lesson_id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Обновляем урок
        updated_lesson_data = {'title': 'Updated Lesson', 'description': 'Updated Description'}
        response = self.client.put(f'/lesson/update/{lesson_id}/', updated_lesson_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.get(id=lesson_id).title, 'Updated Lesson')

        # Удаляем урок
        response = self.client.delete(f'/lesson/delete/{lesson_id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_subscription(self):
        # Создаем клиента для отправки API запросов и авторизуем пользователя
        self.client.force_authenticate(user=self.user)

        # Подписываем пользователя на курс
        subscribe_url = f'/courses/{self.course.id}/subscribe/'
        response = self.client.post(subscribe_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.count(), 1)

        # Проверяем, что пользователь подписан на курс
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

        # Отменяем подписку пользователя на курс
        unsubscribe_url = f'/courses/{self.course.id}/unsubscribe/'
        response = self.client.delete(unsubscribe_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Subscription.objects.count(), 0)

        # Проверяем, что пользователь больше не подписан на курс
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

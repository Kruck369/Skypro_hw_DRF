from django.core.management.base import BaseCommand
from django.utils import timezone

from users.models import User
from courses.models import Payment, Course, Lesson
from datetime import datetime


class Command(BaseCommand):
    help = 'Создайте пример проведенных платежей'

    def handle(self, *args, **options):
        user1 = User.objects.get(email='123@mail.ru')
        user2 = User.objects.get(email='234@mail.ru')

        course1 = Course.objects.get(pk=2)
        lesson1 = Lesson.objects.get(pk=2)

        Payment.objects.create(
            user=user1,
            payment_date=timezone.make_aware(datetime(2023, 9, 5, 12, 0, 0), timezone.get_current_timezone()),
            payed_course=course1,
            payment_amount=12500.00,
            payment_method='cash'
        )

        Payment.objects.create(
            user=user2,
            payment_date=timezone.make_aware(datetime(2023, 9, 5, 12, 0, 0), timezone.get_current_timezone()),
            payed_lesson=lesson1,
            payment_amount=125.00,
            payment_method='transfer'
        )

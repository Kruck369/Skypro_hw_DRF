from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from courses.models import Course, Subscription
import logging

from users.models import User

logger = logging.getLogger(__name__)


@shared_task
def send_update(user_email, course_title):
    subject = f'Обновление курса "{course_title}"'
    message = f'Уважаемые пользователи! Курс {course_title} был обновлен. Пожалуйста, ознакомьтесь с обновлениями.'
    from_email = 'tripicto369@gmail.com'
    recipient_list = [user_email]

    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=False
    )


@shared_task
def check_and_lock_inactive_users():
    threshold_date = timezone.now() - timezone.timedelta(days=30)

    inactive_users = User.objects.filter(last_login__lte=threshold_date, is_active=True)

    for user in inactive_users:
        user.is_active = False
        user.save()

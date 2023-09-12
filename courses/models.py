from django.db import models

from config import settings
from users.models import NULLABLE, User


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    preview = models.ImageField(upload_to='courses/', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание')
    video_url = models.CharField(max_length=250, verbose_name='ссылка на видео', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:

        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    preview = models.ImageField(upload_to='courses/', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание')
    lesson = models.ManyToManyField(Lesson, verbose_name='уроки', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:

        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    payment_date = models.DateTimeField(verbose_name='дата оплаты')
    payed_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='оплаченный курс', null=True)
    payed_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='оплаченный урок', null=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[('cash', 'Наличные'), ('transfer', 'Перевод на счёт')])

    def __str__(self):
        return f'{self.user} {self.payment_amount}'


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
    is_subscribed = models.BooleanField(default=False, verbose_name='статус подписки')

    def __str__(self):
        return f'{self.user}: "{self.course}"'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

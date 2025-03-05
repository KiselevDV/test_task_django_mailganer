# coding=utf-8
from django.db import models
from django.utils import timezone


class Subscriber(models.Model):
    first_name = models.CharField(max_length=50, verbose_name=u'Имя')
    last_name = models.CharField(max_length=70, verbose_name=u'Фамилия')
    email = models.EmailField(unique=True, verbose_name=u'Email')
    birth_date = models.DateField(null=True, blank=True, verbose_name=u'Дата рождения')
    email_opened = models.BooleanField(default=False, verbose_name=u'Письмо открыто')
    opened_at = models.DateTimeField(null=True, blank=True, verbose_name=u'Время открытия')

    class Meta:
        verbose_name=u'Подписчик'
        verbose_name_plural=u'Подписчики'
        ordering = ('first_name', 'last_name')

    def __str__(self):
        return '{} {} ({})'.format(self.first_name, self.last_name, self.email)


class EmailTemplate(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'Название письма')
    subject = models.CharField(max_length=255, verbose_name=u'Тема письма')
    body = models.TextField(
        verbose_name=u'Шаблон письма',
        help_text=u'Используйте {{ first_name }}, {{ last_name }}, {{ birth_data }} для подстановки данных'
    )

    class Meta:
        verbose_name=u'Шаблон письма'
        verbose_name_plural=u'Шаблоны писем'

    def __str__(self):
        return self.subject


class EmailCampaign(models.Model):
    template = models.ForeignKey(EmailTemplate, on_delete=models.CASCADE, verbose_name=u'Шаблон')
    subscribers = models.ManyToManyField(Subscriber, verbose_name=u'Подписчики')
    scheduled_time = models.DateTimeField(default=timezone.now, verbose_name=u'Время отправки')
    is_sent = models.BooleanField(default=False, verbose_name=u'Отправлено')

    class Meta:
        verbose_name=u'Рассылка'
        verbose_name_plural=u'Рассылки'
        ordering = ('-scheduled_time', )

    def __str__(self):
        return ('Рассылка: ' + self.template.subject + ' (' +
                ('Отправлено' if self.is_sent else 'Ожидает отправки') + ')')

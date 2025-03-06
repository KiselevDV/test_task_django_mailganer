# coding=utf-8
import random

from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from emails.models import Subscriber, EmailTemplate, SendingEmails


class Command(BaseCommand):
    help = u'Заполнить БД тестовыми данными'

    def handle(self, *args, **kwargs):
        self.create_subscribers(50)
        self.create_email_templates(5)
        self.create_email_campaigns(2)
        self.stdout.write(self.style.SUCCESS(u'БД успешно заполнена!'))

    def create_subscribers(self, count):
        subscribers = []
        existing_emails = set(Subscriber.objects.values_list('email', flat=True))

        for i in range(count):
            email = u'user{}@example.com'.format(i)
            if email in existing_emails:
                continue

            subscribers.append(Subscriber(
                first_name=u'Имя {}'.format(i),
                last_name=u'Фамилия {}'.format(i),
                email=email,
                birth_date=datetime.today() - timedelta(days=random.randint(6000, 20000)),
                email_opened=random.choice([True, False]),
                opened_at=now() if random.choice([True, False]) else None
            ))

        Subscriber.objects.bulk_create(subscribers)
        self.stdout.write(self.style.SUCCESS(u'Создано {} подписчиков.'.format(len(subscribers))))

    def create_email_templates(self, count):
        templates = [
            EmailTemplate(
                name=u'Шаблон {}'.format(i),
                subject=u'Тема письма {}'.format(i),
                body=u'Привет, {{ first_name }}! Это тестовый шаблон {{ number }}.'.format(number=i)
            )
            for i in range(count)
        ]
        EmailTemplate.objects.bulk_create(templates)
        self.stdout.write(self.style.SUCCESS(u'Создано {} шаблонов писем.'.format(count)))

    def create_email_campaigns(self, count):
        subscribers = list(Subscriber.objects.all())
        templates = list(EmailTemplate.objects.all())

        if not subscribers or not templates:
            self.stdout.write(self.style.WARNING(u'Недостаточно данных для создания кампаний.'))
            return

        campaigns = []
        for i in range(count):
            campaign = SendingEmails.objects.create(
                template=random.choice(templates),
                scheduled_time=now() + timedelta(days=random.randint(1, 30))
            )
            campaign.subscribers.set(random.sample(subscribers, min(len(subscribers), 10)))
            campaigns.append(campaign)

        self.stdout.write(self.style.SUCCESS(u'Создано {} email-кампаний.'.format(len(campaigns))))

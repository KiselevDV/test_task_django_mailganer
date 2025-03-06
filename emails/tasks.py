# -*- coding: utf-8 -*-
import logging

from celery import task
from django.core.mail import send_mail
# from string import Template

from emails.models import SendingEmails

logger = logging.getLogger(__name__)


@task
def test_task():
    print(u'***** Проверка работы Celery *****')
    return u'***** Celery запущен и работает *****'


def get_domain():
    domain = 'https://mailganer.com'
    return domain


@task(bind=True, max_retries=3)
def send_email_campaign(self, campaign_id):
    """Отправка email-рассылки подписчикам"""

    try:
        campaign = SendingEmails.objects \
            .select_related('template') \
            .prefetch_related('subscribers') \
            .get(id=campaign_id)

        logger.info(u'Запуск рассылки: "{}" ID: {}'.format(campaign.template.subject, campaign_id))

        errors = 0
        for subscriber in campaign.subscribers.all():
            try:
                # track_url = (
                #     '{domain}/emails/track/{subscriber_id}/'
                #     .format(domain=get_domain(), subscriber_id=subscriber.id)
                # )
                # template = Template(campaign.template.body)
                # body = template.safe_substitute(
                #     first_name=subscriber.first_name,
                #     last_name=subscriber.last_name,
                #     birth_date=subscriber.birth_date
                # )
                track_url = '{}/emails/track/{}/'.format(get_domain(), subscriber.id)
                body = campaign.template.body.format(
                    first_name=subscriber.first_name or '',
                    last_name=subscriber.last_name or '',
                    birth_date=subscriber.birth_date or ''
                )
                body += "<img src='{}' width='1' height='1' style='display:none;'/>".format(track_url)

                send_mail(
                    subject=campaign.template.subject,
                    message='',
                    from_email='no-reply@example.com',
                    recipient_list=[subscriber.email],
                    html_message=body
                )
            except Exception as e:
                logger.error(u'Ошибка при отправке на {}: {}'.format(subscriber.email, e))
                errors += 1

        campaign.is_sent = errors == 0
        campaign.save()

    except SendingEmails.DoesNotExist:
        logger.error(u'Кампания с ID {} не найдена.'.format(campaign_id))
    except Exception as e:
        logger.critical(u'Ошибка: {}'.format(e))
        raise self.retry(exc=e)

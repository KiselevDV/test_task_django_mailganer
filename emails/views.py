# coding=utf-8
import logging

from datetime import timedelta

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.utils.dateparse import parse_datetime
from django.utils.timezone import now

from emails.models import EmailCampaign, EmailTemplate, Subscriber

logger = logging.getLogger(__name__)


def campaign_page(request):
    """Главная страница с формой для создания рассылок"""

    templates = EmailTemplate.objects.all()
    subscribers = Subscriber.objects.all()
    return render(
        request, 'emails/base.html',
        {'templates': templates, 'subscribers': subscribers}
    )


def create_campaign(request):
    """Обработчик AJAX-запроса для создания email-рассылки"""

    if request.method == "POST":
        template_id = request.POST.get('template_id')
        if not template_id:
            return JsonResponse({'success': False, 'error': u'Не указан шаблон для рассылки'})

        try:
            template = EmailTemplate.objects.get(id=template_id)
        except EmailTemplate.DoesNotExist:
            return JsonResponse({'success': False, 'error': u'Шаблон не найден'})

        scheduled_time = parse_datetime(request.POST.get('scheduled_time'))
        if scheduled_time is None:
            return JsonResponse({'success': False, 'error': u'Некорректная дата'})

        if scheduled_time < now():
            scheduled_time = now() + timedelta(minutes=1)

        campaign = EmailCampaign.objects.create(
            template=template,
            scheduled_time=scheduled_time
        )

        subscriber_ids = request.POST.getlist('subscribers')
        if not subscriber_ids:
            return JsonResponse({'success': False, 'error': u'Не выбраны подписчики'})

        existing_subscribers = set(Subscriber.objects.filter(id__in=subscriber_ids).values_list('id', flat=True))
        invalid_subscribers = set(map(int, subscriber_ids)) - existing_subscribers

        if invalid_subscribers:
            return JsonResponse({
                'success': False,
                'error': u'Некорректные ID подписчиков: {}'.format(list(invalid_subscribers))
            })

        campaign.subscribers.set(existing_subscribers)

        return JsonResponse({'success': True, 'campaign_id': campaign.id})
    return JsonResponse({'success': False, 'error': u'Метод не поддерживается'})


def track_email_open(request, subscriber_id):
    """Обработчик для отслеживания открытия письма"""

    try:
        subscriber = Subscriber.objects.get(id=subscriber_id)
        if not subscriber.email_opened:
            subscriber.email_opened = True
            subscriber.opened_at = now()
            subscriber.save()
            logger.info(u'Открытие письма подписчиком: {}'.format(subscriber.email))
    except Subscriber.DoesNotExist:
        logger.warning(u'Неизвестный ID подписчика: {}'.format(subscriber_id))

    transparent_pixel = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9'
        b'\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b'
    )

    return HttpResponse(transparent_pixel, content_type='image/gif')

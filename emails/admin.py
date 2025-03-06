# -*- coding: utf-8 -*-
from django.contrib import admin
from emails.models import Subscriber, EmailTemplate, SendingEmails


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'birth_date', 'email_opened', 'opened_at')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('birth_date', 'email_opened')
    readonly_fields = ('opened_at',)
    list_editable = ('email_opened',)

    actions = ['mark_email_opened']

    def mark_email_opened(self, request, queryset):
        queryset.update(email_opened=True)

    mark_email_opened.short_description = u'Пометить как открывших письмо'


class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('subject', 'preview_body')

    def preview_body(self, obj):
        return obj.body[:50] + '...' if len(obj.body) > 50 else obj.body

    preview_body.short_description = u'Превью тела письма'


class SendingEmailsAdmin(admin.ModelAdmin):
    list_display = ('template', 'scheduled_time', 'is_sent', 'subscriber_count')
    list_filter = ('is_sent', 'scheduled_time')
    search_fields = ('template__subject',)
    readonly_fields = ('is_sent',)
    autocomplete_fields = ('template', 'subscribers')

    actions = ['send_campaigns']

    def subscriber_count(self, obj):
        return obj.subscribers.count()

    subscriber_count.short_description = u'Количество подписчиков'

    def send_campaigns(self, request, queryset):
        for campaign in queryset:
            if not campaign.is_sent:
                campaign.is_sent = True
                campaign.save()
        self.message_user(request, u'Выбранные рассылки отправлены')

    send_campaigns.short_description = u'Отправить выбранные рассылки'


admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(EmailTemplate, EmailTemplateAdmin)
admin.site.register(SendingEmails, SendingEmailsAdmin)

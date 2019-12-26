# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from api.models import AuthLog
import datetime
from django.conf import settings


class Command(BaseCommand):

    def handle(self, *args, **options):
        start = datetime.datetime.now() - datetime.timedelta(minutes=settings.STORE_MINUTES_OF_AUTH_LOG or 60)
        end = datetime.datetime.now()
        AuthLog.objects.exclude(attempt_date__range=(start, end)).delete()

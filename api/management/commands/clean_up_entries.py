# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from api.models import Entry
import datetime


class Command(BaseCommand):

    def handle(self, *args, **options):
        for entry in Entry.objects.filter(pinned=False):
            if entry.delete_on.date() <= datetime.datetime.now().date():
                self.stdout.write(self.style.SUCCESS('Removing "{0}"'.format(entry)))
                entry.delete()

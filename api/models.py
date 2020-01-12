# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
import datetime


class Entry(models.Model):

    """
    Stores shared elements. Basic objects.
    """

    desc = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateTimeField('Date of creation', auto_now_add=True)
    url = models.CharField(max_length=2000, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
    pinned = models.BooleanField(default=False)
    delete_on = models.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(days=7), blank=True, null=True)
    img_path = models.ImageField(upload_to='images', blank=True, null=True)
    preview_img_path = models.ImageField(upload_to='images/preview', blank=True, null=True)
    icon = models.ImageField(upload_to='images/icons/', blank=True, null=True)

    def delete(self):
        for f in [self.img_path, self.preview_img_path, self.icon]:
            if bool(f):
                f.delete()
        super().delete()

    def __str__(self):
        return '{0}, {1}'.format(self.desc, self.url)

    def extend_with_delete_date(self):
        """
        Calculate and append delete date to show in template.
        """
        today = datetime.datetime.now().date()
        if self.delete_on is not None:
            delta = self.delete_on.date() - today
            delta_days = delta.days
            if delta_days == 0:
                self.delete_date = 'Today!'
            elif delta_days == 1:
                self.delete_date = 'Tomorrow'
            elif delta_days > 1:
                self.delete_date = 'after {0} days'.format(delta_days)

    @staticmethod
    def get_last_four():
        query = list(Entry.objects.order_by('date'))
        if len(query) > settings.ROLLER_LENGTH - 1:
            return query[-settings.ROLLER_LENGTH:]
        return None

    @staticmethod
    def get_previous_entries(current_entry_id):
        """
        Return previous entries whose id is lower than current_entry_id.
        If end is reached adds Entry from the beginning.
        :param current_entry_id: pk, integer
        :return: QuerySet limited to 4 items
        """
        query = list(Entry.objects.filter(pk__lt=current_entry_id))
        if len(query) > settings.ROLLER_LENGTH - 1:
            return query[-settings.ROLLER_LENGTH:]
        elif len(query) < settings.ROLLER_LENGTH:
            not_enough = settings.ROLLER_LENGTH - len(query)
            query = query + list(Entry.objects.all())[-not_enough:]
        return query

    @staticmethod
    def get_next_entries(current_entry_id):
        """
        Same as get_previous_entries but in forward
        """
        query = list(Entry.objects.filter(pk__gt=current_entry_id))
        if len(query) > settings.ROLLER_LENGTH - 1:
            return query[0:settings.ROLLER_LENGTH]
        elif len(query) < settings.ROLLER_LENGTH:
            not_enough = settings.ROLLER_LENGTH - len(query)
            query = query + list(Entry.objects.all())[0:not_enough]
        return query


class AuthLog(models.Model):

    remote_address = models.GenericIPAddressField(unpack_ipv4=True)
    attempt_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'from:{0} at {1}'.format(self.remote_address, self.attempt_date)

    @staticmethod
    def get_attempts_by_ip_address(ip_address):
        start = datetime.datetime.now() - datetime.timedelta(minutes=settings.ATTEMPTS_INTERVAL or 5)
        end = datetime.datetime.now()
        return AuthLog.objects.filter(remote_address=ip_address, attempt_date__range=(start, end)).count()

# -*- coding: utf-8 -*-

from django.contrib import admin
from django.shortcuts import redirect
from .models import Entry, AuthLog


class EntryAdmin(admin.ModelAdmin):

    def response_change(self, request, obj):
        super(EntryAdmin, self).response_change(request, obj)
        return redirect('index')


class AuthLogAdmin(admin.ModelAdmin):

    readonly_fields = ['remote_address', 'attempt_date']


admin.site.register(Entry, EntryAdmin)
admin.site.register(AuthLog, AuthLogAdmin)

# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.exceptions import PermissionDenied
from .models import Entry
from .forms import EntryForm
import os
from .request_utils import NewEntryProcessor, get_first_and_last_ids, IconGetter


def log_out(request):
    logout(request)
    return render(request, 'logout.html')


@login_required
def index(request):
    if request.method == 'GET':
        form = EntryForm()

        last_four = Entry.get_last_four() or list(Entry.objects.all())
        [i.extend_with_delete_date() for i in last_four]

        roller_first_item_id, roller_last_item_id = get_first_and_last_ids(last_four)

        context = {'entries': last_four, 'days_to_live': settings.DAYS_TO_LIVE, 'form': form,
                   'roller_start': roller_first_item_id, 'roller_end': roller_last_item_id,
                   'messages_ttl': settings.MESSAGES_TIME_TO_LIVE}

        if 'Android' in request.META['HTTP_USER_AGENT']:
            last_four.reverse()
            return render(request, 'm_index.html', context)
        return render(request, 'index.html', context)
    else:
        return redirect('index')


@login_required
def get_prev(request):
    """
    Return container(div) with previous Entries
    """
    if request.method == 'POST':
        entry_id = request.POST.get('entry_id')
        previous_entries = Entry.get_previous_entries(entry_id)
        roller_start, roller_end = get_first_and_last_ids(previous_entries)

        return render(request, 'content.html',
                      {'entries': previous_entries, 'roller_start': roller_start, 'roller_end': roller_end})
    else:
        raise PermissionDenied


@login_required
def get_next(request):
    """
    Same as get_prev but in forward
    """
    if request.method == 'POST':
        entry_id = request.POST.get('entry_id')
        next_entries = Entry.get_next_entries(entry_id)
        roller_start, roller_end = get_first_and_last_ids(next_entries)
        return render(request, 'content.html',
                      {'entries': next_entries, 'roller_start': roller_start, 'roller_end': roller_end})
    else:
        raise PermissionDenied


@login_required
def add_entry(request):
    if request.method == 'POST':
        form = EntryForm(request.POST, request.FILES)
        if form.is_valid():
            new_entry_handler = NewEntryProcessor(form, request)
            user_object, description, url, pinned, delete_on, img, preview_img = new_entry_handler.extract()
            icon_img = IconGetter(url).get_icon()

            if url or img:
                Entry.objects.create(desc=description,
                                     url=url,
                                     owner=user_object,
                                     pinned=pinned,
                                     delete_on=delete_on,
                                     img_path=img,
                                     preview_img_path=preview_img,
                                     icon=icon_img)
                messages.add_message(request, messages.INFO, 'New entry added!')
            else:
                messages.add_message(request, messages.INFO,
                                     'Error! URL or image are empty. Entry wasn`t added!')
        else:
            return render(request, 'index.html', {'form': form})
    return redirect('index')


@login_required
def delete_entry(request, entry_id):
    """
    Delete Entry and all related images and icon file.
    :param request: Django Request
    :param entry_id: int
    """
    for entry in Entry.objects.filter(id=entry_id):
        entry.delete()

    messages.add_message(request, messages.INFO, 'Entry was deleted!')
    return redirect('index')

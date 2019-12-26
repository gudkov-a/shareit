# -*- coding: utf-8 -*-

from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from api.images_tools import convert_to_pil
import datetime


def validate_delete_date_value(delete_date_value):
    if not delete_date_value.isdigit():
        raise ValidationError('Delete data is not a digit!')
    if int(delete_date_value) < 1:
        raise ValidationError('Invalid time to live')


class EntryForm(forms.Form):
    new_desc = forms.CharField(required=False)
    new_url = forms.CharField(required=False,
                              validators=[validators.URLValidator()],)
    text = forms.CharField(required=False)
    pinned = forms.BooleanField(required=False, initial=True)
    delete_on = forms.ChoiceField(required=False,
                                  widget=forms.Select,
                                  choices=[(i, i) for i in range(0, 31)],
                                  initial=7,
                                  validators=[validate_delete_date_value])
    img_path = forms.ImageField(required=False)

    # CSS attributes
    new_desc.widget.attrs.update({'class': 'new_desc', 'placeholder': 'Short description'})
    new_url.widget.attrs.update({'class': 'new_url', 'placeholder': 'URL'})
    text.widget.attrs.update({'class': 'new_text', 'placeholder': 'text here'})
    pinned.widget.attrs.update({'class': 'pinned'})
    delete_on.widget.attrs.update({'class': 'ttl'})
    img_path.widget.attrs.update({'class': 'new_img'})

    def clean_delete_on(self):
        """
        Convert value of time-to-live to datetime object
        :return: datetime
        """
        data = self.cleaned_data.get('delete_on')
        if data:
            data = datetime.datetime.now().date() + datetime.timedelta(days=int(data))
        else:
            data = datetime.datetime.now().date() + datetime.timedelta(days=7)
        return data

    def clean(self):
        """
        Common validation of the form
        :return:
        """
        if not self.cleaned_data.get('img_path') and not self.cleaned_data.get('new_url'):
            raise ValidationError('Form is empty. Please add URL or image.')
        return self.cleaned_data

# -*- coding: utf-8 -*-

from .images_tools import ImageProcessor, convert_to_pil, convert_to_uploaded_file
from django.contrib.auth.models import User
from django.contrib import messages
from urllib.request import urlopen, Request
from urllib.error import URLError
import re
from shareit.decorators import skip_in_test


class NewEntryProcessor:
    """
    Extract objects from form
    """

    def __init__(self, form, request, pil_converter=convert_to_pil):
        """
        :param form: instance of EntryForm
        :param request: django Request object
        """
        self.__form = form
        self.__request = request
        self.__pil_converter = pil_converter

    def extract(self):
        user_object = self.__get_user()

        description = self.__get_description()

        url = self.__get_url()

        pinned = self.__get_is_pinned()

        if pinned:
            delete_on = None
        else:
            delete_on = self.__get_delete_date()

        img = self.__get_image()
        preview_img = None
        if img:
            preview_img = self.__get_preview_image(img)

        return user_object, description, url, pinned, delete_on, img, preview_img

    def __get_user(self):
        return User.objects.get(username=self.__request.user)

    def __get_image(self):
        return self.__form.cleaned_data.get('img_path')

    def __get_preview_image(self, img):
        pil_object = self.__pil_converter(img.read())
        img_processor = ImageProcessor(pil_object, img.name)
        preview_img = img_processor.get_preview_img()
        return preview_img

    def __get_description(self):
        description = self.__form.cleaned_data.get('new_desc') or ''
        if len(description) > 100:
            description = self.__trim_description(description)
        return description

    def __trim_description(self, desc):
        desc = desc[0: 100] + '...'
        messages.add(self.__request, messages.INFO, 'Description was reduced to 100 symbols.')
        return desc

    def __get_is_pinned(self):
        return self.__form.cleaned_data.get('pinned')

    def __get_delete_date(self):
        return self.__form.cleaned_data.get('delete_on')

    def __get_url(self):
        return self.__form.cleaned_data.get('new_url')


class IconGetter:
    """
    Get icon file of the page
    """

    def __init__(self, url, converter=convert_to_uploaded_file, pil_converter=convert_to_pil):
        self.__url = url
        self.__converter = converter
        self.__pil_converter = pil_converter

    def __get_user_agent(self):
        return 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                             'Chrome/35.0.1916.47 Safari/537.36'

    def __create_request(self, url):
        return Request(url, data=None, headers={'User-Agent': self.__get_user_agent()})

    def __get_content(self):
        request = self.__create_request(self.__url)
        result = urlopen(request)
        if result.getcode() == 200:
            return result.read()

    def __url_is_not_full(self, path_to_icon):
        if path_to_icon.startswith('/'):
            return True
        return False

    def parse_content(self, raw_content):
        content = raw_content.decode('utf-8')

        link_pattern = """<link (.*?)>"""
        href_pattern = """href=['|"](?P<url>.+\.\w{3,5})['|"]"""
        site_root_url_pattern = """https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}"""

        links = re.findall(link_pattern, content)

        for link in links:
            result = re.search(href_pattern, link)
            if result and 'icon' in result.group('url'):
                href_string = result.group('url')
                if self.__url_is_not_full(href_string):
                    root_url = re.search(site_root_url_pattern, self.__url)
                    if root_url:
                        return root_url.group(0) + href_string  # .replace('//', '/')
                else:
                    return href_string
        return None

    def __fetch_icon_file(self, icon_url):
        if icon_url:
            request = self.__create_request(icon_url)
            result = urlopen(request)
            if result.getcode() == 200:
                return result.read()

    def __get_name(self):
        symbols_to_exclude = [':', '/', '.']
        excluded = ''

        _, without_scheme = self.__url.split('://')

        for symbol in without_scheme:
            if symbol not in symbols_to_exclude:
                excluded += symbol

        if len(without_scheme) > 10:
            return without_scheme[:10]

    def __get_extension(self, path_to_icon):
        return path_to_icon.split('.')[-1]

    @skip_in_test
    def get_icon(self):
        if self.__url is None:
            return None

        raw_page = self.__get_content()
        path_to_icon = self.parse_content(raw_page)
        if path_to_icon:
            icon_file = self.__fetch_icon_file(path_to_icon)
            name = self.__get_name() + '.' + self.__get_extension(path_to_icon)
            uploaded_file = self.__converter(self.__pil_converter(icon_file), name)
            return uploaded_file


def get_first_and_last_ids(list_of_items):
    """
    Return ids of first and last entries in list of Entries.
    Consumer - JavaScript roller.
    """
    if len(list_of_items) > 0:
        return list_of_items[0].id, list_of_items[-1].id
    return None, None

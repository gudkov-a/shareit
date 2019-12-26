# -*- coding: utf-8 -*-*

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from PIL import Image


def convert_to_pil(img):
    return Image.open(BytesIO(img))


def convert_to_uploaded_file(pil_object, name):
    """
    :param pil_object: instance of Pillow.Image class
    :param name: 'string'
    :return: Django InMemoryUploadedFile
    """
    in_memory_file = BytesIO()
    pil_object.save(in_memory_file, format=pil_object.format)
    in_memory_file.seek(0)
    uploaded_file = InMemoryUploadedFile(in_memory_file, None, name, pil_object.format,
                                         in_memory_file.__sizeof__(), None)
    return uploaded_file


class ImageProcessor:

    def __init__(self, pil_object, name, converter=convert_to_uploaded_file):
        """
        Creates preview image
        :param pil_object: instance of PIL
        """
        self.__img = pil_object
        self.__name = name
        self.__converter = converter

    def get_preview_img(self):
        if self.img_is_large():
            preview = self.reduce_size()
        else:
            preview = self.__img

        converted = self.__converter(preview, self.__name)
        return converted

    def reduce_size(self):
        resized = self.__img.resize(settings.PREVIEW_IMAGE_SIZE)
        resized.format = self.__img.format
        return resized

    def img_is_large(self):
        if self.__img.size > settings.PREVIEW_IMAGE_SIZE:
            return True
        return False

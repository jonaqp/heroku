import os
import sys

from PIL import Image
from django.conf import settings
from django.core.files.storage import default_storage as storage

from core.utils import resize_image

prefix_profile = 'uploads/profiles/'
prefix_container = 'uploads/container/'
prefix_upload_company = 'upload/logo_company'


def upload_location_profile(instance, filename):
    file_base, extension = filename.split(".")
    path_file = u"{0:s}/{1:s}.{2:s}".format(
        str(instance.user.id), str(instance.id), extension)
    return os.path.join(prefix_profile, path_file)


def upload_location_trip(instance, filename):
    file_base, extension = filename.split(".")
    path_file = u"{0:s}/shellcatch_{1:s}_{2:s}-{3:s}.{4:s}".format(
        str(instance.container.identifier_mac),
        str(instance.container.identifier_mac),
        str(instance.datetime_image.strftime("%Y_%m_%d")),
        str(instance.datetime_image.strftime("%H-%M-%S")),
        extension).lower()
    return os.path.join(prefix_container, path_file)


def upload_location_company(instance, filename):
    file_base, extension = filename.split(".")
    return "{0}/{1}.{2}".format(
        prefix_upload_company, instance.name, extension)


def handle_upload_remove(current_image):
    if settings.DEBUG:
        if current_image:
            image_path = "{0}/{1}".format(str(settings.MEDIA_ROOT),
                                          str(current_image))
            if os.path.isfile(image_path):
                os.remove(image_path)
    else:
        pass


def handle_upload_profile(name_image, resize_height=100):
    if settings.DEBUG:
        url = "{0}/{1}".format(str(settings.MEDIA_ROOT).replace('\\', '/'),
                               str(name_image))
        image = Image.open(url)
        filename_base, filename_ext = os.path.splitext(url)
        filename = url.rsplit('/', 1)[1].rsplit('.', 1)[0]
        fullpath = url.rsplit('/', 1)[0]
        if filename_ext not in ['.jpg', '.jpeg', '.png']:
            sys.exit()
        image = resize_image.resize_height(image, resize_height)
        new_resize_image = filename + "_" + str(resize_height) + filename_ext
        image.save(fullpath + '/' + new_resize_image)
    else:
        file_path = name_image.name
        filename_base, filename_ext = os.path.splitext(file_path)
        thumb_file_path = filename_base + "_" + str(resize_height) + filename_ext
        f = storage.open(file_path, 'r')
        image = Image.open(f)
        if filename_ext not in ['.jpg', '.jpeg', '.png']:
            sys.exit()
        image = resize_image.resize_height(image, resize_height)
        f_thumb = storage.open(thumb_file_path, "w")
        image.save(f_thumb, "jpeg")
        f_thumb.close()

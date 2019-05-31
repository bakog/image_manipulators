# -*- coding: utf-8 -*-

import os
from exif import Image
import datetime
import time
#import filecmp
import hashlib


with open("/home/bakog/Dropbox/phyton/image_renamer_by_exif/sample_data/pictures_without_exif/DSCN0017.JPG", 'rb') as image_file:
    my_image = Image(image_file)
    image_date = my_image.get('datetime_original', None)
    image_date_converted = image_date.replace(":", '_').replace(" ", '_')

    print(len(image_date_converted))

    print(image_date_converted.strip('\n\l'))

    print(image_date_converted.replace(chr(0), ""))

    for c in image_date_converted:
        print(ord(c))

# -*- coding: utf-8 -*-

import os
from exif import Image
import datetime
import time
#import filecmp
import hashlib


with open("/home/bakog/Dropbox/phyton/image_renamer_by_exif/teszt_kepek/kepek_2/vmps.jpg", 'rb') as image_file:
    my_image = Image(image_file)
    image_date = my_image.get('datetime_original', None)
    print(image_date)

# -*- coding: utf-8 -*-

import os
import hashlib


def list_image_hash_in_dir(dirname):
    file_hash_in_target_dir = set()
    file_count = 0

    if check_dir(dirname):

        for root, dirs, files in os.walk(dirname, topdown=True):
            for file in files:
                # print(file)
                name, ext = os.path.splitext(file)
                if ext.lower() in [".jpg", ".jpeg"]:
                    # print(ext)
                    file_count += 1
                    filename = os.path.join(root, file)
                    file_hash_in_target_dir.add(hashlib.blake2b(open(filename, 'rb').read()).hexdigest())

    return file_hash_in_target_dir


def check_dir(dirname):

    if os.path.exists(dirname) and os.path.isdir(dirname):
        return True
    return False

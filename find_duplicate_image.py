# -*- coding: utf-8 -*-

import os
import hashlib
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_hash_in_target_dir = set()

file_count = 0
duplicate_count = 0
start_time = time.time()
for root, dirs, files in os.walk(BASE_DIR, topdown=True):
    for file in files:
        # print(file)
        name, ext = os.path.splitext(file)
        if ext.lower() in [".jpg", ".jpeg"]:
            # print(ext)
            file_count += 1
            filename = os.path.join(root, file)
            file_hash = hashlib.blake2b(open(filename, 'rb').read()).hexdigest()
            if file_hash not in file_hash_in_target_dir:
                file_hash_in_target_dir.add(file_hash)
            else:
                duplicate_count +=1

end_time = time.time()

print(file_hash_in_target_dir)

print(file_count, " fájl van a könyvtárban, ebből ", duplicate_count, "fájl van többször...")

print("A futási idő : ", end_time-start_time, " másodperc")

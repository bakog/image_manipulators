# -*- coding: utf-8 -*-


import os
from exif import Image
import hashlib


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_hash_in_target_dir = set()


image_name = "080726 1020.jpg"
image_file_path = os.path.join(BASE_DIR, "teszt_kepek/kepek_1", image_name)
# image_hash = hashlib.sha3_512(open(image_file_path, 'rb').read()).hexdigest()
# print(image_hash, image_hash.digest_size, image_hash.block_size)

#print(hashlib.algorithms_available)

image_hash = hashlib.blake2b(open(image_file_path, 'rb').read()).hexdigest()

print(image_hash)
print(image_file_path)

# sys.exit()
with open(image_file_path, 'rb') as image_file:
    my_image = Image(image_file)
    image_date = my_image.get('datetime_original', None)
    if image_date:
        image_date_part_1 = image_date.split()[0].replace(":", "-")
        print(image_date_part_1[:7])
        target_dir = os.path.join(BASE_DIR, image_date_part_1[:7])
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)
        else:
            for root, dirs, files in os.walk(target_dir, topdown=True):
                for file in files:
                    print(file)

                    name, ext = os.path.splitext(file)
                    print(name, ext)

                    if ext.lower() in [".jpg", ".jpeg"]:
                        print(ext)
                        filename = os.path.join(root, file)
                        file_hash_in_target_dir.add(hashlib.blake2b(open(filename, 'rb').read()).hexdigest())

            print(file_hash_in_target_dir)


        if image_hash not in file_hash_in_target_dir:
            pass
            #os.replace(image_file_path, os.path.join(BASE_DIR, image_date_part_1[:7], image_name))
        else:
            print("Már van ilyen fájl, törlöm...")
            #os.remove(image_file_path)

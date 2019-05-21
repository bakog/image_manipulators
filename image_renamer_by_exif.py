# -*- coding: utf-8 -*-

import os
import sys
from exif import Image
import datetime
import time
import filecmp

start_dir = input("Adja meg a kezdőkönyvtár nevét! ")

if not start_dir:
    start_dir = "./teszt_kepek"

konyvtarak = set()

inkey = "öüóőúéáűíÖÜÓŐÚÉÁŰÍ "
outkey = "ouooueauiouooueaui_"
delkey = ',?;:.-§¬~+^!˘%°/˛=`(˙)´˝¨¸÷×$ß¤'
t = str.maketrans(inkey, outkey, delkey)

if os.path.exists(start_dir):

    for root, dirs, files in os.walk(start_dir, topdown=True):
        #print("Fájlok: ")
        for name in files:
            old_name = name
            print(os.path.join(root, name))
            print("ROOT: ",root)



            filename_parts = []
            filename_parts = name.split(".")
            #filename, filename_ext = name.split(".")
            # for part in len(filename_parts)-2:
            filename_parts_2 = [x.strip() for x in filename_parts]

            filename = "_".join(filename_parts_2[:-1])

            print(filename)

            #sys.exit()
            filename_ext = filename_parts[-1]
            filename_new = filename.translate(t)

            #print(os.path.join(root, name))
            if filename_ext in ['jpg', 'JPG', 'jpeg', 'JPEG']:
                with open(os.path.join(root, old_name), 'rb') as image_file:
                    try:
                        my_image = Image(image_file)
                        image_date = my_image.get('datetime_original', None)
                        if image_date:
                            image_date_converted = image_date.replace(":", '_').replace(" ", '_')
                            print(image_date, image_date_converted)
                            if image_date_converted not in filename_new:
                                filename_new += "_"+image_date_converted
                    except:
                        print("Az EXIF információ nem elérhető...")


            new_name = ".".join([filename_new.lower(), filename_ext])
            print(os.path.join(root, new_name))
            if os.path.isfile(os.path.join(root, new_name)) and not filecmp.cmp(os.path.join(root, new_name), os.path.join(root, old_name)):

                print("már van ilyen nevű fájl és a kettő tartalma nem egyezik meg...")
                now = datetime.datetime.now()
                now_filepart = str(now.hour)+str(now.minute)+str(now.second)+str(now.microsecond)
                print(now_filepart)
                new_name_part1, new_name_part2 = new_name.split(".")
                new_name_part1 += "_"+now_filepart
                new_name = ".".join([new_name_part1, new_name_part2])
                print(new_name)

                os.rename(os.path.join(root, old_name), os.path.join(root, new_name))
                time.sleep(1/100)

            else:

                os.rename(os.path.join(root, old_name), os.path.join(root, new_name))


        # #print("Könyvtárak")
        # for name in dirs:
        #     konyvtarak.add(os.path.join(root, name))
        #     #print(os.path.join(root, name))


else:
    print("Nincs ilyen könyvtár!")


# print("A könyvtár alkönyvtárai: ")
# for d in konyvtarak:
#     print(d)
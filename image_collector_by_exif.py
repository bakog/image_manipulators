# -*- coding: utf-8 -*-
'''
A forrás könyvtárban lévő jpg fájlokat áthelyezi a cél könyvtárba úgy, hogy az exif információval
rendelkező fájlok esetében a fájl nevébe beírja a készítés dátumát is.

Fájlnévütközés esetén - ha a két fájl tartalma eltér -  a fájl nevét kiegészíti az aktuális időből
 készített időbélyeggel a felülírás elkerülése érdekében.

A fájlok neveit optimalizálja:
- lecseréli a magyar ékezetes karaktereket ékezet nélkülire (angol ábc)
- eltávolítja szóközöket, pontokat és egyéb speciális jeleket

Az inkey-ben lévő karaktereket cseréli az outkeyben lévő párjára (index!!!)
A delkey-ben lévő karaktereket törli a fájl nevéből

inkey = "öüóőúéáűíÖÜÓŐÚÉÁŰÍ "
outkey = "ouooueauiouooueaui_"
delkey = ',?;:.-§¬~+^!˘%°/˛=`(˙)´˝¨¸÷×$ß¤'

'''
import os
import sys
from exif import Image
import datetime
import time
import filecmp

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

file_counter_dest_dir = 0
file_counter_dest_dir_no_exif = 0
file_counter_for_same_name = 0

file_counter_bad_image = 0

konyvtarak = set()
inkey = "öüóőúéáűíÖÜÓŐÚÉÁŰÍ "
outkey = "ouooueauiouooueaui_"
delkey = ',?;:.-§¬~+^!˘%°/˛=`(˙)´˝¨¸÷×$ß¤'
t = str.maketrans(inkey, outkey, delkey)


def convert_relative_path_to_absolute(dirname):
    if dirname[0] == ".":
        dirname = BASE_DIR + dirname[1:]
    return dirname


def check_dir_exists(dirname):
    if os.path.exists(dirname):
        return True
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        return False


while True:
    start_dir = input("Adja meg a forrás könyvtár nevét! ")
    start_dir = convert_relative_path_to_absolute(start_dir)
    if check_dir_exists(start_dir):
        break
    else:
        print("A forrás könyvtár nem létezik...")

while True:
    dest_dir = input("Adja meg a cél könyvtár nevét! ")
    dest_dir = convert_relative_path_to_absolute(dest_dir)
    if check_dir_exists(dest_dir):
        break
    else:
        print("A cél könyvtár nem létezik...")

dest_dir_no_exif = dest_dir + "/no_exif_data"

if not check_dir_exists(dest_dir_no_exif):
    print("Létrehozom a célkönyvtár 'no_exif_data' alkönyvtárát, azoknak a képeknek, amiknek nincs exif adata...")
    os.mkdir(dest_dir_no_exif)

for root, dirs, files in os.walk(start_dir, topdown=True):
    for name in files:
        old_name = name
        filename_parts = []
        # a fájlnév és a fájlkiterjesztés szétbontása
        filename_parts = name.split(".")
        # az utolsó pont után van a fájlnév kiterjesztés, ha több pont is lenne...
        filename_ext = filename_parts[-1]
        # a felesleges szóközök, ékezetes karakterek törlése a fájlnévben
        filename_parts_1 = [x.strip().translate(t) for x in filename_parts]
        # a korábbi fájlnév részeket összefűzzük _ jellel
        filename = "_".join(filename_parts_1[:-1])

        # jpg fájlokból kiszedjük az exif információt

        if filename_ext in ['jpg', 'JPG', 'jpeg', 'JPEG']:
            with open(os.path.join(root, old_name), 'rb') as image_file:
                try:
                    my_image = Image(image_file)
                    image_date = my_image.get('datetime_original', None)
                    if image_date:
                        target_dir = dest_dir
                        file_counter_dest_dir += 1
                        # az exif információ átalakítása
                        image_date_converted = image_date.replace(":", '_').replace(" ", '_')
                        # az exif információ hozzáfűzése a fájl eredeti nevéhez, ha még nem tartalmazta
                        if image_date_converted not in filename:
                            filename += "_" + image_date_converted
                    else:
                        target_dir = dest_dir_no_exif
                        file_counter_dest_dir_no_exif += 1

                except:
                    # ha a fájl kiterjesztés képre utal, de mégsem
                    #target_dir = dest_dir_no_exif
                    file_counter_bad_image +=1
                    print("Az EXIF információ nem elérhető...", os.path.join(root, old_name))

                    continue

            new_name = ".".join([filename, filename_ext])
            if os.path.isfile(os.path.join(target_dir, new_name)):
                if not filecmp.cmp(os.path.join(target_dir, new_name), os.path.join(root, old_name)):
                    # már van ilyen nevű fájl és a kettő tartalma nem egyezik meg, ezért a fájlnevet ellátjuk időbélyeggel is
                    print("már van ilyen nevű fájl és a kettő tartalma nem egyezik meg...")
                    now = datetime.datetime.now()
                    now_filepart = str(now.hour).zfill(2)+str(now.minute).zfill(2)+str(now.second).zfill(2)+str(now.microsecond).zfill(6)
                    new_name_part1, new_name_part2 = new_name.split(".")
                    new_name_part1 += "_"+now_filepart
                    new_name = ".".join([new_name_part1, new_name_part2])
                    time.sleep(1/100)
                    file_counter_for_same_name += 1

            os.rename(os.path.join(root, old_name), os.path.join(target_dir, new_name))


print("\n\nÖsszegzés: ")

print(file_counter_dest_dir, " fájl áthelyezve a cél könyvtárba, ", file_counter_dest_dir_no_exif,\
      " fájl áthelyezve a a célkönyvtár 'no_exif_data' könyvtárába.")

print(file_counter_for_same_name, " fájl esetén a fájlnevet kiegészítettem időbélyeggel, mert már volt ilyen fájl más tartalommal")

print("Úgy tűnik ", file_counter_bad_image," db. fájl van, ami kiterjesztését tekintve kép, de mégsem az...")
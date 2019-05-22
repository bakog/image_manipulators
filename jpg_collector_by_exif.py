# -*- coding: utf-8 -*-

from exif import Image
import datetime
import hashlib
import os
from termcolor import colored
import time
# import filecmp
# import sys


def convert_relative_path_to_absolute(dirname):

    """
        Convert relative path to absolute

        :param dirname:
        :return: dirname
    """

    base_dir = os.path.dirname(os.path.abspath(__file__))

    if dirname[0] == ".":
        dirname = base_dir + dirname[1:]
    return dirname


def check_dir_exists(dirname):

    """
    Checking dirname directory  existence.

    :param dirname:
    :return: boolean
    """
    if os.path.exists(dirname):
        return True
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        return False


def set_dir(directory_type):
    """
    Set dirname from user input

    :param directory_type: string
    :return: dirname
    """

    while True:
        dirname = input("Adja meg a " + directory_type + " könyvtár nevét! ")
        dirname = convert_relative_path_to_absolute(dirname)
        if check_dir_exists(dirname):
            return dirname


def check_no_exif_data_dir(dest_dir):

    """
    Check dest_dir_no_exif directory existence. If not exists, then create  it, and return its name.

    :param dest_dir:
    :return: dest_dir_no_exif
    """

    dest_dir_no_exif = dest_dir + "/no_exif_data"

    if not check_dir_exists(dest_dir_no_exif):
        print("Létrehozom a célkönyvtár 'no_exif_data' alkönyvtárát, azoknak a képeknek, amiknek nincs exif adata...")
        os.mkdir(dest_dir_no_exif)

    return dest_dir_no_exif


def clean_file_name(filename):

    """
    Clean filaname variable from undesirable chars.

    :param filename:
    :return: filename
    """

    inkey = "öüóőúéáűíÖÜÓŐÚÉÁŰÍ "
    outkey = "ouooueauiouooueaui_"
    delkey = ',?;:.-§¬~+^!˘%°/˛=`(˙)´˝¨¸÷×$ß¤'
    t = str.maketrans(inkey, outkey, delkey)

    return filename.strip().translate(t)


def get_exif_info(root, filename):

    """

    Try to get exif info from file (datetime_original).

    :param root: string file root directory
    :param filename:  string filename
    :return:  image_date_converted : string, or None
    """

    with open(os.path.join(root, filename), 'rb') as image_file:
        try:
            my_image = Image(image_file)
            image_date = my_image.get('datetime_original', None)
            if image_date:
                # az exif információ átalakítása
                image_date_converted = image_date.replace(":", '_').replace(" ", '_')
                return image_date_converted
            else:
                return image_date

        except AssertionError:
            # ha a fájl kiterjesztés képre utal, de mégsem
            # print("Az EXIF információ nem elérhető...", os.path.join(root, filename))
            raise TypeError('Az EXIF információ nem elérhető. Vélhetően hibás a fájl kiterjesztése...')
            # return 'Ez nem igazi képfájl...'


def set_exif_info_in_filename(image_date_converted, filename):

    """
    Check image_date_converted is in the filaname. If not, then insert it to filename end.

    :param image_date_converted: string
    :param filename: string
    :return: filename: string
    """

    # az exif információ hozzáfűzése a fájl eredeti nevéhez, ha még nem tartalmazta
    if image_date_converted not in filename:
        filename += "_" + image_date_converted
    return filename


def list_image_hash_in_dir(dirname):

    """
    Create a set of file hash from files in dirname.

    :param dirname: string
    :return: file_hash_in_target_dir: set of hash string
    """

    print("A meglévő fájlok ellenőrzése a cél könyvtárban....")
    print("Sok kép esetén a folyamat hosszabb ideig tart, várjon türelemmel...")

    file_hash_in_target_dir = set()

    if check_dir_exists(dirname):

        for root, dirs, files in os.walk(dirname, topdown=True):
            for file in files:
                # print(file)
                name, ext = os.path.splitext(file)
                if ext.lower() in [".jpg", ".jpeg"]:
                    # print(ext)
                    filename = os.path.join(root, file)
                    file_hash_in_target_dir.add(hashlib.blake2b(open(filename, 'rb').read()).hexdigest())

    return file_hash_in_target_dir


def get_file_hash(filename):

    """
    Create hash value from file content.

    :param filename: string
    :return: file_hash: string
    """

    file_hash = hashlib.blake2b(open(filename, 'rb').read()).hexdigest()
    return file_hash


def main():
    """
    A forrás könyvtárban lévő jpg fájlokat áthelyezi a cél könyvtárba úgy, hogy az exif információval
    rendelkező fájlok esetében a fájl nevébe beírja a készítés dátumát is.

    Fájlnévütközés esetén - ha a két fájl tartalma eltér -  a fájl nevét kiegészíti az aktuális időből
     készített időbélyeggel a felülírás elkerülése érdekében.

    A fájlok neveit optimalizálja:
    - lecseréli a magyar ékezetes karaktereket ékezet nélkülire (angol ábc)
    - eltávolítja szóközöket, pontokat és egyéb speciális jeleket

    """

    start_dir = set_dir("forrás")
    dest_dir = set_dir("cél")
    dest_dir_no_exif = check_no_exif_data_dir(dest_dir)
    file_hash_in_dest_dir = list_image_hash_in_dir(dest_dir)
    file_counter_for_same_name = 0
    file_counter_dest_dir_no_exif = 0
    file_counter_dest_dir = 0
    file_counter_bad_image = 0
    file_count_deleted = 0

    for root, dirs, files in os.walk(start_dir, topdown=True):
        for name in files:
            old_name = name
            filename, filename_ext = os.path.splitext(name)
            filename = clean_file_name(filename)

            # jpg fájlokból kiszedjük az exif információt

            if filename_ext.lower() in ['.jpg', '.jpeg']:
                try:

                    image_date_converted = get_exif_info(root, old_name)

                    if image_date_converted:
                        filename = set_exif_info_in_filename(image_date_converted, filename)
                        target_dir = dest_dir
                    else:
                        target_dir = dest_dir_no_exif
                except TypeError as error:
                    print(colored (error, "red"), colored(old_name, "grey"))
                    file_counter_bad_image += 1
                    # sys.exit()
                    continue

                new_name = filename+filename_ext

                file_hash = get_file_hash(os.path.join(root, old_name))

                if file_hash in file_hash_in_dest_dir:
                    print(colored ("Már létezik ugyanilyen tartalmú fájl a célkönyvtárban, ezért törlöm a forráskönyvtárban...", "red"))
                    file_count_deleted += 1
                    os.remove(os.path.join(root, old_name))
                else:
                    # A forrás állomány áthelyezése a célkönyvtárba
                    if os.path.isfile(os.path.join(target_dir, new_name)):
                        # már van ilyen nevű fájl és a kettő tartalma nem egyezik meg,
                        # ezért a fájlnevet ellátjuk időbélyeggel is
                        print("Már van ilyen nevű fájl és a kettő tartalma nem egyezik meg...")
                        now = datetime.datetime.now()
                        now_filepart = str(now.hour).zfill(2) + str(now.minute).zfill(2) + str(now.second).zfill(
                            2) + str(now.microsecond).zfill(6)

                        filename += "_" + now_filepart
                        new_name = filename + filename_ext

                        time.sleep(1 / 100)
                        file_counter_for_same_name += 1

                    message = " ".join(["Áthelyezés: ", os.path.join(root, old_name), os.path.join(target_dir, new_name)])
                    print(colored (message, "green"))
                    if target_dir == dest_dir:
                        file_counter_dest_dir += 1
                    else:
                        file_counter_dest_dir_no_exif += 1

                    file_hash_in_dest_dir.add(file_hash)
                    os.rename(os.path.join(root, old_name), os.path.join(target_dir, new_name))

    print("\n\nÖsszegzés: \n")

    print(file_counter_dest_dir, " fájl áthelyezve a cél könyvtárba, ", file_counter_dest_dir_no_exif,
          " fájl áthelyezve a a célkönyvtár 'no_exif_data' könyvtárába.")

    print(file_counter_for_same_name,
          ''' fájl esetén a fájlnevet kiegészítettem időbélyeggel, mert már volt ilyen fájl más tartalommal'''
          )

    print("Úgy tűnik ", file_counter_bad_image,
          ''' db. fájl van, ami kiterjesztését tekintve kép, de mégsem az...'''
          )

    print(file_count_deleted,
          " fájl már létezett a célkönyvtárban (azonos tartalommal) így ezek törölve lettek a forrás könyvtárban!"
          )


if __name__ == "__main__":
    main()

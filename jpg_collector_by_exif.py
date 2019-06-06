# -*- coding: utf-8 -*-

import sys

try:
    import hashlib
    from exif import Image
    import re
    from termcolor import colored
    import time
    from tqdm import tqdm
    import os
    import datetime

except ImportError as exc:
    import_error_message = '''
    A program futásához szükséges '{0}' modul nem taláható!
    Telepítse a 'pip install {0}' parancs beírásával, majd futtassa újra a programot!'''.format(exc.name)

    print(import_error_message)
    sys.exit(1)

# import traceback
# import filecmp


CONFIG_FILENAME = "files_hash_data_in_current_dir_or_subdirs"
CONFIG_FILENAME_EXT = ".txt"


def convert_relative_path_to_absolute(dirname: str) -> str:

    """
    Convert relative path to absolute
    """
    if not os.path.isabs(dirname):
        dirname = os.path.abspath(dirname)

    return dirname


def check_dir_exists(dirname: str) -> bool:

    """
    Checking dirname directory  existence.
    """
    if os.path.exists(dirname):
        return True
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        return False


def warning_message(message: str):
    print(colored(message, "yellow"))


def error_message(message: str):
    print(colored(message, "red"))


def info_message(message: str):
    print(colored(message, "blue"))


def get_dir(directory_type: str) -> str:
    """
    Set dirname from user input
    """

    while True:
        dirname = input("Adja meg a " + directory_type + " könyvtár nevét! ")
        dirname = convert_relative_path_to_absolute(dirname)
        if check_dir_exists(dirname):
            return dirname
        else:
            error_message("A megadott könyvtár nem létezik!")


def create_no_exif_data_dir(dest_dir: str) -> str:

    """
    Check dest_dir_no_exif directory existence. If not exists, then create  it, and return its name.
    """

    dest_dir_no_exif = dest_dir + "/no_exif_data"

    if not check_dir_exists(dest_dir_no_exif):
        # info_message("Létrehozom a célkönyvtár 'no_exif_data' alkönyvtárát, azoknak\
        # a képeknek, amiknek nincs exif adata...")
        os.mkdir(dest_dir_no_exif)

    return dest_dir_no_exif


def clean_file_name(filename: str) -> str:

    """
    Clean filaname variable from undesirable chars.
    """

    inkey = "öüóőúéáűíÖÜÓŐÚÉÁŰÍ"
    outkey = "ouooueauiouooueaui"
    # delkey = ',?;:.-§¬~+^!˘%°/˛=`(˙)´˝¨¸÷×$ß¤@'

    # levágjuk a felesleges szóközöket és feldaraboljuk szóközönként, ha van benne
    filename_part = list(filename.strip().split())

    # a fájlnév darabjai összefűzzük _ jellel
    cleaned_string = "_".join(filename_part)

    # kiszedjük a magyar ékezetes karaktereket
    t = str.maketrans(inkey, outkey)
    cleaned_string = cleaned_string.translate(t)

    # eltávolítjuk az  összes nem odaillő karaktert, kivéve az _ jelet
    cleaned_string = re.sub('[^A-Za-z0-9_]+', '', cleaned_string)

    # levágjuk a felesleges _ jeleket a végeiről, majd a többször előforduló _ jelet egy _-ra cseréljük
    cleaned_string = re.sub('_{2,}', '_', cleaned_string.strip('_'))

    return cleaned_string


def get_exif_info(filename_with_path: str):

    """
    Try to get exif info from file (datetime_original).

    :return:  image_date_converted : string, or None
    """

    with open(filename_with_path, 'rb') as image_file:
        try:
            my_image = Image(image_file)
            image_date = my_image.get('datetime_original', None)
            if image_date:
                # az exif információ átalakítása
                image_date = image_date.replace(chr(0), "")
                image_date_converted = image_date.replace(":", '_').replace(" ", '_')
                return image_date_converted
            else:
                return None

        except:
            # ha a fájl kiterjesztés képre utal, de mégsem
            # traceback.print_exc()
            return None
            #raise


def set_exif_info_in_filename(image_date_converted: str, filename: str) -> str:

    """
    Check image_date_converted is in the filaname. If not, then insert it to filename end.
    """

    # az exif információ hozzáfűzése a fájl eredeti nevéhez, ha még nem tartalmazta
    if image_date_converted not in filename:
        filename += "_" + image_date_converted
    return filename


def get_file_hash_in_dir(dirname: str) -> set:

    """
    Create a set of file hash from files in dirname.
    """
    file_hash_in_target_dir = set()
    count_of_files_in_dest_dir = sum([len(files) for r, d, files in os.walk(dirname)])

    if count_of_files_in_dest_dir != 0:

        with tqdm(total=count_of_files_in_dest_dir) as pbar:
            if count_of_files_in_dest_dir == 0:
                pbar.update()

            if check_dir_exists(dirname):

                for root, dirs, files in os.walk(dirname, topdown=True):
                    for file in files:
                        pbar.update()
                        name, ext = os.path.splitext(file)
                        if ext.lower() in [".jpg", ".jpeg"]:
                            filename = os.path.join(root, file)
                            file_hash_in_target_dir.add(get_file_hash(filename))

    return file_hash_in_target_dir


def save_file_hash_to_file(hash_of_files: set):

    filename = set_date_in_filename(CONFIG_FILENAME)

    full_filename = filename+CONFIG_FILENAME_EXT

    with open(full_filename, "w") as outfile:
        for item in hash_of_files:
            outfile.write(item+'\n')


def open_file_hash_from_file() -> set:

    hash_of_files = set()

    filename = set_date_in_filename(CONFIG_FILENAME)

    full_filename = filename+CONFIG_FILENAME_EXT

    try:
        with open(full_filename, "r") as in_file:
            for line in in_file:
                hash_of_files.add(line.strip())
    except IOError:
        info_message("Még nem készült  friss nyilvántartás a célkönyvtár fájljairól, most készítek egyet...")

    return hash_of_files


def get_file_hash(filename: str) -> str:

    """
    Create hash value from file content.
    """

    file_hash = hashlib.blake2b(open(filename, 'rb').read()).hexdigest()
    return file_hash


def set_timestamp_in_filename(filename: str) -> str:
    """
    Add timestamp to end of filename.
    """
    now = datetime.datetime.now()
    now_filepart = str(now.hour).zfill(2) + str(now.minute).zfill(2) + str(now.second).zfill(
        2) + str(now.microsecond).zfill(6)

    filename += "_" + now_filepart
    time.sleep(1 / 100)
    return filename


def set_date_in_filename(filename: str) -> str:
    """
    Add timestamp to end of filename.
    """
    now = datetime.datetime.now()
    now_filepart = str(now.year).zfill(4) + str(now.month).zfill(2) + str(now.day).zfill(
        2)

    filename += "_" + now_filepart
    return filename


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

    start_dir = get_dir("forrás")
    dest_dir = get_dir("cél")
    dest_dir_no_exif = create_no_exif_data_dir(dest_dir)

    file_hash_in_dest_dir = open_file_hash_from_file()
    if not file_hash_in_dest_dir:
        info_message("A meglévő fájlok ellenőrzése a cél könyvtárban....")
        info_message("Sok kép esetén a folyamat hosszabb ideig tart, várjon türelemmel...")
        file_hash_in_dest_dir = get_file_hash_in_dir(dest_dir)


    file_counter_for_same_name = 0
    file_counter_dest_dir_no_exif = 0
    file_counter_dest_dir = 0
    file_counter_bad_image = 0
    file_count_deleted = 0

    for root, dirs, files in os.walk(start_dir, topdown=True):
        for name in files:

            original_name = name
            original_name_with_path = os.path.join(root, name)
            filename, filename_ext = os.path.splitext(name)
            filename = clean_file_name(filename)

            # jpg fájlokból kiszedjük az exif információt

            if filename_ext.lower() in ['.jpg', '.jpeg']:
                # try:

                image_date_converted = get_exif_info(original_name_with_path)

                if image_date_converted:
                    filename = set_exif_info_in_filename(image_date_converted, filename)
                    target_dir = dest_dir
                else:
                    target_dir = dest_dir_no_exif
                    error_message("\nAz EXIF információ nem elérhető... " + original_name)

                # except:
                #     target_dir = dest_dir_no_exif
                #
                #     error_message("\nAz EXIF információ nem elérhető... "+original_name)
                #     file_counter_bad_image += 1
                #     # sys.exit()
                #     # continue

                new_name = filename + filename_ext

                print(new_name)

                file_hash = get_file_hash(original_name_with_path)

                if file_hash in file_hash_in_dest_dir:
                    warning_message("Már létezik ugyanilyen tartalmú fájl a célkönyvtárban, ezért törlöm a forráskönyvtárban...")
                    file_count_deleted += 1
                    os.remove(original_name_with_path)
                else:
                    # A forrás állomány áthelyezése a célkönyvtárba
                    try:

                        if os.path.isfile(os.path.join(target_dir, new_name)):
                            # már van ilyen nevű fájl és a kettő tartalma nem egyezik meg,
                            # ezért a fájlnevet ellátjuk időbélyeggel is
                            warning_message("Már van ilyen nevű fájl és a kettő tartalma nem egyezik meg...")
                            filename = set_timestamp_in_filename(filename)
                            new_name = filename + filename_ext
                            file_counter_for_same_name += 1

                        message = " ".join(["Áthelyezés: ", original_name_with_path, os.path.join(target_dir, new_name)])
                        info_message(message)
                        if target_dir == dest_dir:
                            file_counter_dest_dir += 1
                        else:
                            file_counter_dest_dir_no_exif += 1

                        file_hash_in_dest_dir.add(file_hash)
                        os.rename(original_name_with_path, os.path.join(target_dir, new_name))
                    except:

                        print("Hiba lépett fel a következő fájl esetén: ", os.path.join(target_dir, new_name))
                        continue

    save_file_hash_to_file(file_hash_in_dest_dir)

    warning_message("\n\nÖsszegzés: \n")

    info_message(
            str(file_counter_dest_dir) + " fájl áthelyezve a cél könyvtárba, " + str(file_counter_dest_dir_no_exif) +
            " fájl áthelyezve a a célkönyvtár 'no_exif_data' könyvtárába."
        )

    info_message(
            str(file_counter_for_same_name) +
            ' fájl esetén a fájlnevet kiegészítettem időbélyeggel, mert már volt ilyen fájl más tartalommal'
          )

    warning_message(
            "Úgy tűnik " + str(file_counter_bad_image) +
            ' db. fájl van, ami kiterjesztését tekintve kép, de az exif információk nem elérhetőek...'
          )

    error_message(
            str(file_count_deleted) +
            " fájl már létezett a célkönyvtárban (azonos tartalommal) így ezek törölve lettek a forrás könyvtárban!"
          )


if __name__ == "__main__":
    main()

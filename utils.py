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


def convert_relative_path_to_absolute(dirname: str) -> str:
    """
    Convert relative path to absolute
    """
    if not os.path.isabs(dirname):
        dirname = os.path.abspath(dirname)

    return dirname


# def check_dir_exists(dirname: str) -> bool:
#
#     """
#     Checking dirname directory  existence.
#     """
#     if os.path.exists(dirname):
#         return True
#     else:
#         os.system('cls' if os.name == 'nt' else 'clear')
#         return False

# def check_hash_file_exists(filename: str) -> bool:
#     """
#
#     :param filename:
#     :return:
#     """
#     filename = set_date_in_filename(CONFIG_FILENAME)
#
#     full_filename = filename+CONFIG_FILENAME_EXT
#
#     if os.path.exists(daily_config_filaname):
#         return True
#     return False


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
        if os.path.exists(dirname):
            return dirname
        else:
            error_message("A megadott könyvtár nem létezik!")


def create_no_exif_data_dir(dest_dir: str) -> str:

    """
    Check dest_dir_no_exif directory existence. If not exists, then create  it, and return its name.
    """

    dest_dir_no_exif = dest_dir + "/no_exif_data"

    if not os.path.exists(dest_dir_no_exif):
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


def get_image_exif_info(filename_with_path: str):

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
                exif_info_date = image_date.replace(":", '_').replace(" ", '_')
                return exif_info_date
            else:
                return None

        except:
            # ha a fájl kiterjesztés képre utal, de mégsem
            # traceback.print_exc()
            return None
            # raise


def get_video_exif_info(filename_with_path: str):

    """
    Try to get exif info from file (datetime_original).

    """
    dates = list()
    grep_formula = ' | grep -e "Create Date" -e "Creation time" -e \
                    "File Access Date/Time" -e "File Modification Date/Time"'
    process = os.popen('exiftool ' + filename_with_path.replace(" ", "\ ") + grep_formula, 'r', 1)
    for item in process:
        datum = item.split(":", 1)[1].strip()
        datum = datum.replace(":", "_").replace(" ", "_").replace("-", "_")

        # print(datum[0:4], datum.split("_")[0], filename)
        datum_kezdet = datum.split("_")[0]
        try:
            if datum_kezdet != "0000" and int(datum_kezdet) < 2019:
                # print("Dátum hossza: ", len(datum))
                # print("hozzáadom , datum )
                dates.append(datum)
        except:
            print("Oppá, valami gond van, az adatok átalakításával...")

    if len(dates):
        dates.sort()
        return min(dates).strip()[0:19]
    else:
        # nincs exif információ
        return None


def set_exif_info_in_filename(exif_info_date: str, filename: str) -> str:

    """
    Check image_date_converted is in the filename. If not, then insert it to filename end.
    """

    # az exif információ hozzáfűzése a fájl eredeti nevéhez, ha még nem tartalmazta
    if exif_info_date not in filename:
        filename += "_" + exif_info_date
    return filename


def get_count_of_files_in_dir(dirname: str) -> int:
    """
    Visszaadja a megadott köynvtár fájljainak a számát!
    :param dirname:
    :return:  int
    """
    count_of_files_in_dir = sum([len(files) for r, d, files in os.walk(dirname)])
    return count_of_files_in_dir


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


def get_file_hash_in_dir(dirname: str) -> set:

    """
    Create a set of file hash from files in dirname.
    """
    info_message("A meglévő fájlok ellenőrzése a cél könyvtárban....")
    info_message("Sok fájl esetén a folyamat hosszabb ideig tart, várjon türelemmel...")

    file_hash_in_target_dir = set()
    count_of_files_in_dest_dir = get_count_of_files_in_dir(dirname)

    if count_of_files_in_dest_dir != 0:

        with tqdm(total=count_of_files_in_dest_dir) as pbar:
            if count_of_files_in_dest_dir == 0:
                pbar.update()

            if os.path.exists(dirname):

                for root, dirs, files in os.walk(dirname, topdown=True):
                    for file in files:
                        pbar.update()
                        name, ext = os.path.splitext(file)
                        # if ext.lower() in [".jpg", ".jpeg"]:
                        filename = os.path.join(root, file)
                        file_hash_in_target_dir.add(get_file_hash(filename))

    return file_hash_in_target_dir


def save_file_hash_to_file(hash_file: str, hash_of_files: set):

    with open(hash_file, "w") as outfile:
        for item in hash_of_files:
            outfile.write(item+'\n')


def get_hash_of_files_from_file(hash_file: str, dest_dir: str) -> set:
    """
    Get hash of files in destiantion dir from config file or rescan destiantion dir for current hash data
    :param hash_file: daily saved hash file
    :param dest_dir:  destiantion directory for files
    :return:  set: hash values of files in destination dir
    """

    hash_of_files = set()

    if os.path.exists(hash_file):
        with open(hash_file, "r") as in_file:
            for line in in_file:
                hash_of_files.add(line.strip())

    if not hash_of_files or (len(hash_of_files) != get_count_of_files_in_dir(dest_dir)):
        hash_of_files = get_file_hash_in_dir(dest_dir)

    return hash_of_files

def summary_report(file_counter_dest_dir: int, file_counter_dest_dir_no_exif: int, file_counter_for_same_name: int, file_count_deleted:int):

    warning_message("\n\nÖsszegzés: \n")

    info_message(
            str(file_counter_dest_dir) + " fájl áthelyezve a cél könyvtárba, " + str(file_counter_dest_dir_no_exif) +
            " fájl áthelyezve a a célkönyvtár 'no_exif_data' könyvtárába."
        )

    info_message(
            str(file_counter_for_same_name) +
            ' fájl esetén a fájlnevet kiegészítettem időbélyeggel, mert már volt ilyen fájl más tartalommal'
          )

    error_message(
            str(file_count_deleted) +
            " fájl már létezett a célkönyvtárban (azonos tartalommal) így ezek törölve lettek a forrás könyvtárban!"
          )
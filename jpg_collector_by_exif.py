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


from utils import warning_message, info_message, error_message, get_dir, clean_file_name,\
                    set_timestamp_in_filename, set_exif_info_in_filename, set_date_in_filename, \
                    create_no_exif_data_dir, get_hash_of_files_from_file, get_file_hash, get_image_exif_info,\
                    save_file_hash_to_file, summary_report


CONFIG_FILENAME = "hash_data_of images_in_current_dir_or_subdirs"
CONFIG_FILENAME_EXT = ".txt"
daily_config_filename = set_date_in_filename(CONFIG_FILENAME)+CONFIG_FILENAME_EXT
FILE_EXTENSIONS = [".jpg", ".jpeg"]


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

    file_hash_in_dest_dir = get_hash_of_files_from_file(daily_config_filename, dest_dir)

    file_counter_for_same_name = 0
    file_counter_dest_dir_no_exif = 0
    file_counter_dest_dir = 0
    # file_counter_bad_image = 0
    file_count_deleted = 0

    for root, dirs, files in os.walk(start_dir, topdown=True):
        for name in files:

            original_name = name
            original_name_with_path = os.path.join(root, name)
            filename, filename_ext = os.path.splitext(name)
            filename = clean_file_name(filename)

            # jpg fájlokból kiszedjük az exif információt

            if filename_ext.lower() in FILETYPES:
                # try:

                image_date_converted = get_image_exif_info(original_name_with_path)

                if image_date_converted:
                    filename = set_exif_info_in_filename(image_date_converted, filename)
                    target_dir = dest_dir
                else:
                    target_dir = dest_dir_no_exif
                    error_message("\nAz EXIF információ nem elérhető... " + original_name)

                new_name = filename + filename_ext

                print(new_name)

                file_hash = get_file_hash(original_name_with_path)

                if file_hash in file_hash_in_dest_dir:
                    warning_message("Már létezik ugyanilyen tartalmú fájl\
                                    a célkönyvtárban, ezért törlöm a forráskönyvtárban...")
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

                        message = " ".join(["Áthelyezés: "
                                               , original_name_with_path, os.path.join(target_dir, new_name)])
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

    if file_hash_in_dest_dir:
        save_file_hash_to_file(daily_config_filename, file_hash_in_dest_dir)

    summary_report(file_counter_dest_dir, file_counter_dest_dir_no_exif, file_counter_for_same_name, file_count_deleted)

    # warning_message("\n\nÖsszegzés: \n")
    #
    # info_message(
    #         str(file_counter_dest_dir) + " fájl áthelyezve a cél könyvtárba, " + str(file_counter_dest_dir_no_exif) +
    #         " fájl áthelyezve a a célkönyvtár 'no_exif_data' könyvtárába."
    #     )
    #
    # info_message(
    #         str(file_counter_for_same_name) +
    #         ' fájl esetén a fájlnevet kiegészítettem időbélyeggel, mert már volt ilyen fájl más tartalommal'
    #       )
    #
    # warning_message(
    #         "Úgy tűnik " + str(file_counter_bad_image) +
    #         ' db. fájl van, ami kiterjesztését tekintve kép, de az exif információk nem elérhetőek...'
    #       )
    #
    # error_message(
    #         str(file_count_deleted) +
    #         " fájl már létezett a célkönyvtárban (azonos tartalommal) így ezek törölve lettek a forrás könyvtárban!"
    #       )


if __name__ == "__main__":
    main()

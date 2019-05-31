# -*- coding: utf-8 -*-

import sys

try:
    import os
    import datetime
    import time

except ImportError as exc:
    import_error_message = '''
    A program futásához szükséges '{0}' modul nem taláható!
    Telepítse a 'pip install {0}' parancs beírásával, majd futtassa újra a programot!'''.format(exc.name)

    print(import_error_message)
    sys.exit(1)

from jpg_collector_by_exif import get_dir, get_exif_info, info_message, error_message


def get_timestamp() -> str:
    """
    Add timestamp to end of filename.
    """
    now = datetime.datetime.now()
    now_filepart = str(now.hour).zfill(2) + str(now.minute).zfill(2) + str(now.second).zfill(
        2) + str(now.microsecond).zfill(6)

    time.sleep(1 / 100)
    return now_filepart

def main():

    start_dir = get_dir("forrás")
    file_counter = 1

    for root, dirs, files in os.walk(start_dir, topdown=True):

        for name in files:

            original_name = name
            original_name_with_path = os.path.join(root, name)
            filename, filename_ext = os.path.splitext(name)
            # filename = clean_file_name(filename)

            # jpg fájlokból kiszedjük az exif információt

            if filename_ext.lower() in ['.jpg', '.jpeg']:
                try:

                    image_date_converted = get_exif_info(original_name_with_path)

                    if image_date_converted:
                        # filename = set_exif_info_in_filename(image_date_converted, filename)

                        new_name = 'IMG_' + str(file_counter).zfill(6) + "_" + image_date_converted + filename_ext.lower()
                        message = " ".join(
                            ["Áthelyezés: ", original_name_with_path, os.path.join(root, new_name)])
                        info_message(message)
                        os.rename(original_name_with_path, os.path.join(root, new_name))

                except:
                    error_message("\nAz EXIF információ nem elérhető... " + original_name)
                    new_name = 'IMG_' + str(file_counter).zfill(6) + "_" + get_timestamp() + filename_ext.lower()
                    message = " ".join(
                        ["Áthelyezés: ", original_name_with_path, os.path.join(root, new_name)])
                    info_message(message)
                    os.rename(original_name_with_path, os.path.join(root, new_name))

                    # sys.exit()
            file_counter += 1

if __name__ == "__main__":
    main()

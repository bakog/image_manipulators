# -*- coding: utf-8 -*-

import sys

try:
    import hashlib
    from exif import Image
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


from jpg_collector_by_exif import error_message, info_message, get_dir, get_exif_info


def create_dir(dirname: str):

    """
    Checking dirname directory  existence.
    """
    if not os.path.exists(dirname):
        os.mkdir(dirname)


def main():

    start_dir = get_dir("forrás")

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
                        create_dir(os.path.join(start_dir, image_date_converted[:7]))
                        create_dir(os.path.join(start_dir, image_date_converted[:7], image_date_converted[:10]))
                        target_dir = os.path.join(start_dir, image_date_converted[:7], image_date_converted[:10])
                        new_name = filename + filename_ext
                        message = " ".join(
                            ["Áthelyezés: ", original_name_with_path, os.path.join(target_dir, new_name)])
                        info_message(message)
                        os.rename(original_name_with_path, os.path.join(target_dir, new_name))

                except AssertionError:
                    error_message("\nAz EXIF információ nem elérhető... " + original_name)
                    # sys.exit()
                    continue


if __name__ == "__main__":
    main()

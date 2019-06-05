# -*- coding: utf-8 -*-


import os

from jpg_collector_by_exif import get_dir, create_no_exif_data_dir, clean_file_name, open_file_hash_from_file, info_message,\
        save_file_hash_to_file, get_file_hash_in_dir, set_exif_info_in_filename, error_message


def get_exif_info_for_video(filename_with_path: str):

    """
    Try to get exif info from file (datetime_original).

    """
    dates = list()
    process = os.popen('exiftool ' + filename_with_path.replace(" ", "\ ") + ' | grep -e "Create Date" -e "Creation time" -e "File Access Date/Time" -e "File Modification Date/Time"', 'r', 1)
    for item in process:
        datum = item.split(":", 1)[1].strip()
        #print(datum[0:4])
        if datum[0:4] != "0000" and int(datum[0:4]) < 2019:
            #print("Dátum hossza: ", len(datum))
            print("hozzáadom ", datum )
            dates.append(datum)

    if len(dates):
        dates.sort()
        #print(dates)
        #print(dates[1], min(dates))
        #print(min(dates))
        return min(dates).strip().replace(":", "_").replace(" ", "_")[0:19]
    else:
        print("Nincs exif információ")
        return None


#
# start_dir = get_dir("forrás")
# dest_dir = get_dir("cél")

start_dir = "./sample_data/videos"
dest_dir = "./videos"

dest_dir_no_exif = create_no_exif_data_dir(dest_dir)

file_hash_in_dest_dir = open_image_hash_from_file()
if not file_hash_in_dest_dir:
    info_message("A meglévő fájlok ellenőrzése a cél könyvtárban....")
    info_message("Sok kép esetén a folyamat hosszabb ideig tart, várjon türelemmel...")
    file_hash_in_dest_dir = get_image_hash_in_dir(dest_dir)

save_image_hash_to_file(file_hash_in_dest_dir)

file_counter_for_same_name = 0
file_counter_dest_dir_no_exif = 0
file_counter_dest_dir = 0
file_counter_bad_image = 0
file_count_deleted = 0

dates = list()

for root, dirs, files in os.walk(start_dir, topdown=True):
    for name in files:

        original_name = name
        original_name_with_path = os.path.join(root, name)
        filename, filename_ext = os.path.splitext(name)
        filename = clean_file_name(filename)

        image_date_converted = get_exif_info_for_video(original_name_with_path)

        if image_date_converted:
            filename = set_exif_info_in_filename(image_date_converted, filename)
            target_dir = dest_dir
        else:
            target_dir = dest_dir_no_exif
            error_message("\nAz EXIF információ nem elérhető... " + original_name)

        new_name = filename + filename_ext

        print(new_name)



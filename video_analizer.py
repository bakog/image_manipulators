# -*- coding: utf-8 -*-


import os
import sys

from utils import get_dir, create_no_exif_data_dir, clean_file_name, get_hash_of_files_from_file, info_message,\
        save_file_hash_to_file, set_exif_info_in_filename, error_message,\
        warning_message, get_file_hash, set_timestamp_in_filename, get_count_of_files_in_dir, set_date_in_filename,\
        get_video_exif_info, summary_report, convert_relative_path_to_absolute


CONFIG_FILENAME = "hash_data_of_videos_in_current_dir_or_subdirs"
CONFIG_FILENAME_EXT = ".txt"
FILE_EXTENSIONS = [".mp4", ".mpg", ".mkv", ".flv", ".3gp", ".wmv", ".avi", ".m4v", ".vob", ".mov"]

daily_config_filename = set_date_in_filename(CONFIG_FILENAME)+CONFIG_FILENAME_EXT


def main():

    #
    # start_dir = get_dir("forrás")
    # dest_dir = get_dir("cél")

    start_dir = "./teszt_video"
    dest_dir = convert_relative_path_to_absolute("./videos")

    dest_dir_no_exif = create_no_exif_data_dir(dest_dir)

    #print(daily_config_filename, dest_dir)
    file_hash_in_dest_dir = get_hash_of_files_from_file(daily_config_filename, dest_dir)

    #print(file_hash_in_dest_dir, get_count_of_files_in_dir(dest_dir), len(file_hash_in_dest_dir))

    # sys.exit()
    file_counter_for_same_name = 0
    file_counter_dest_dir_no_exif = 0
    file_counter_dest_dir = 0
    file_count_deleted = 0

    for root, dirs, files in os.walk(start_dir, topdown=True):
        for name in files:

            original_name = name
            original_name_with_path = os.path.join(root, name)
            filename, filename_ext = os.path.splitext(name)
            filename = clean_file_name(filename)

            if filename_ext.lower() in FILE_EXTENSIONS:

                video_date_converted = get_video_exif_info(original_name_with_path)

                if video_date_converted:
                    filename = set_exif_info_in_filename(video_date_converted, filename)
                    target_dir = dest_dir
                else:
                    target_dir = dest_dir_no_exif
                    error_message("\nAz EXIF információ nem elérhető... " + original_name)

                new_name = filename + filename_ext

                #print(new_name)

                file_hash = get_file_hash(original_name_with_path)

                # print("HASH elenőrzés: ", file_hash in file_hash_in_dest_dir)

                if file_hash in file_hash_in_dest_dir:
                    warning_message("Már létezik ugyanilyen tartalmú fájl" \
                        + "a célkönyvtárban, ezért törlöm a forráskönyvtárban...")
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

    if file_hash_in_dest_dir:
        save_file_hash_to_file(daily_config_filename, file_hash_in_dest_dir)

    summary_report(file_counter_dest_dir, file_counter_dest_dir_no_exif, file_counter_for_same_name, file_count_deleted)


if __name__ == "__main__":
    main()

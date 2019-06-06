# -*- coding: utf-8 -*-


import os

from jpg_collector_by_exif import get_dir, create_no_exif_data_dir, clean_file_name, open_file_hash_from_file, info_message,\
        save_file_hash_to_file, get_file_hash_in_dir, set_exif_info_in_filename, error_message,\
        warning_message, get_file_hash, set_timestamp_in_filename, get_count_of_files_in_dir


def get_exif_info_for_video(filename_with_path: str):

    """
    Try to get exif info from file (datetime_original).

    """
    dates = list()
    process = os.popen(
        'exiftool ' + filename_with_path.replace(" ", "\ ") \
        + ' | grep -e "Create Date" -e "Creation time" -e "File Access Date/Time" -e "File Modification Date/Time"', 'r', 1
        )
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


def main():

    #
    # start_dir = get_dir("forrás")
    # dest_dir = get_dir("cél")

    start_dir = "./sample_data/videos"
    dest_dir = "./videos"

    dest_dir_no_exif = create_no_exif_data_dir(dest_dir)

    file_hash_in_dest_dir = open_file_hash_from_file()

    if not file_hash_in_dest_dir or (len(file_hash_in_dest_dir) != get_count_of_files_in_dir(dest_dir)):
        info_message("A meglévő fájlok ellenőrzése a cél könyvtárban....")
        info_message("Sok fájl esetén a folyamat hosszabb ideig tart, várjon türelemmel...")
        file_hash_in_dest_dir = get_file_hash_in_dir(dest_dir)


    print(file_hash_in_dest_dir, get_count_of_files_in_dir(dest_dir), len(file_hash_in_dest_dir))

    file_counter_for_same_name = 0
    file_counter_dest_dir_no_exif = 0
    file_counter_dest_dir = 0
    file_count_deleted = 0

    dates = list()

    for root, dirs, files in os.walk(start_dir, topdown=True):
        for name in files:

            original_name = name
            original_name_with_path = os.path.join(root, name)
            filename, filename_ext = os.path.splitext(name)
            filename = clean_file_name(filename)

            video_date_converted = get_exif_info_for_video(original_name_with_path)

            if video_date_converted:
                filename = set_exif_info_in_filename(video_date_converted, filename)
                target_dir = dest_dir
            else:
                target_dir = dest_dir_no_exif
                error_message("\nAz EXIF információ nem elérhető... " + original_name)

            new_name = filename + filename_ext

            print(new_name)

            file_hash = get_file_hash(original_name_with_path)

            print("HASH elenőrzés: ", file_hash in file_hash_in_dest_dir)

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

    if file_hash_in_dest_dir:
        save_file_hash_to_file(file_hash_in_dest_dir)

    print(file_hash_in_dest_dir, get_count_of_files_in_dir(dest_dir))

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


if __name__ == "__main__":
    main()

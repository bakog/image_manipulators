# -*- coding: utf-8 -*-

import pytest
import os
import shutil
import time

from utils import create_no_exif_data_dir, clean_file_name, get_image_exif_info, get_video_exif_info, \
                    set_exif_info_in_filename, get_file_hash, set_date_in_filename, \
                    get_count_of_files_in_dir

working_dir = os.getcwd()
temp_root_dir_for_tests = os.path.join(working_dir, "tmp")
empty_dir = os.path.join(temp_root_dir_for_tests, "empty")
source_dir_for_tests = os.path.join(temp_root_dir_for_tests, "source")
target_dir_for_tests = os.path.join(temp_root_dir_for_tests, "target")
sample_dir = os.path.join(working_dir, "sample_data")
dest_dir_no_exif = target_dir_for_tests + "/no_exif_data"

picture_without_exif_1 = os.path.join(sample_dir, "images/pictures_without_exif/DSCN0017.JPG")
picture_with_exif_in_filename = os.path.join(sample_dir, "images/pictures_with_exif/080726_1019_2008_08_07_11_58_32.jpg")
picture_with_exif_not_in_filename = os.path.join(sample_dir, "images/pictures_with_exif/080726.jpg")

picture_without_exif_1_basename = os.path.basename(picture_without_exif_1)
picture_with_exif_in_filename_basename = os.path.basename(picture_with_exif_in_filename)
picture_with_exif_not_in_filename_basename = os.path.basename(picture_with_exif_not_in_filename)

video_without_exif_1 = os.path.join(sample_dir, "videos/videos_without_exif/bg1.mkv")
video_with_exif_in_filename = os.path.join(sample_dir, "videos/videos_with_exif/bg1_2014_02_19_11_56_05.flv")
video_with_exif_not_in_filename = os.path.join(sample_dir, "videos/videos_with_exif/MOV005.3gp")

filename1, filename1_ext = os.path.splitext(picture_with_exif_in_filename_basename)
filename2, filename2_ext = os.path.splitext(picture_with_exif_not_in_filename_basename)

def setup():

    shutil.copytree(sample_dir, source_dir_for_tests)
    os.mkdir(target_dir_for_tests)

def teardown():

    shutil.rmtree(temp_root_dir_for_tests)


def test_create_no_exif_data_dir_function():
    assert os.path.exists(dest_dir_no_exif) is False
    assert create_no_exif_data_dir(target_dir_for_tests) == dest_dir_no_exif


def test_clean_file_name_function():
    # with space
    assert clean_file_name("   ez egy rossz fajlnev  ") == "ez_egy_rossz_fajlnev"

    # with non alfanumeric char
    assert clean_file_name("ez egy@rossz:fajlnev  ") == "ez_egyrosszfajlnev"

    # with hungarian special chars
    assert clean_file_name("és ő rossz fájlnév  öüóőúéáűíÖÜÓŐÚÉÁŰÍ") == "es_o_rossz_fajlnev_ouooueauiouooueaui"

    # with multiple _
    assert clean_file_name("és ő rossz____ fájlnév__  öüóőúéáűíÖÜÓŐÚÉÁŰÍ___") == "es_o_rossz_fajlnev_ouooueauiouooueaui"


def test_get_image_exif_info_function():

    assert get_image_exif_info(picture_without_exif_1) is None
    assert get_image_exif_info(picture_with_exif_in_filename) == "2008_08_07_11_58_32"


def test_get_video_exif_info_function():

    assert get_video_exif_info(video_without_exif_1) is None
    assert get_video_exif_info(video_with_exif_in_filename) == "2014_02_19_11_56_05"

def test_set_exif_info_in_filename_function():


    assert "080726_1019_2008_08_07_11_58_32" in set_exif_info_in_filename("2008_08_07_11_58_32", filename1)
    assert "080726_2008_08_07_11_58_58" in set_exif_info_in_filename("2008_08_07_11_58_58_32", filename2)


def test_count_get_count_of_files_in_dir_function():

    assert get_count_of_files_in_dir(empty_dir) == 0
    assert get_count_of_files_in_dir(os.path.join(sample_dir, "images/pictures_with_exif")) == 2
    assert get_count_of_files_in_dir(os.path.join(sample_dir, "images")) == 9


def test_get_file_hash_function():
    assert get_file_hash(picture_with_exif_not_in_filename) == "f83ab5b8387d67b537cbf07ce6259d4a754b63d2043059c9e67b28cb6cc8ada7c37001e1af5007313d521989ccfb128d54aefc9b58e9b09790e09375eb31b544"


def test_set_date_in_filename_function():
    pass
# -*- coding: utf-8 -*-

import pytest
import os
import shutil
import time

from jpg_collector_by_exif import check_dir_exists, create_no_exif_data_dir, clean_file_name, get_exif_info, set_exif_info_in_filename


# ennek itt fuggvenyben kene lennie

working_dir = os.getcwd()  # sokkal jobb az __file__ a cwd az az ahol kiadod a parancsot, es nnem az ahol a file van
temp_root_dir_for_tests = os.path.join(working_dir, "tmp")
source_dir_for_tests = os.path.join(temp_root_dir_for_tests, "source")
target_dir_for_tests = os.path.join(temp_root_dir_for_tests, "target")
sample_dir = os.path.join(working_dir, "sample_data")
dest_dir_no_exif = target_dir_for_tests + "/no_exif_data"

picture_without_exif_1 = os.path.join(sample_dir, "pictures_without_exif/DSCN0017.JPG")
picture_with_exif_in_filename = os.path.join(sample_dir, "pictures_with_exif/080726_1019_2008_08_07_11_58_32.jpg")
picture_with_exif_not_in_filename = os.path.join(sample_dir, "pictures_with_exif/080726.jpg")


def setup():

    shutil.copytree(sample_dir, source_dir_for_tests)
    os.mkdir(target_dir_for_tests)

def teardown():

    shutil.rmtree(temp_root_dir_for_tests)


def test_check_dir_exists_function(): # ugy szoktak csinalni, hogy a negativ teszteket kulon veszik
    assert check_dir_exists(temp_root_dir_for_tests) == True
    assert check_dir_exists("/ez_nem_letezik") == False
# ha tobb assertet akarsz hasznalni, telepitsd a pytest_assume csomagot,
# itt ha az assert fail-el, akkor a kovetkezo mar nem kerul vegrehajtasra
# kijavitod a hibat, amit eloszor lattal, es a kovetkezo futaskor ujabb hiba johet elo

def test_create_no_exif_data_dir_function():
    assert check_dir_exists(dest_dir_no_exif) == False
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
# ezeket a vegtelensegig lehet kombinalni
# az otletek jok, de itt most eleg, ha mindez egy stringben van benne


def test_get_exif_info_function():

    assert get_exif_info(picture_without_exif_1) == None
    assert get_exif_info(picture_with_exif_in_filename) == "2008_08_07_11_58_32"

def teyt_set_exif_info_in_filename():
    assert get_exif_info(picture_with_exif_in_filename) == "080726_1019_2008_08_07_11_58_32.jpg"
    assert get_exif_info(picture_with_exif_not_in_filename) == "080726_1020_2008_08_07_11_58_58.jpg"
# ez itt egy erdekes typo ...
# merthogy nincsen az elejen test_
# igy nem fog lefutni a teszt, mindig meg kell nezni, hogy annyi teszt eredmeny van-e
# ahany tesztet irtal ;-)
# es persze figyelni kell a ha apycharm azt mondja, hogy typo van valahol
# es bar en is ritkan alakalmazom, ezert jo a TDD, mert irsz egy tesztet, es latod failelni
# ha elirtad a nevet, akkor nem fog fail-elni ;-)

# amugy jok a cuccok, csak igy tovabb


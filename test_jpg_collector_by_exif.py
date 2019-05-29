# -*- coding: utf-8 -*-

import pytest
import os
import shutil
import time

from jpg_collector_by_exif import check_dir_exists, create_no_exif_data_dir, clean_file_name

working_dir = os.getcwd()
temp_root_dir_for_tests = os.path.join(working_dir, "tmp")
source_dir_for_tests = os.path.join(temp_root_dir_for_tests, "source")
target_dir_for_tests = os.path.join(temp_root_dir_for_tests, "target")
sample_dir = os.path.join(working_dir, "sample_data")
dest_dir_no_exif = target_dir_for_tests + "/no_exif_data"


def setup():

    shutil.copytree(sample_dir, source_dir_for_tests)
    os.mkdir(target_dir_for_tests)

def teardown():

    shutil.rmtree(temp_root_dir_for_tests)


def test_check_dir_exists_function():
    assert check_dir_exists(temp_root_dir_for_tests) == True


def test_check_dir_no_exists_function():
    assert check_dir_exists("/ez_nem_letezik") == False


def test_create_no_exif_data_dir_function():
    assert check_dir_exists(dest_dir_no_exif) == False
    assert create_no_exif_data_dir(target_dir_for_tests) == dest_dir_no_exif

def test_clean_file_name_function():
    # with space
    assert clean_file_name("ez egy rossz fajlnev  ") == "ez_egy_rossz_fajlnev"

    # with non alfanumeric char
    assert clean_file_name("ez egy@rossz:fajlnev  ") == "ez_egyrosszfajlnev"

    # with hungarian special chars
    assert clean_file_name("és ő rossz fájlnév  ") == "es_o_rossz_fajlnev"


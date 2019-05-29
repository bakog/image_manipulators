# -*- coding: utf-8 -*-

import os
import pathlib

dirname = "./teszt_kepek"


print(" SCANDIR: \n")
with os.scandir(dirname) as items:
    for item in items:
        if item.is_file():
            print(item.name)


print("\n\n PATHLIB: \n")
for item in pathlib.Path(dirname).glob("*"):
    if item.is_file():
        print(item.name)



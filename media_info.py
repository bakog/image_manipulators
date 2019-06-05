# -*- coding: utf-8 -*-

import os
import sys
import subprocess

import sh


from subprocess import Popen, PIPE, check_output
dirname = os.getcwd()

filepath = os.path.join(dirname,'teszt_kepek/kepek_2')
os.chdir(filepath)

print(os.getcwd())

filename ="P1010379.MP4"

print(filepath)
process = Popen(['mediainfo', filename], stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()
process.wait()
print(stdout)
#
# #
# s = check_output(['mediainfo', filename])
# print("s = " + str(s))


info = list(sh.mediainfo(filename).split('\n'))

info_dict = {}
print(info)

for item in info:
    #print(item)
    if "Encoded date" in item:
        print(item)
        key, value = item.split(': ')
        info_dict[key.strip()] = value.strip()
        print("Dátum:", value[4:14])


print(info_dict['Encoded date'])

#print(sh.mediainfo('--Inform="Video;%DisplayAspectRatio%"',filename))

info = list(sh.exiftool(filename).split('\n'))
print(info)


process = os.popen('exiftool '+ filename + ' | grep "Create Date"', 'r', 1)

for item in process:
    egysor = item.split(":", 1)[1]
    print("sor:", type(egysor), egysor)


sor = "Media Create Date               : 2017:02:09 08:25:01"
print(sor.split(": ", 1)[1].replace(":", "_").replace(" ", "_"))
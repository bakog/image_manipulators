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
process = Popen(['mediainfo', '--Inform="[General]"', filename], stdout=PIPE, stderr=PIPE)
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
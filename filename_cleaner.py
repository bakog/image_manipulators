# -*- coding: utf-8 -*-

import re


string = " Hello $#! Peo_ple   White__space 7331 ,?;:.-§¬~+^!˘%°/˛=`(˙)´˝¨¸÷×$ß¤@ öüóőúéáűíÖÜÓŐÚÉÁŰÍ "
inkey = "öüóőúéáűíÖÜÓŐÚÉÁŰÍ"
outkey = "ouooueauiouooueaui"
# delkey = ',?;:.-§¬~+^!˘%°/˛=`(˙)´˝¨¸÷×$ß¤@'

# levágjuk a felesleges szóközöket és feldaraboljuk szóközönként, ha van benne
filename_part = list(string.strip().split())

# a fájlnév darabjai összefűzzük _ jellel
cleaned_string = "_".join(filename_part)

# kiszedjük a magyar ékezetes karaktereket
t = str.maketrans(inkey, outkey)
cleaned_string = cleaned_string.translate(t)

# eltávolítjuk az  összes nem odaillő karaktert, kivéve az _ jelet
cleaned_string = re.sub('[^A-Za-z0-9_]+', '', cleaned_string)

# levágjuk a felesleges _ jeleket a végeiről, majd a többször előforduló _ jelet egy _-ra cseréljük
cleaned_string = re.sub('_{2,}', '_', cleaned_string.strip('_'))

print(cleaned_string)

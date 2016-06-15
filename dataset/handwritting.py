import os
import sys

from PIL.ImageDraw import Draw
from PIL import ImageFont
from PIL import Image

import xml.etree.ElementTree as ET
from keras.preprocessing.image import *

def list_files(directory, ext='jpg|jpeg|bmp|png'):
    return [os.path.join(directory, f) for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f)) and ("."+ext in f)]


def decompose_word(img, word, font):
    x_size = img.size[0]
    letters = len(word)
    array = img_to_array(img)
    array.shape = (array.shape[1], array.shape[2])
    #print word, img.size
    draw = Draw(Image.new("L",(100,100)))

    total_font_size = float(draw.textsize(word, font)[0])

    data = []
    acc_size = 0
    for letter in word: #  range(0,x_size, x_size / len(word)):
        #print i*word_size,(i+1)*word_size, array.shape
        letter_size = draw.textsize(letter, font)[0]
        x = int(x_size*letter_size/total_font_size)
        #print acc_size, acc_size+x
        data.append((array[:,acc_size:(acc_size + x)],letter))
        acc_size = acc_size + x
  
    return data

def load_data(path):
    files = list_files(path, 'png')
    xmls = list_files(path, 'xml')
    font = ImageFont.truetype(path+'/times.ttf')
    data = []

    for xml in xmls:
        tree = ET.parse(xml)   
        root = tree.getroot()
        for x in root.iter('word'):
            fid = x.attrib['id']
            ftext = x.attrib['text']

            for f in files:
               if fid+".png" in f:
                   print "Loading",f,"->",ftext             
                   assert(not (" " in ftext))
                   data = data + decompose_word(load_img(f).convert('L'), ftext, font)
    return data

#for i,(data,letter) in enumerate(load_handimgs(sys.argv[1])):
  #print letter
  #img = array_to_img(data, "th")
  #print letter, data.shape, img.size
  #img.save("img-"+letter+"-"+str(i)+".bmp")
  #pl.show()



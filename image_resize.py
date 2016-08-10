# author: Run2, Kaggler
# author home page: https://www.kaggle.com/rightfit
# Apache 2.0 License

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

# Any results you write to the current directory are saved as output.

# Using the code from http://blog.iconfinder.com/detecting-duplicate-images-using-python/

import zipfile
import os
import io
from PIL import Image
import datetime

def dhash(image, hash_size = 16):
    imageHor = image.convert('LA').resize((hash_size+1, hash_size),Image.ANTIALIAS)
    pixels = list(imageHor.getdata())
    difference = []
    for row in range(hash_size):
        for col in range(hash_size):
            pixel_left = imageHor.getpixel((col, row))
            pixel_right = imageHor.getpixel((col+1, row))
            difference.append(pixel_left > pixel_right)
    decimal_value = 0
    hex_string = []
    for index, value in enumerate(difference):
        if value:
            decimal_value += 2**(index%8)
        if (index%8) == 7:
            hex_string.append(hex(decimal_value)[2:].rjust(2,'0'))
            decimal_value = 0

    horString = ''.join(hex_string)

    imageVer = image.convert('LA').resize((hash_size, hash_size + 1),Image.ANTIALIAS)
    pixels = list(imageVer.getdata())
    difference = []
    for row in range(hash_size):
        for col in range(hash_size):
            pixel_up = imageVer.getpixel((col, row))
            pixel_down = imageVer.getpixel((col, row + 1))
            difference.append(pixel_up > pixel_down)
    decimal_value = 0
    hex_string = []
    for index, value in enumerate(difference):
        if value:
            decimal_value += 2**(index%8)
        if (index%8) == 7:
            hex_string.append(hex(decimal_value)[2:].rjust(2,'0'))
            decimal_value = 0

    verString = ''.join(hex_string)

    return [horString, verString]


for zip_counter in [3]:
    imgzipfile = zipfile.ZipFile('Images_' + str(zip_counter)+'.zip')
    print ('Doing zip file ' + str(zip_counter))
    namelist = imgzipfile.namelist()
    # Comment this line below and uncomment the above line when you do for the whole set
    # namelist = imgzipfile.namelist()[:10]
    print ('Total elements ' + str(len(namelist)))

    img_id_hash = []
    counter = 1
    for name in namelist:
        imgdata = imgzipfile.read(name)
        if len(imgdata) > 0:
            counter += 1
            img_id = name[:-4]
            stream = io.BytesIO(imgdata)
            img = Image.open(stream)
            img_hash = dhash(img)
            img_id_hash.append([img_id] + img_hash)
            #hash_size = 16
            #img = img.convert('LA').resize((hash_size+1, hash_size), Image.ANTIALIAS)
            #name = name.replace('.jpg', '.png')
            #folders = '/'.join(name.split('/')[:-1])
            #os.makedirs(folders, exist_ok=True)
            #img.save(name)
        # Uncomment the lines below to get an idea of progress when you do for the whole set
        if counter%10000==0:
            print ('Done ' + str(counter) , datetime.datetime.now())
    df = pd.DataFrame(img_id_hash, columns=['image_id', 'hor_hash', 'ver_hash'])
    df.to_csv('image_hash_' + str(zip_counter) + '.csv', index=False)

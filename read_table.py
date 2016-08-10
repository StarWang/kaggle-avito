%load_ext autoreload
%autoreload 2
%matplotlib inline
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import predictor
import build_utils
import feature_utils
import read_utils
import time
from read_utils import *
plt.style.use('ggplot')

st = time.time()
pairTrain = readData('ItemPairs_train')
pairTest = readData('ItemPairs_test')

print ('reading info train and test...')
#infoTrain = readData('ItemInfo_train').drop(['attrsJSON', 'locationID', 'metroID'], axis=1)
infoTrain = readData('infoTrainHash')

infoTest = readData('ItemInfo_test').drop(['attrsJSON', 'locationID', 'metroID'], axis=1)
#infoTest = readData('infoTestHash')

#print ('converting images array...')
#boolVec = infoTrain['images_array'].isnull()
#infoTrain.loc[~boolVec, 'images_array'] = infoTrain.loc[~boolVec, 'images_array'].apply(lambda x: x.replace(' ', '').split(','))

print ('cleaning text...')
#infoTrain = feature_utils.cleanText(infoTrain, 'title')
#infoTrain = feature_utils.cleanText(infoTrain, 'description')
infoTest = feature_utils.cleanText(infoTest, 'title')
infoTest = feature_utils.cleanText(infoTest, 'description')

boolVec = infoTest['images_array'].isnull()
infoTest.loc[~boolVec, 'images_array'] = infoTest.loc[~boolVec, 'images_array'].apply(lambda x: x.replace(' ', '').split(','))

imgHashDict = readAllHash().set_index('image_id').to_dict()

#infoTrainHash = feature_utils.img2hash(infoTrain, imgHashDict)

cat = readData('Category')
loc = readData('Location')
sub = readData('Random_submission')
sub['probability'] = None
print ('done')
ed = time.time()
print ('time elapsed:', ed - st)

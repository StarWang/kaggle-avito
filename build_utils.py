import pandas as pd
import numpy as np
import time
from feature_utils import *


def buildFeatures(pair, info, completePairs=['price']):
    isTest = True if 'id' in pair.columns else False
    if not isTest:
        pair = pair.drop('generationMethod', axis=1)
    infoItem = info.itemID.unique()
    pair = pair.query('itemID_1 in @infoItem and itemID_2 in @infoItem').reset_index()

    print ('text to list...')
    st = time.time()
    if 'attrsJSON' in info.columns:
        info = info.drop('attrsJSON', axis=1)
    itemList = np.union1d(pair.itemID_1.unique(), pair.itemID_2.unique())
    print ('filtering...')
    info = info.query('itemID in @itemList').copy()
    print ('info size:', info.shape[0])
    print ('done')
    #info = cleanText(info, 'title')
    #info = cleanText(info, 'description')


    pair = pair.merge(info.add_suffix('_1')).merge(info.add_suffix('_2'))
    print ('pair size:', pair.shape[0])
    pair['hasPrice'] = isNull(pair, 'price')
    pair['hasImage'] = isNull(pair, 'images_array')
    print ('processing price and image...')

    if 'price' in completePairs:
        pair = pair.query('hasPrice == True').copy()
        pair = getDiff(pair, 'price')
        pair = getDiff(pair, 'price', percentage=False)
    if 'image' in completePairs:
        pair = pair.query('hasImage == True').copy()
        pair = hammingDistance(pair, 'horHash')
        pair = hammingDistance(pair, 'verHash')

    ed = time.time()
    print ('time elapsed:', ed - st)

    print ('train size:', pair.shape[0])
    st = time.time()

    print ('getting diff...')
    pair = getDiff(pair, 'lat')
    pair = getDiff(pair, 'lon')

    pair = getDiff(pair, 'lat', percentage=False)
    pair = getDiff(pair, 'lon', percentage=False)

    print ('getting sim...')
    pair = getSim(pair, 'title')
    pair = getSim(pair, 'description')

    ed = time.time()
    print ('time elapsed:', ed - st)

    features = ['latDiff', 'latDiffAbs', 'lonDiff', 'lonDiffAbs']
    features += ['titleSim', 'descriptionSim']
    if 'price' in completePairs:
        features += ['priceDiff', 'priceDiffAbs']
    if 'image' in completePairs:
        features += ['horHashMaxMinDist', 'horHashMinDist', 'verHashMaxMinDist', 'verHashMinDist']
    print ('feature num:', len(features))
    print ('features:', features)

    if not isTest:
        X = pair[features]
        print ('X size:', X.shape[0])
        y = pair['isDuplicate']
        return X, y
    else:
        X = pair[['id'] + features]
        print ('X size:', X.shape[0])
        return X



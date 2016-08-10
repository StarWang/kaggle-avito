import pandas as pd
import numpy as np
import string
import time

def isSame(df, attrName):
    return df[attrName + '_1'] == df[attrName + '_2']

def isNull(df, attrName):
    return (~df[attrName + '_1'].isnull()) & (~df[attrName + '_2'].isnull())

def getMin(df, attrName):
    series1 = df[attrName + '_1'].copy()
    series2 = df[attrName + '_2'].copy()
    boolVec = series1 > series2
    series1[boolVec] = series2[boolVec]
    return series1

def getDiff(df, attrName, percentage=True):
    attrMin = getMin(df, attrName)
    if percentage:
        df[attrName + 'Diff'] = (df[attrName + '_1'] - df[attrName + '_2']).abs().div(attrMin)
    else:
        df[attrName + 'DiffAbs'] = (df[attrName + '_1'] - df[attrName + '_2']).abs()

    return df

def cleanText(df, attrName):
    df = df.copy()
    boolVec = ~df[attrName].isnull()
    trans = str.maketrans({punc:None for punc in string.punctuation})
    df.loc[boolVec, attrName] = df.loc[boolVec, attrName].apply(lambda x: x.lower().translate(trans).split())
    return df

def img2hash(df):
    return df.groupby('itemID')['images_array'].apply(lambda x: pd.Series(x, name='images'))

def getSim(df, attrName):
    lst = []
    attrLst = np.dstack((df[attrName + '_1'].values, df[attrName + '_2'].values))[0]
    def getsim(x):
        try:
            attr1 = np.unique(x[0])
        except Exception as e:
            attr1 = np.array(['$#@%'])
        if len(attr1) < 1:
            attr1 = np.array(['$#@%'])
        try:
            attr2 = np.unique(x[1])
        except Exception as e:
            attr2 = np.array(['fdjaisoh'])
        if len(attr2) < 1:
            attr2 = np.array(['fdjaisoh'])
        return np.intersect1d(attr1, attr2).shape[0]/np.union1d(attr1, attr2).shape[0]

    lst = pd.DataFrame(list(zip(df['index'].values.tolist(), [getsim(x) for x in attrLst])), columns=['index', attrName + 'Sim'])

    return df.merge(lst)

def img2hash(info, imgHashDict):
    imgList = np.dstack((info.itemID.values, info.images_array.values))[0]
    st = time.time()
    def toHashList(x):
        itemID = x[0]
        array = x[1]
        if type(array) != type([1]):
            return [itemID, np.nan, np.nan]
        return [itemID, [imgHashDict['hor_hash'][x] for x in array if x in imgHashDict['hor_hash']],
                [imgHashDict['ver_hash'][x] for x in array if x in imgHashDict['ver_hash']]]
    lst = pd.DataFrame([toHashList(x) for x in imgList], columns=['itemID', 'horHash', 'verHash'])
    print (imgList)
    ed = time.time()
    print ('time elapsed:', ed - st)
    return info.merge(lst)

def hammingDistance(df, attrName):
    attrLst = np.dstack((df['index'].values, df[attrName + '_1'].values, df[attrName + '_2'].values))[0]
    def getMinMaxDistance(x):
        index = x[0]
        array1 = x[1]
        array2 = x[2]
        minDist = -1
        maxMinDist = -1
        if len(array1) > len(array2):
            array1, array2 = array2, array1
        for hash1 in array1:
            for hash2 in array2:
                dist = getDist(hash1, hash2)
                minDist = min(minDist, dist) if minDist != -1 else dist
            maxMinDist = max(minDist, maxMinDist) if maxMinDist != -1 else minDist
        return [index, maxMinDist, minDist]

    def getDist(x, y):
        count = 0
        z = int(x, 16)^int(y, 16)
        while z:
            count += 1
            z &= z-1 # magic!
        return count

    lst = pd.DataFrame([getMinMaxDistance(x) for x in attrLst], columns=['index', attrName + 'MaxMinDist', attrName + 'MinDist'])
    return df.merge(lst)


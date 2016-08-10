import pandas as pd
import numpy as np

def readData(csvName, nrows=None, fromOutput=False):
    dataDir = 'data/' if not fromOutput else 'out/'
    try:
        df = pd.read_csv(dataDir + csvName + '.csv', nrows=nrows)
    except Exception as e:
        df = pd.read_csv(dataDir + csvName + '.csv', engine='python', nrows=nrows)
    return df

def readHash(imageCount):
    df = readData('image_hash_' + str(imageCount))
    df['image_id'] = df['image_id'].apply(lambda x: x.split('/')[-1])
    return df

def readAllHash():
    lst = []
    for count in range(10):
        lst.append(readHash(count))
    return pd.concat(lst)


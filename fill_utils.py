


def fill(dfToFill, srcDf):
    columns = dfToFill.columns.tolist()[:]
    columns.remove('id')
    attrPred = columns[0]

    srcDf = dfToFill[['id']].merge(srcDf[['id', attrPred]], how='left')
    boolVec = dfToFill[attrPred].isnull()
    print ('na num before:', boolVec.sum())

    dfToFill = dfToFill.copy()
    dfToFill.loc[boolVec, attrPred] = srcDf.loc[boolVec, attrPred]

    boolVecAfter = dfToFill[attrPred].isnull()
    print ('na num after:', boolVecAfter.sum())
    print ('fill', boolVec.sum() - boolVecAfter.sum(), 'rows')
    return dfToFill

def output(filename, df, fillValue=None):
    df = df.copy()
    columns = df.columns.tolist()[:]
    columns.remove('id')
    attr = columns[0]
    print ('na num', df[attr].isnull().sum())
    if fillValue is not None:
        df.loc[df[attr].isnull(), attr] = fillValue
        filename = 'out/' + filename + '_fill_value_' + str(fillValue) + '.csv'
    else:
        filename = 'out/' + filename + '.csv'
    df.to_csv(filename, index=False)
    print ('output file:', filename)



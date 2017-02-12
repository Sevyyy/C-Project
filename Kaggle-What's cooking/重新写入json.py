# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 00:56:06 2015

@author: WQ
"""
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import csv

train = json.load(file('train.json'))
test = json.load(file('test.json'))
ass_rule = pd.read_csv('glgz.csv')
asset = set()
for i in ass_rule.values:
    asset.add(i[0])

for i in range(len(train)):
    l = len(train[i]['ingredients'])
    for k in range(l):
        for j in range(k+1,l):
            if train[i]['ingredients'][k] < train[i]['ingredients'][j]:
                new_word = train[i]['ingredients'][k] + '&' + train[i]['ingredients'][j]
            else:
                new_word = train[i]['ingredients'][j] + '&' + train[i]['ingredients'][k]
            if new_word in asset:
                train[i]['ingredients'].append(new_word)
    print i,'Done!'
for i in range(len(test)):
    l = len(test[i]['ingredients'])
    for k in range(l):
        for j in range(k+1,l):
            if test[i]['ingredients'][k] < test[i]['ingredients'][j]:
                new_word = test[i]['ingredients'][k] + '&' + test[i]['ingredients'][j]
            else:
                new_word = test[i]['ingredients'][j] + '&' + test[i]['ingredients'][k]
            if new_word in asset:
                test[i]['ingredients'].append(new_word)
    print i,'Done!'

print test[2]

fout = open('trainEX.json','w+')
fout.write(json.dumps(train))
fout.close()
fout = open('testEX.json','w+')
fout.write(json.dumps(test))
fout.close()               
print 'Done'
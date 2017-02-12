# -*- coding:utf-8 -*-
from __future__ import division
import json
import csv
import copy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def test_and_out(train,data,country_count,test):
    print 'begin test'
    ans_csv = file('ans.csv', 'wb')
    fout = csv.writer(ans_csv)
    for i in range(len(test)):
        ans = [test[i]['id']]
        cuisine = 'none'
        temp_chance = 1.0
        max_chance = 0.0
        for each in data:
            for key in range(len(test[i]['ingredients'])):
                if test[i]['ingredients'][key] in data[each].keys():
                    temp_chance *= data[each][test[i]['ingredients'][key]] * 10
            temp_chance *= country_count[each] / len(train)
            if temp_chance > max_chance:
                cuisine = each
                max_chance = temp_chance
            temp_chance = 1.0
        ans = ans + [cuisine]
        fout.writerow(ans)
    ans_csv.close()

def test_and_change(train,data,country_count,test):
    for i in range(len(test)):
        ans = test[i]['cuisine']
        cuisine = 'none'
        temp_chance = 1.0
        max_chance = 0.0
        for each in data:
            for key in range(len(test[i]['ingredients'])):
                if test[i]['ingredients'][key] in data[each].keys():
                    temp_chance *= data[each][test[i]['ingredients'][key]] * 10
            temp_chance *= country_count[each] / len(train)
            if temp_chance > max_chance:
                cuisine = each
                max_chance = temp_chance
            temp_chance = 1.0
        if cuisine != ans:
            for key in range(len(test[i]['ingredients'])):
                data[cuisine][test[i]['ingredients'][key]] *= 0.995
                data[ans][test[i]['ingredients'][key]] *= 1.005

def train(train,data,country_count):
    print 'begin train'
    for i in range(len(train)):
        this_country = train[i]
        country_count[this_country['cuisine']] += 1
        for j in range(len(this_country['ingredients'])):
            data[this_country['cuisine']][this_country['ingredients'][j]] += 1
    for each in data:
        for key in data[each]:
            data[each][key] = (data[each][key] + 20.0 * country_count[each] / len(train) ) * 1.0 / (country_count[each] + 20)

def init(train,data,country_count):

def data_out(data,data_name,country_count,country_count_name):
    fout = open(data_name,'w+')
    fout.write(json.dumps(data))
    fout.close()
    fout = open(country_count_name,'w+')
    fout.write(json.dumps(country_count))
    fout.close()

def init_from_file(data_name,country_count_name):
    data_file = file(data_name)
    data = json.load(data_file)
    country_count_file = file(country_count_name)
    country_count = json.load(country_count_file)
    return data,country_count

# get data
training_file = file('train.json')
train_all = json.load(training_file)
testing_file = file('test.json')
test_all = json.load(testing_file)
# devide into two parts
train_1 = train_all[0:20000]
train_2 = train_all[20001:]

# data init
data_all = {}
data_1 = {}
data_2 = {}
country_count_all = {}
country_count_1 = {}
country_count_2 = {}
init(train_all,data_all,country_count_all)
init(train_all,data_1,country_count_1)
init(train_all,data_2,country_count_2)

# data train or read data from file
train(train_1,data_1,country_count_1)
train(train_2,data_2,country_count_2)
data_1,country_count_1 = init_from_file('data_1.json','country_count_1.json')
data_2,country_count_2 = init_from_file('data_2.json','country_count_2.json')

# train and update the data
for i in range(14):
    test_and_change(train_1,data_1,country_count_1,train_2)
for i in range(14):
    test_and_change(train_2,data_2,country_count_2,train_1)

# write the updated data to file
data_out(data_1,'data_1.json',country_count_1,'country_count_1.json')
data_out(data_2,'data_2.json',country_count_2,'country_count_2.json')

#get the data_all
for each in data_all:
    for key in data_all[each]:
        data_all[each][key] = (data_1[each][key] + data_2[each][key]) * 1.0 / 2.0
for each in country_count_all:
    country_count_all[each] = country_count_1[each] + country_count_2[each]

# test the testing set and print the ans
test_and_out(train_all,data_all,country_count_all,test_all)

# close file
training_file.close()
testing_file.close()

# a 'done' for the symbol of the end of the program
print "Done!"


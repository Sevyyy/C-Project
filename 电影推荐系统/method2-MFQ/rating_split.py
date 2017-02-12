#usage: python rating_split.py <num_of_split> rating_small.csv
#if <num_of_split> is 4,
#then rating_train.csv will get 3/4 records and rating_test.csv will get the rest 1/4

import sys
import csv

def split(k, file):
	dict_of_user_movies = {}
	i = 0
	with open(file,'r') as f:
		for line in f:
			if i == 0:
				i = i + 1
				continue

			user, movie, rating, timestamp = line.split(',')
			if dict_of_user_movies.get(int(user)) is None:
				dict_of_user_movies[int(user)] = []
			dict_of_user_movies[int(user)].append((int(user),int(movie),float(rating),int(timestamp)))
	#print(dict_of_user_movies)
	
	train = open('rating_train.csv', 'wb')
	train_writer = csv.writer(train)
	train_writer.writerow(('userid','movieid','rating','timestamp'))
	test = open('rating_test.csv', 'wb')
	test_writer = csv.writer(test)
	test_writer.writerow(('userid','movieid','rating','timestamp'))
	for user in dict_of_user_movies:
		total_num = len(dict_of_user_movies[user])
		test_num = total_num / k
		train_num = total_num - test_num
		i = 0
		for item in dict_of_user_movies[user]:
			if i < train_num:
				train_writer.writerow(item)
			else:
				test_writer.writerow(item)
			i = i + 1

	train.close()
	test.close()

if __name__ == '__main__':
    #python rating_split.py <num_of_split> rating_small.csv
    if len(sys.argv) == 3:
    	k = int(sys.argv[1])
    	file = sys.argv[2]

        split(k, file)
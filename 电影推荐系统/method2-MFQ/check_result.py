#python check_result.py mf_result.txt <rating_test> <movie_file>

import sys
import csv
import codecs

def build_movie_dict(movies_file):
    i = 0
    movie_id_dict = {}

    with codecs.open(movies_file, 'r', 'latin-1') as f:
        for line in f:
            if i == 0:
                i = i + 1
                continue

            movieId, title, genre = line.split(',')
            movie_id_dict[int(movieId)] = i
            i = i + 1
    return movie_id_dict

def check(result_file, test_file, movie_dict):
	user_num = 50
	movie_num = 1000
	result_data = {}
	i = 0
	with open(result_file) as r:
		for line in r:
			result_data[i] = line.split(',')
			i = i + 1

	#print(result_data)

	predict = open('predict.csv', 'wb')
	writer = csv.writer(predict)
	writer.writerow(('userid','movieid','rating','predict','miss'))

	i = 0
	totalMiss = 0
	maxMiss = 0
	correct = 0
	with open(test_file,'r') as f:
		for line in f:
			if i == 0:
				i = i + 1
				continue

			user, movie, rating, timestamp = line.split(',')
			id = movie_dict[int(movie)]
			pre = round(float(result_data[int(user) - 1][id - 1]), 1)
			miss = round(abs(float(rating) - pre), 1)
			if miss > maxMiss:
				maxMiss = miss
			if miss <= 1.0:
				correct = correct + 1
			totalMiss = totalMiss + miss
			writer.writerow((int(user), int(movie), float(rating), pre, miss))
			i = i + 1
	i = i - 1

	predict.close()
	print 'Total miss is', round(totalMiss,1)
	print 'The max miss is', round(maxMiss,1)
	print 'The correct prediction rate is', round(float(correct)/float(i),5)

if __name__ == '__main__':
    #python check_result.py mf_result.txt <rating_test> <movie_file>
    if len(sys.argv) == 4:
    	result_file = sys.argv[1]
    	test_file = sys.argv[2]
    	movie_file = sys.argv[3]
    	movie_id_dict = build_movie_dict(movie_file)

        check(result_file, test_file, movie_id_dict)
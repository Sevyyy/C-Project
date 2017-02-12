#usage: python getSmallData.py [num_movies] movies.csv [num_users] ratings.csv

import sys
import csv

def get_small(num_movies, movie_file, num_users, rating_file):
	file = open(movie_file, 'r')
	all_movie = csv.reader(file)

	csvfile = open('movies_small.csv', 'wb')
	writer = csv.writer(csvfile)
		
	i = 0
	max_movie_id = 1
	for row in all_movie:
		writer.writerow(row)
		if i >= num_movies:
			max_movie_id = int(row[0])
			break
		i = i + 1

	print(max_movie_id)

	file.close()
	csvfile.close()

	file = open(rating_file, 'r')
	all_rating = csv.reader(file)

	csvfile = open('rating_small.csv', 'wb')
	writer = csv.writer(csvfile)

	i = 0
	for row in all_rating:
		if i == 0:
			writer.writerow(row)
			i = i + 1
			continue

		if int(row[0]) > num_users:
			break
		elif int(row[1]) > max_movie_id:
			continue
		else:
			writer.writerow(row)

	file.close()
	csvfile.close()

def main(num_movies, movie_file, num_users, rating_file):
	get_small(num_movies, movie_file, num_users, rating_file)
	
if __name__ == '__main__':
    #python getSmallData.py num_movies movies.csv num_users ratings.csv
    if len(sys.argv) == 5:
    	num_movies = int(sys.argv[1])
        movie_file = sys.argv[2]
        num_users = int(sys.argv[3])
        rating_file = sys.argv[4]

        main(num_movies, movie_file, num_users, rating_file)
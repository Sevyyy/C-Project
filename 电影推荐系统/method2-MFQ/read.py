#read all data and print in csv as a matrix
#usage: python read.py <rating file> <movie file>

import sys, numpy as np
from numpy import genfromtxt
import codecs

#build movie dicitionary with line number as numpy movie id and genre set
def build_info(movies_file):
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

#read data
def read_data(input_file, movies_dict):
    #number of users
    users = 50
    
    #number of movies
    movies = 1000
    
    #initialize matrix X
    X = np.zeros(shape = (users, movies))
    i = 0

    #X = genfromtxt(input_file, delimiter=",",dtype=str)
    with open(input_file,'r') as f:
        for line in f:
            if i == 0:
                i = i + 1
                continue
            #split every line
            user, movie_id, rating, timestamp = line.split(',')
            #get its id in movies_dict
            id = movies_dict[int(movie_id)]
            #set his/her rating
            X[int(user) - 1, id - 1] = float(rating)
            
    return X

#main function
def main(movies_file, ratings_file):
    #build a dictionary of movie id mapping with counter of number of movies 
    #and get genre set, genres_dict
    movies_dict = build_info(movies_file)
    #read data and return a numpy array
    X = read_data(ratings_file, movies_dict)

    #training result
    #Predicted numpy array of users and movie rating
    np.savetxt('?.csv', X, delimiter=',')


if __name__ == '__main__':
    #makeMatrix.py <rating file> <movie file>
    if len(sys.argv) == 3:
        ratings_file =  sys.argv[1]
        movies_file = sys.argv[2]

        #main function
        main(movies_file, ratings_file)
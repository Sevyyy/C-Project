#Implementing regularized Non-negative Matrix factorization using Regularized gradient descent
#usage: python makeMatrix.py <rating file> <movie file>
import sys, numpy as np
from numpy import genfromtxt
import codecs
from numpy import linalg as LA

#build movie dicitionary with line number as numpy movie id and genre set
def build_info(movies_file):
    i = 0
    movie_id_dict = {}
    genres = set([])

    with codecs.open(movies_file, 'r', 'latin-1') as f:
        for line in f:
            if i == 0:
                i = i + 1
                continue

            movieId, title, genre = line.split(',')
            movie_id_dict[int(movieId)] = i
            all_genre = genre.split('|')
            for g in all_genre:
                genres.add(g)
            i = i + 1
    return movie_id_dict, genres

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

#build genre dictionary
def build_genre_dict(genres):
    genres_dict = {}
    i = 1
    for g in genres:
        genres_dict[g] = i
        i = i + 1

    return genres_dict

#generate matrix Q
def genre_movie(movies_file, genres_num, movies_dict, genres_dict):
    #number of movies
    movies_num = 1000

    #initialize matrix Q
    Q = np.zeros(shape = (genres_num, movies_num))

    i = 0
    with codecs.open(movies_file, 'r', 'latin-1') as f:
        for line in f:
            if i == 0:
                i = i + 1
                continue

            movieId, title, genre = line.split(',')
            id = movies_dict[int(movieId)]
            genres = genre.split('|')
            for g in genres:
                #set movie with this genre to 1
                Q[int(genres_dict[g]) - 1, id - 1] = 1

    return Q

# non negative regulaized matrix factorization implemention
def matrix_factorization(X, P, Q, genres_num, steps, alpha, beta):
    for step in xrange(steps):
        print step
        #for each user
        for i in xrange(X.shape[0]):
            #for each item
            for j in xrange(X.shape[1]):
                if X[i][j] > 0:
                    #calculate the error of the element
                    eij = X[i][j] - np.dot(P[i,:],Q[:,j])
                    #second norm of P and Q for regularilization
                    ##sum_of_norms = 0
                    #for k in xrange(K):
                    #    sum_of_norms += LA.norm(P[:,k]) + LA.norm(Q[k,:])
                    #added regularized term to the error
                    ##sum_of_norms += LA.norm(P) + LA.norm(Q)
                    #print sum_of_norms
                    ##eij += ((beta / 2) * sum_of_norms)
                    #print eij
                    #compute the gradient from the error
                    for k in xrange(genres_num):
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - (beta * P[i][k]))
                        #Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - (beta * Q[k][j]))

        #compute total error
        error = 0
        #for each user
        for i in xrange(X.shape[0]):
            #for each item
            for j in xrange(X.shape[1]):
                if X[i][j] > 0:
                    error += np.power(X[i][j] - np.dot(P[i,:],Q[:,j]),2)
        print(error)
        if error < 10:
            break
    return P, Q

#main function
def main(movies_file, ratings_file):
    #build a dictionary of movie id mapping with counter of number of movies 
    #and get genre set, genres_dict
    movies_dict, genres = build_info(movies_file)
    genres_dict = build_genre_dict(genres)
    #read data and return a numpy array
    X = read_data(ratings_file, movies_dict)
    
    #number of users
    N = X.shape[0]
    #number of movies
    M = X.shape[1]
    #P: an initial matrix of dimension N x size of genres
    P = np.random.rand(N, len(genres))
    #Q : a matrix of (genre, movie)
    Q = genre_movie(movies_file, len(genres), movies_dict, genres_dict)
    #steps : the maximum number of steps to perform the optimisation, hardcoding the values
    #alpha : the learning rate, hardcoding the values
    #beta  : the regularization parameter, hardcoding the values
    steps = 5000
    alpha = 0.0002
    beta = float(0.02)

    #training result
    estimated_P, estimated_Q = matrix_factorization(X, P, Q, len(genres), steps, alpha, beta)

    #Predicted numpy array of users and movie ratings
    modeled_X = np.dot(estimated_P, Q)
    np.savetxt('mf_result.txt', modeled_X, delimiter=',')

if __name__ == '__main__':
    #makeMatrix.py <rating file> <movie file>
    if len(sys.argv) == 3:
        ratings_file =  sys.argv[1]
        movies_file = sys.argv[2]

        #main function
        main(movies_file, ratings_file)

#!/usr/bin/env python
import sys, numpy as np
from numpy import genfromtxt
import codecs
from numpy import linalg as LA

def build_movies_dict(movies_file):
    i = 0
    movie_id_dict = {}
    with codecs.open(movies_file, 'r', 'latin-1') as f:
        for line in f:
            if i == 0:
                i = i+1
            else:
                movieId,title,genres = line.split(',')
                movie_id_dict[int(movieId)] = i-1
                i = i +1
    return movie_id_dict

def read_data(input_file,movies_dict):
    users = 718
    movies = 8927

    X = np.zeros(shape=(users,movies))
    i = 0

    with open(input_file,'r') as f:
        for line in f:
            if i == 0:
                i = i +1
            else:
                user,movie_id,rating,timestamp = line.split(',')
                id = movies_dict[int(movie_id)]
                X[int(user)-1,id] = float(rating)
                i = i+1
    return X

def R1MP(Y, r):
    print('Begin r1mp')
    #################################
    #Y means the input matrix
    #idx means the index of the omega
    #r means the iteration times
    #################################
    row = Y.shape[0]
    column = Y.shape[1]
    length = row * column
    X = np.zeros((row, column))

    M1 = np.zeros((length, r))
    M11 = M1
    Y1 = np.zeros((length, 1))
    y = Y.reshape((length, 1), order = 'F')

    idx = []
    for i in range(length):
        if y[i] != 0:
            idx.append(i)
    idx = np.array(idx)


    for k in range(r):
        print(k)
        #step one
        R = Y - X     #regression residual
        X = 0;        #???
        print('Begin svd')
        u,S,v = LA.svd(R)
        print('Begin dot')
        M = np.dot(u[:,0].reshape((row,1), order = 'F'),v[0,:].reshape((1,column), order = 'F'))
        #step two
        print('begin step two')
        m1 = np.zeros((length,1))
        m = M.reshape((length,1), order = 'F')
        m1[idx] = m[idx]
        M1[:,k] = m1.reshape(1,length)
        M11[:,k] = m.reshape(1,length)
        print('Begin inv')
        invMTM = LA.inv(np.dot(M1[:,0:k+1].T,M1[:,0:k+1]))
        print('Begin update theta')
        print(invMTM.shape)
        print(M1[:,0:k+1].T.shape)
        theta = np.dot(np.dot(invMTM,M1[:,0:k+1].T),y)
        print(theta)
        print('Step three')
        #step three
        for i in range(k+1):
            Mi = M1[:,i].reshape((row,column), order = 'F')
            X = X + theta[i]*Mi
        if k == r:
            Y1 = np.dot(M11, theta)
            Y1 = Y1.reshape((row, column), order = 'F')
    return Y1



def matrix_factorization(X,P,Q,K,steps,alpha,beta):
    Q = Q.T
    for step in xrange(steps):
        print step
        for i in xrange(X.shape[0]):
            for j in xrange(X.shape[1]):
                if X[i][j] > 0 :
                    eij = X[i][j] - np.dot(P[i,:],Q[:,j])
                    sum_of_norms = 0
                    sum_of_norms += LA.norm(P) + LA.norm(Q)
                    eij += ((beta/2) * sum_of_norms)
                    for k in xrange(K):
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - (beta * P[i][k]))
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - (beta * Q[k][j]))
        error = 0
        for i in xrange(X.shape[0]):
            for j in xrange(X.shape[1]):
                if X[i][j] > 0:
                    error += np.power(X[i][j] - np.dot(P[i,:],Q[:,j]),2)
        print(error)
        if error < 0.001:
            break
    return P, Q.T

def main(X,K):
    N= X.shape[0]
    M = X.shape[1]
    
    P = np.random.rand(N,K)
    Q = np.random.rand(M,K)
    steps = 5000
    alpha = 0.0002
    beta = float(0.02)
    #estimated_P, estimated_Q = matrix_factorization(X,P,Q,K,steps,alpha,beta)
    #modeled_X = np.dot(estimated_P,estimated_Q.T)
    result = R1MP(X,100)
    np.savetxt('mf_result.txt', result, delimiter=',')

if __name__ == '__main__':
    if len(sys.argv) == 4:
        ratings_file =  sys.argv[1]
        no_of_features = int(sys.argv[2])
        movies_mapping_file = sys.argv[3]
        movies_dict = build_movies_dict(movies_mapping_file)
        numpy_arr = read_data(ratings_file,movies_dict)
        main(numpy_arr,no_of_features)

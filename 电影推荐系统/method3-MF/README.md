To run the project:

If you want get small dataset:
    $python getSmallData.py [num_movies] movies.csv [num_users] ratings.csv
    it generate movies_small.csv and rating_small.csv

For small dataset:

1.  Split rating_file into rating_train.csv and rating_test.csv:

    $python rating_split.py <num_of_split> rating_small.csv

2.  Steps to run the code to build matrix factorization model:
    Don't forget to change number of users and number of movies in this code!
    
    $python MatrixFactorization.py rating_train.csv <num_hidden_layers> movies_small.csv

    This steps takes a long time, and it generate a result called mf_result.txt

3.  Steps to show prediction and real rating:

    $python check_result.py mf_result.txt rating_test.csv movies_small.csv

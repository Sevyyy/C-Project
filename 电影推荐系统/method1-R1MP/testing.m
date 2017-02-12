clc;
clear all;

train = csvread('big_train.csv');
test = csvread('big_test.csv');
[row, column] = size(train);

train_reshape = reshape(train, row*column, 1);
test_reshape = reshape(test, row*column, 1);
ii = 0;
jj = 0;
for i = 1 : row*column
    if train_reshape(i) ~= 0
        ii = ii + 1;
        idx(ii) = i;%训练集
    end
    if test_reshape(i) ~= 0
        jj = jj + 1;
        idy(jj) = i;%测试集
    end
end

tic;
[Matrix] = ER1MP(train,idx,50);%R1MP
toc;

result_reshape = reshape(Matrix, row*column, 1);
real_answer = test_reshape(idy);
predict_answer = result_reshape(idy);

pre = abs(real_answer - predict_answer);
sum(pre)
count = 0;
for i = 1:jj
    if pre(i) <= 1.0
        count = count + 1;
    end
end

disp(['rate = ', num2str(count / jj)]);
mat0 = zeros(row*column,1);
mat21 = zeros(row*column,1);

mat0(idy) = Matrix(idy);
mat21(idy) = test(idy);
rmse = RMSE(mat0,mat21,length(idy));%训练结果与测试集之间的RMSE
disp(num2str(rmse)); 
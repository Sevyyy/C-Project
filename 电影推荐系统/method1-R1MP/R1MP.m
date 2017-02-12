function [Y1] = R1MP(Y ,idx , r)
%%%%%%%%%%%%
%输入: 投影矩阵Y,投影坐标idx，迭代次数r
%输出: 复原矩阵
%注意: idx为投影矩阵Y变换为向量后对应的下标
%%%%%%%%%%%%

addpath(genpath('.\private'));
%init
[row,column] = size(Y);
len = row * column;
X = zeros(row,column);

M1 = zeros(len,r);%调整矩阵
M11 = M1;
Y1 = zeros(len,1);
y = reshape(Y,len,1);%列向量合并,大小 (row*column)*1
for  k = 1 : r
    disp(num2str(k));
    %step one
    R = Y - X;%残差矩阵
    X = 0;

    [u, S, v] = lansvd(R,1,'L');%求最大奇异向量
    M = u * v';%秩一矩阵
    
    %step two
    m1 = zeros(len, 1);
    m = reshape(M, len, 1);%列向量合并
    m1(idx) = m(idx);
    M1(:,k) = m1;%大小(row*column)*k
    M11(:,k) = m;
    theta = (M1(:,1:k)' * M1(:,1:k))^(-1) * M1(:,1:k)' * y;%theta大小 k*1
    
    %step three
    for i = 1 : k
        Mi = reshape(M1(:,i),row,column);
        X = X + theta(i)*Mi;%估计值更新
    end
    
    if(k == r)
        Y1 = M11*theta;
        Y1 = reshape(Y1,row,column);  
    end
end

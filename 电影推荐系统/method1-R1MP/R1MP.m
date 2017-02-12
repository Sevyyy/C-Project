function [Y1] = R1MP(Y ,idx , r)
%%%%%%%%%%%%
%����: ͶӰ����Y,ͶӰ����idx����������r
%���: ��ԭ����
%ע��: idxΪͶӰ����Y�任Ϊ�������Ӧ���±�
%%%%%%%%%%%%

addpath(genpath('.\private'));
%init
[row,column] = size(Y);
len = row * column;
X = zeros(row,column);

M1 = zeros(len,r);%��������
M11 = M1;
Y1 = zeros(len,1);
y = reshape(Y,len,1);%�������ϲ�,��С (row*column)*1
for  k = 1 : r
    disp(num2str(k));
    %step one
    R = Y - X;%�в����
    X = 0;

    [u, S, v] = lansvd(R,1,'L');%�������������
    M = u * v';%��һ����
    
    %step two
    m1 = zeros(len, 1);
    m = reshape(M, len, 1);%�������ϲ�
    m1(idx) = m(idx);
    M1(:,k) = m1;%��С(row*column)*k
    M11(:,k) = m;
    theta = (M1(:,1:k)' * M1(:,1:k))^(-1) * M1(:,1:k)' * y;%theta��С k*1
    
    %step three
    for i = 1 : k
        Mi = reshape(M1(:,i),row,column);
        X = X + theta(i)*Mi;%����ֵ����
    end
    
    if(k == r)
        Y1 = M11*theta;
        Y1 = reshape(Y1,row,column);  
    end
end

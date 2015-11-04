n= 6; %number of nodes
d = [1 3 3 3 4 0]; %out links per node
dP = .85; %Random jump probability
probDist = zeros(n, 100);
%Initial Probability Matrix
probDist(:, 1)  = [1/n; 1/n; 1/n; 1/n; 1/n; 1/n];

%Adjacency Matrix Representation of the tree
A = [0 1 0 0 0 0; 0 0 1 1 1 0 ; 0 1 0 1 1 0; 0 1 1 0 1 0; 0 1 1 1 0 1;
    0 0 0 0 0 0];

% Make Transition Probablilty Matrix 
for i = 1:n
    if A(i, :) == 0 % when we have a sink note
        P(i, :) = 1/n;
    else
        for j = 1:n
            if A(i, j) == 1
                P(i, j) = dP*1/d(i) + (1-dP)*1/n;
            else
                P(i, j) = (1-dP)*1/n;
            end
        end
    end
end

tol = 1e-5;
i = 1;
probDist(:, 2) = probDist(:, 1)'*P;
i = 2;
% Execute iterative scheme
while(abs(norm(probDist(:, i-1)-probDist(:, i))) >tol)
   probDist(:, i+1) = probDist(:, i)'*P;
    i = i +1;
end
probDist(:, i-1)



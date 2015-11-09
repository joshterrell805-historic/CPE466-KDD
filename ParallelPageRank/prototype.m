clear all
dP = .95; %Random jump probability
n = 250; %number of nodes
tol = 1e-4; %error tol and dP for testing (Lupo said use these)
probDistA = zeros(n, 100);
probDistB = zeros(n, 100);
%Adjacency Matrix Representation of the tree
%A = [0 1 0 0 0 0; 0 0 1 1 1 0 ; 0 1 0 1 1 0; 0 1 1 0 1 0; 0 1 1 1 0 1;
 %   0 0 0 0 0 0];

%Make a random nxn adjacency matix
A = rand(n, n)>.8;
d = ones(n, 1);
probDistA(:, 1)  = 1/n;
probDistB(:, 1)  = 1/n;

%Get outnode vector
d = A*d;

% Make Transition Probablilty Matrix 
for i = 1:n
    if A(i, :) == 0 % when we have a sink node
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

P2 = sparse(P- ones(n, n)*(1-dP)/n); % we wont actually do this this way

% Execute iterative scheme
%NEW WAY
toAdd = ones(1, n)*(1-dP)/n*sum(probDistA(:, 1));
probDistA(:, 2) = probDistA(:, 1)'*P2+toAdd;
i = 2;
error = 10;
%maybe we find a better way to quantify the difference (error)
while(n*error/dP >tol) 
   toAdd = ones(1,n)*((1-dP)/n)*sum(probDistA(:,i));
   probDistA(:, i+1) = probDistA(:, i)'*P2 + toAdd;
   error = abs(probDistA(1, i+1)-probDistA(1, i));
   i = i +1;
end

%OLD WAY
probDistB(:, 2) = probDistB(:, 1)'*P;
i = 2;
while(abs(norm(probDistB(:, i-1)-probDistB(:, i))) >tol)
%    probDistA(:, i+1) = probDistA(:, i)'*(A*dPd' +v);
    probDistB(:, i+1) = probDistB(:, i)'*P;
    i = i +1;
end
   
%Find the actual rankings by sorting the values and storing the indices in
%order
savei = i-1;
L = probDistA(:, savei);
Lsort = sort(L, 1);
i = 1;
while(i<=n)
    ind = find(L == Lsort(i, 1));
        for j = 0:length(ind)-1
            sortOrderL(j+i) = ind(j+1);
        end
        i = i +j+1;
 end

M = probDistB(:, savei);
Msort = sort(M, 1);
i = 1;
j = 0;
while(i<=n)
    ind = find(M == Msort(i, 1));
        for j = 0:length(ind)-1
            sortOrderM(j+i) = ind(j+1);
        end
        i = i +j+1;
end

%compare old way (M) to new way (L)
for i = 1:n
    if sortOrderM(i)~=sortOrderL(i)
        disp('IT DIDNT WORK')
        break;
    end
end


%Morgans Approximation way-- doesn't work
% cheat = probDistB(:, 1)'*(trace(P2)^(savei))*P2;
% N = cheat'/norm(cheat);
% Nsort = sort(N, 1);
% i = 1;
% j= 0;
% while(i<=n)
%     ind = find(N == Nsort(i, 1));
%         for j = 0:length(ind)-1
%             sortOrderN(j+i) = ind(j+1);
%         end
%         i = i +j+1;
% end
% 
% sorted = [sortOrderM' sortOrderL' sortOrderN'];



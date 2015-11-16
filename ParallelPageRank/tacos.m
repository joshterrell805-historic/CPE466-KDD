clear all
dP = .95; %Random jump probability
n = 6; %number of nodes
tol = 1e-4; %error tol and dP for testing (Lupo said use these)
probDistA = zeros(n, 10);
probDistB = zeros(n, 10);
%Adjacency Matrix Representation of the tree
A = [0 1 0 0 0 0; 0 0 1 1 1 0 ; 0 1 0 1 1 0; 0 1 1 0 1 0; 0 1 1 1 0 1;
    0 0 0 0 0 0];

%Make a random nxn adjacency matix
%A = rand(n, n)>.8;
d = ones(n, 1);
probDistA(:, 1)  = 1/n;
probDistB(:, 1)  = 1/n;
norm(probDistA(:, 1))
%Get outnode vector
d = A*d;
sink = zeros(n, 1);
for i = 1:n
    if ~d(i)
        sink(i) = 1;
    end
end

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
P2 = zeros(n, n);
%P2 = sparse(P- ones(n,n)*(1-dP)/n); % we wont actually do this this way
for i = 1:n
        for j = 1:n
            if A(i, j) == 1
                P2(i, j) = dP/d(i);
            end
        end
end

% Execute iterative scheme
%NEW WAY
 toAdd = ((1-dP)/n)*sum(probDistA(:, 1));
 toAdd = toAdd + sum(sink .* probDistA(:, 1)) * dP/n;
 probDistA(:, 2) = P2'*probDistA(:, 1)+toAdd ;
% toAdd = (1-dP)/n*sum(probDistA(:, 2))+sink*dP/n*sum(probDistA(:,2));
i = 2;
%i = 1;
error = 10;
%maybe we find a better way to quantify the difference (error)
%while(i<n+1) 
%toAddA = ((1-dP)/n)*sum(probDistA(:, 1));
%toAdd = toAddA + sum(sink .* probDistA(:, 2)) * dP/n;
toAdd = (1-dP)/n;
while(norm(probDistA(:, i-1)-probDistA(:, i)) >tol)
%while(i<n+1);
    probDistA(:, i+1) = P2'*probDistA(:, i) + toAdd;
 %  error = abs(probDistA(1, i+1)-probDistA(1, i));
   i = i +1;
end
saveiL = i-1;
%OLD WAY
probDistB(:, 2) = probDistB(:, 1)'*P;
i = 2;
while(abs(norm(probDistB(:, i-1)-probDistB(:, i))) >tol)
%    probDistA(:, i+1) = probDistA(:, i)'*(A*dPd' +v);
    probDistB(:, i+1) = probDistB(:, i)'*P;
    i = i +1;
end
saveiM = i-1;
%Find the actual rankings by sorting the values and storing the indices in
%order

L = probDistA(:, saveiL);
Lsort = sort(L, 1);
i = 1;
while(i<=n)
    ind = find(L == Lsort(i, 1));
        for j = 0:length(ind)-1
            sortOrderL(j+i) = ind(j+1);
        end
        i = i +j+1;
 end

M = probDistB(:, saveiM);
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
rankL_rankM = [L M]
new_Old = [sortOrderL' sortOrderM']
for i = 1:n
    if sortOrderM(i) ~= sortOrderL(i)
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



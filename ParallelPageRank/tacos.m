clear all
dP = .95; %Random jump probability
tol = 1e-4; %error tol and dP for testing (Lupo said use these)
%Adjacency Matrix Representation of the tree
iterations = 1000
A = [0 1 0 0 0 0; 0 0 1 1 1 0 ; 0 1 0 1 1 0; 0 1 1 0 1 0; 0 1 1 1 0 1;
    0 0 0 0 0 0];
n = 100
A = rand(n, n)>.8;
%A(1, :) = 0;
%A(12, :) = 0;
%A(34, :) = 0;
%A(77, :) = 0;
%A(78, :) = 0;
%A(96, :) = 0;

n = length(A(:, 1)); %number of nodes

for i = 1:n
  if (i == 1)
    A(i, 2) = 1;
  else
    A(i, i-1) = 1;
  end
end

probDistA = zeros(n, 10);
probDistB = zeros(n, 10);

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
                P(i, j) = dP/d(i) + (1-dP)/n;
            else
                P(i, j) = (1-dP)/n;
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
 toAdd = toAdd + sink' * probDistA(:, 1) * dP/n;
 probDistA(:, 2) = P2'*probDistA(:, 1)+toAdd ;
% toAdd = (1-dP)/n*sum(probDistA(:, 2))+sink*dP/n*sum(probDistA(:,2));
i = 2;
%i = 1;
error = 10;
%maybe we find a better way to quantify the difference (error)
%while(i<n+1) 
%toAddA = ((1-dP)/n)*sum(probDistA(:, 1));
%toAdd = toAddA + sum(sink .* probDistA(:, 2)) * dP/n;
%while(norm(probDistA(:, i-1)-probDistA(:, i)) >tol)
while(i < 1000)
%while(i<n+1);
    toAdd = ((1-dP)/n)*sum(probDistA(:, i));
    %toAdd = toAdd + sink' * probDistA(:, i) * dP/n;
    probDistA(:, i+1) = P2'*probDistA(:, i) + toAdd;
    if (sum(probDistA(:, i)) < 0.99)
      fprintf('loosing page rank (%d=%f)\n', i, sum(probDistA(:, i)))
      return
    end
 %  error = abs(probDistA(1, i+1)-probDistA(1, i));
   i = i +1;
end
saveiL = i-1;
%OLD WAY
probDistB(:, 2) = P' * probDistB(:, 1);
i = 2;
while(i < iterations)
%while(abs(norm(probDistB(:, i-1)-probDistB(:, i))) >tol)
    probDistB(:, i+1) = P' * probDistB(:, i);
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
        fprintf('(%d) %f != %f\n', i, L(i), M(i))
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



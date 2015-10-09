for i in {1..9}; do
  wget http://users.csc.calpoly.edu/~dekhtyar/466-Fall2015/labs/lab2/query0$i.txt
done

wget http://users.csc.calpoly.edu/~dekhtyar/466-Fall2015/labs/lab2/query10.txt

for i in {1..5}; do
  wget http://users.csc.calpoly.edu/~dekhtyar/466-Fall2015/labs/lab2/InfoNeed0$i.txt
done

rm *.txt.1

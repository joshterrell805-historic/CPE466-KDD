cd "$( dirname "${BASH_SOURCE[0]}" )"/..

for i in {1..9}; do
  cat data/query0$i.txt | matcher --debug > out.txt
  vim -n out.txt -s data/remove_debug_stuff.vim
  mv out.txt data/queryresults0$i.txt
done
cat data/query10.txt | matcher --debug > out.txt
vim -n out.txt -s data/remove_debug_stuff.vim
 mv out.txt data/queryresults10.txt

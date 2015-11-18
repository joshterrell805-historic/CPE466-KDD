#bin/bash
scp -o StrictHostKeyChecking=no pageRank soc-LiveJournal1.txt mic0:
ssh -o StrictHostKeyChecking=no -t mic0 

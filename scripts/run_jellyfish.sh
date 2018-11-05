cd .. && make
cd bin
./jellyfish count -m 21 -s 10M -t 2 -e 0.9 new_test_sequence.fasta > out.txt
vim out.txt

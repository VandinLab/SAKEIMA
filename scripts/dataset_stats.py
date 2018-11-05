import sys
import math

if len(sys.argv) < 3:
    print "error with input parameters; first is k, second is file."
    exit()

k = int(sys.argv[1])

fin = open(sys.argv[2],'r')

if k < 1:
    print "error with k"
    exit()

numer_of_reads = 0
avg_read_length = 0
max_read_length = 0
min_read_length = 999999
count_dist_in_reads = 0
# key is kmer, value is dict of counts
distincts = dict()

j = 0
for line in fin:
    j = j + 1
    # check if this line is a read or not
    j = (j - 2) % 4
    if j == 0:

        numer_of_reads = numer_of_reads + 1
        max_read_length = max(max_read_length , len(line))
        min_read_length = min(min_read_length , len(line))
        avg_read_length = avg_read_length + len(line)

        if count_dist_in_reads == 1:
            # this line is a read; reset current set of kmers
            kmers = set()
            for i in xrange(len(line)-k):
                kmer = line[i:i+k]
                kmers.add(kmer)
            # add counter for distincts
            if len(kmers) in distincts:
                distincts[len(kmers)] = distincts[len(kmers)] + 1
            else:
                distincts[len(kmers)] = 1

avg_read_length = float(avg_read_length) / float(numer_of_reads)

print "numer_of_reads = "+str(numer_of_reads)
print "max_read_length = "+str(max_read_length)
print "min_read_length = "+str(min_read_length)
print "avg_read_length = "+str(avg_read_length)

if count_dist_in_reads == 0:
    exit()

# compute dbound
distinct_list = list()
for dist in distincts:
    distinct_list.append( (dist , distincts[dist]) )
distinct_list = sorted(distinct_list, key=lambda x: x[0], reverse=True)
print distinct_list
dbound = 0
sum = 0
for dist_ in distinct_list:
    sum = sum + dist_[1]
    a = sum
    b = math.floor(math.log(dist_[0] , 2.0) + 1)
    print "a = "+str(a)
    print "b = "+str(b)
    if a  >= b:
        dbound = b
        break

print "dbound = "+str(dbound)

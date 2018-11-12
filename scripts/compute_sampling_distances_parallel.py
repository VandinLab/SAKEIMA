import math
import os
import numpy as np
import sys
import time

datasets = ['SRS024075','SRS024388','SRS011239','SRS075404','SRS043663','SRS062761']
datasets_size = [8819242497,7924744349,8135441782,7754975225,9156418180,8265706595]
outputfile = "all_results.csv"
jellyfish_path = "../bin/jellyfish"
work_dir_path = "work_dir/"
temp_file_path = "out_sampling_"+str(np.random.randint(100000))+".txt"
k = 31
n = float(10**9)
lambdas = np.linspace(0.1,1.0,10).tolist()
print lambdas
delta = 0.05
threads = 30
runs = 10


def get_result(pattern , path ,  verbose=1):
    fin = open(path,'r')
    for line in fin:
        if pattern in line:
            if verbose == 1:
                print line
            return line[len(pattern):]
    fin.close()

def get_tot_full(numthreads):
    counter = 0.0
    for i in range(numthreads):
        counter = counter + float(get_result(str(i)+" full pass: finished and inserted ",0))
    print "full passes: finished and inserted "+str(counter)
    return counter

def get_tot(numthreads, path):
    counter = 0.0
    for i in range(numthreads):
        counter = counter + float(get_result(str(i)+" sampling pass: finished and inserted ",path,0))
    print "sampling passes: finished and inserted "+str(counter)
    return counter

def get_total_positions(dataset):
    numer_of_positions = 0
    fin = open(dataset , 'r')
    j = 0
    for line in fin:
        j = j + 1
        # check if this line is a read or not
        j = (j - 2) % 4
        if j == 0:
            numer_of_positions = numer_of_positions + len(line) - k
    print "positions of "+dataset+" = "+str(numer_of_positions)
    return numer_of_positions


# compute total number of positions of datasets
#total_positions = dict()
#for dataset in datasets:
#    path_reads = str(dataset)+"/"+str(dataset)+".fastq"
#    total_positions[dataset] = get_total_positions(path_reads)

total_pos = float(datasets_size[0])
for dat in datasets_size:
    total_pos = min(total_pos , float(dat) )

total_positions = dict()
for j in range(len(datasets_size)):
    total_positions[datasets[j]] = float(datasets_size[j])

thetas = []
#for i in range(1,9):
#    thetas.append(float(i)/10.0 * 10**(-8))
for lambd in lambdas:
    sample_size = lambd * total_pos
    m = 100.
    ell = float(sample_size) / m
    epsilon = 1./ell * math.sqrt( 2./m * (math.floor(math.log(2.*ell,2.)) + math.log(1./delta)) )
    theta = epsilon + 2.0 / float(total_pos)
    thetas.append(theta)
#thetas.append(0.0)
print thetas

def run_and_check(list_of_commands , list_of_results):
    to_check = list()
    results = dict()
    running = 0
    while len(list_of_commands) > 0:
        if running < threads:
            next = list_of_commands.pop()
            cmd = next[0]
            dataset = next[1]
            print cmd
            os.system(cmd)
            time.sleep(3)
            running = running + 1
            to_check.append(dataset)
        else:
            time.sleep(10)
            for dataset in to_check[:]:
                time.sleep(10)
                out_path = dataset+"_"+temp_file_path
                try:
                    results_ = list()
                    for pattern in list_of_results:
                        res = float(get_result(pattern , out_path))
                        results_.append(res)
                    results[dataset] = results_
                    to_check.remove(dataset)
                    running = running - 1
                except TypeError:
                    pass
    while len(to_check) > 0:
        time.sleep(10)
        for dataset in to_check[:]:
            time.sleep(10)
            out_path = dataset+"_"+temp_file_path
            try:
                results_ = list()
                for pattern in list_of_results:
                    res = float(get_result(pattern , out_path))
                    results_.append(res)
                results[dataset] = results_
                to_check.remove(dataset)
                running = running - 1
            except TypeError:
                pass
    return results

counting_times = dict()
dumping_times = dict()
memories = dict()


for index , theta in enumerate(thetas):
    to_run = list()
    sample_sizes = dict()
    for dataset in datasets:
        # full counting
        path_counts = work_dir_path+str(dataset)+"_counts_frequentsampling_"+str(k)+".txt"
        path_binary = work_dir_path+str(dataset)+"_frequentsampling_"+str(k)+".mf"
        path_reads = str(dataset)+"/"+str(dataset)+".fastq"
        out_path = dataset+"_"+temp_file_path
        lamb = lambdas[index]
        param = math.exp(-lamb)
        cmd = jellyfish_path+" count -m "+str(k)+" -s 1M -t 1 -j "+str(param)+" -o "+str(path_binary)+" -C "+str(path_reads)+" > "+str(out_path)+" &"
        #print cmd
        to_run.append((cmd , dataset))

    results = run_and_check(to_run , ("Total running time  " , "Writing  " , "Peak Memory (MB):  "))
    for dataset in results:
        counting_times[dataset] = results[dataset][0] + results[dataset][1]
        memories[dataset] = results[dataset][2]
        out_path = dataset+"_"+temp_file_path
        sample_sizes[dataset] = get_tot(1 , out_path)

    to_run = list()
    for dataset in datasets:
        minsupp = max(1 , int(math.ceil(theta * total_positions[dataset])))
        # dump frequent kmers
        path_counts = work_dir_path+str(dataset)+"_counts_frequentsampling_"+str(k)+".txt"
        path_binary = work_dir_path+str(dataset)+"_frequentsampling_"+str(k)+".mf"
        path_reads = str(dataset)+"/"+str(dataset)+".fastq"
        out_path = dataset+"_"+temp_file_path
        tot_ = int(sample_sizes[dataset])
        ell = int(math.floor(float(tot_) / 100.))
        cmd = jellyfish_path+" dump -o "+str(path_counts)+" --bagsell "+str(ell)+" --totalkmers "+str(tot_)+" --theta "+str(theta)+" "+str(path_binary)+" > "+str(out_path)+" &"
        #print cmd
        to_run.append((cmd , dataset))
    patterns = list()
    patterns.append("Running time for dumping  ")
    results = run_and_check(to_run , patterns)
    for dataset in results:
        dumping_times[dataset] = results[dataset][0]
    for i in range(len(datasets)):
        for j in range(i+1 , len(datasets)):
            dataset1 = datasets[i]
            dataset2 = datasets[j]
            print "first dataset "+str(dataset1)
            print "second dataset "+str(dataset2)
            path_counts1 = work_dir_path+str(dataset1)+"_counts_frequentsampling_"+str(k)+".txt"
            path_counts2 = work_dir_path+str(dataset2)+"_counts_frequentsampling_"+str(k)+".txt"
            out_path = dataset1+"_"+dataset2+"_"+temp_file_path

            # compute distances
            cmd = jellyfish_path+" dump --dist "+str(path_counts1)+" "+str(path_counts2)+" > "+str(out_path)+" & "
            to_run.append((cmd , dataset1+"_"+dataset2))
    results = run_and_check(to_run , (" Bray-Curtis distance " , " Whittaker distance " , " Chord distance " , " Jaccard distance " , "Running time for dist  "))
    for dataset in results:
        items = dataset.split("_")
        dataset1 = items[0]
        dataset2 = items[1]
        bcdist = results[dataset][0]
        wdist = results[dataset][1]
        cdist = results[dataset][2]
        jdist = results[dataset][3]
        jdist = results[dataset][3]
        dist_time = results[dataset][4]
        output = str(dataset1)+"_sampling_freq;"+str(dataset2)+"_sampling_freq;"+str(bcdist)+";"
        output = output+str(wdist)+";"+str(cdist)+";"+str(jdist)+";"+str(dist_time)+";"+str(counting_times[dataset1])+";"
        output = output+str(counting_times[dataset2])+";"+str(dumping_times[dataset1])+";"+str(dumping_times[dataset2])+";"
        output = output+str(memories[dataset1])+";"+str(memories[dataset2])+";"+str(theta)+";"+"\n"
        fout = open(outputfile,'a')
        fout.write(output)
        fout.close()

# SAKEIMA
##Sampling Algorithm for K-mers Approximation (Pellegrina, Pizzi, Vandin)
`SAKEIMA` is a sampling-based algorithm for computing an approximation of the most frequent k-mers from a dataset of reads or a sequence. It's implementation is based on Jellyfish (version 2 https://github.com/gmarcais/Jellyfish ).


In order to replicate all experiments, the python script `/scripts/download_ds.py` automatically downloads and prepare the data we used in our experiments. Then, the python scripts `/scripts/compute_exact_distances_parallel.py` and `/scripts/compute_sampling_distances_parallel.py` can be executed to replicate our experiments. Before doing that, you need to compile `SAKEIMA`.

## Compiling SAKEIMA
`SAKEIMA` has the same requirements of Jellyfish. You need `autoconf`, `automake`, `libool`, `gettext`, `pkg-config` and `yaggo`. Then compile using:
```
autoreconf -i
./configure
make -j 4
```

## Counting k-mers from a random sample of the dataset

To execute `SAKEIMA` to count (canonical) k-mers using a random sample of a dataset of reads, you can use the python wrapper `/scripts/run_SAKEIMA.py`. The usage is the following:

```
usage: run_SAKEIMA.py [-h] [-k K] [-db DB] [-o OUTPUT] [-thr THR] [-dt DBTOT]
                      [-t THETA] [-l LAMBD] [-e EPSILON] [-ell ELL] [-d DELTA]
                      [-v VERBOSE]

optional arguments:
  -h, --help            show this help message and exit
  -k K                  length of k-mers (>0)
  -db DB                path to input file (dataset of reads)
  -o OUTPUT, --output OUTPUT
                        path to output file (counts of frequent k-mers)
  -thr THR              Number of threads to use for counting (>0, def. 1)
  -dt DBTOT, --dbtot DBTOT
                        dataset size (>0). Computed if not given
  -t THETA, --theta THETA
                        frequency threshold (in (0,1))
  -l LAMBD, --lambd LAMBD
                        fraction of k-mers to sample (in (0,2))
  -e EPSILON, --epsilon EPSILON
                        approximation accuracy parameter (in (0,1), def. theta + 2/dbtot)
  -ell ELL              size of bags to sample (>0, def. 1/theta - 1)
  -d DELTA, --delta DELTA
                        approximation confidence parameter (in (0,1), def. 0.1)
  -v VERBOSE, --verbose VERBOSE
                        increase output verbosity (def. false)

```
You need to specify the length `-k` of the k-mers and the path `-db` to the dataset (relative to the current folder); then, you need to provide in input the parameter theta using `-t` (`--theta`) or lambda `-l` (`--lambda`). The parameter theta is the frequency threshold for the frequent k-mers, while lambda is the fraction of k-mers to sample form the dataset. You can also fix both parameters. All the others parameters are optional; if not given, the algorithm automatically sets them. As example, you can provide the size (in terms of numer of positions) of k-mers in the dataset using the `-dt` option. If you do not, the algorithm automatically computes it.

The following section describes the basic command for executing `SAKEIMA`.


## Computing ecological distances

To compute ecological distances between two sets of k-mers (and their counts) you can use:
```
jellyfish dump --dist mer_counts1.fa mer_counts2.fa
```
where `mer_counts1.fa` and `mer_counts2.fa` are two files containing the counts of the k-mers obtained from the dataset we want to analyze.


The documentation for computing the exact count of all the k-mers (using Jellyfish) is described in the `/doc/` folder or at https://github.com/gmarcais/Jellyfish .

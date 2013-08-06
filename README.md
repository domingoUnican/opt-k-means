opt-k-means (pure python)
===========

This code finds all possible k-clusters, which are convex, and select
the minimum one with minimal inter cluster function   

NEWS (0.0.4)
===========
- Added one separated file with the implementation of kmean++


NEWS (0.0.3)
===========
- There is only one main program opt-k-means.py, containing a completely
  implementation in python. 
- Minor bugs in the code and some cleaning


NEWS (0.0.2)
===========
- There is a new file called not-so-opt.py, containing a completely
  implementation in python. That is, runing this program works the same
  but it does not contain any reference to .so.
- The implementation of Kmeans in Scipy is not the one in Scipy. The 
  initialization of the centroids is done as described in the kmeans++
  algorithm.

NEWS (0.0.1)
===========
- The program prints only once the inter cluster measure of the
  optimum solution with the inter cluster measure found by k-means
  (implemented in SCIPY)
- The default number of procs is set to 4
- Bookkeping is done in a separate directory
- The minimum cluster is written to a file named 'minimum_cluster'
  with its inter cluster measure
- The kmeans minimum cluster is written to a file named
  'kmeans_cluster' with its inter cluster measure
 

REQUIREMENTS
============
The following libraries are required:

- numpy
- sciPy

Also, because there are some parts of the code that use c code, it is 
necessary a compiler like gcc.

TO INSTALL
==========
First take the file array.c, and issue the following command on the terminal

gcc -O3 -shared -Wl,-soname,array -o arraylib.so -fPIC array.c

TO USE
==========
The script must be run in the terminal, so to see the help just write:

    python opt-k-means -h

The data file name must be a file of float numbers, separated by
commas and in each line, there must be the same number of features.


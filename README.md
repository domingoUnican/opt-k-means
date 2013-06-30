opt-k-means
===========

This code finds all possible k-clusters, which are convex, and select
the minimum one with minimal inter cluster function   

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
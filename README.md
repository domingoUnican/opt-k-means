opt-k-means (based on Avis and Fukuda)
======================================

This code finds all possible k-clusters, which are convex, and select
the minimum one with minimal inter cluster function. This 
method is efficient in the sense that the algorithm find all
clusterings defined by a Voronoi diagram which are not trivial and
without repetition.

NEWS (0.0.1)
============
- Implementation of an abstract class, which represent the algorithm
  of Avis and Fukuda for enumeration
- Cleaning of several parts of the code which are not necessary for
  this version

REQUIREMENTS
============
Sage is required, as the implementation relays on:
- a class called QQ which represents EXACT rational numbers
- a class called Polyhedron which represent general polyhedron in
  general spaces

TO INSTALL
==========

Upload to the Sage server

TO USE
==========
TODO

The data file name must be a file of float numbers, separated by
commas and in each line, there must be the same number of features.


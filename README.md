opt-k-means (based on Avis and Fukuda)
======================================

This code finds all possible k-clusters, which are convex, and select
the minimum one with minimal inter cluster function. This 
method is efficient in the sense that the algorithm find all
clusterings defined by a Voronoi diagram which are not trivial and
without repetition.

NEWS (0.0.2)
============
- Implementation of parallelization in Enumerator (a class implementin
  reverse search)
- First implementation of an arrangement of hyperplanes as a subclass
  of Enumerator (a class implementing reverse_search)
- First implementation of Cluster2, a dummy cluss which finds all
  possible 2- partitions defined by Voronoi diagramm.

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


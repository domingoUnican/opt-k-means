opt-k-means (based on Avis and Fukuda)
======================================

This code finds all possible k-clusters, which are convex, and select
the minimum one with minimal inter cluster function. This 
method is efficient in the sense that the algorithm find all
clusterings defined by a Voronoi diagram which are not trivial and
without repetition.

NEWS (0.0.3)
============
- Implementation of Cluster, a class with outputs all possible
  partitioning in k clusters. This class is a subclass of Enumerator,
  so it is parallelizable  

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

Class Cluster contains everything that you need, it takes as arguments 
a list of points (representing as list of integers), the number of
processors in your computer and other argments relating in which
directory to do bookmarking. 

To generate all partitions, just call the method codes_m_launch()
This is a generator, so it is necessary to iterate over it.

Each partition is coded as a list of k tuples, where each tuple
represent the pertenence of a point to the cluster.
This means tuple t[i] = 1 iff p[i] belong to that cluster.

In order to save space, when k > 2, empty clusters are not given a vector.

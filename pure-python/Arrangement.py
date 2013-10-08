# -*- coding: utf-8 -*-
#Class Arrangement
from Polytope import Polytope
from Enumerator import Enumerator
from itertools import izip
from numpy import array, dot, sign, hstack, infty
K = float

class Arrangement(Enumerator):

    """
    This class  represents an arrangement of hyperplanes
    """

    def __init__(self, points, pointR = [], processes = 1,
                 filename = 'arrange', directory = '/tmp'):
        """
        Constructor, which takes a list of hyperplanes, representing
        by lists of the same length and a initial point pointR.
        This point represents an hyperplane where all the points are
        in the left side. This is a precondition.
        """
        Enumerator.__init__(self, processes, filename, directory)
        self.points = [array(l, dtype = K) for l in points]
        self.pointR = array(pointR)

    def interior_point(self,c):
        """
        Returns an interior point of the cell that have
        the signs given by c, which must be non-empty.
        """
        return Polytope(self.points, c).interiorPoint()

    def f(self, v):
        """
        Returns which elements go before this element
        """
        p = array(self.interior_point(v))
        self.p = p
        if all(p0 == K(0) for p0 in p):
            print "Empty cell!"+str(c)
            return c
        distance = infty
        position, counter = 0, -1
        p1 = hstack([1, self.points[0]])
        best = p1/(-dot(p, p1))
        # print "point", p
        for point, c_counter in izip(self.points, v):
            counter += 1
            p1 = hstack([-1,point])
            dotProduct = -dot(p, p1)
            if dot(p1, self.pointR-p)!=K(0):
                auxDistance = dotProduct/dot(p1, self.pointR-p)
                # print "distance",p1,c_counter
            else:
                auxDistance = infty
            if ((distance > auxDistance and 0 < auxDistance < 1 and
                 c_counter == -1) or
                 (distance==auxDistance and
                  self.order( best , p1/(dotProduct)))
                ):
                position, distance = counter, auxDistance
                best = p1/(dotProduct)
        e=list(v)
        e[position]=1
        return tuple(e)

    def order(self,V,V1):
        """
        This function is returns True if V> V1, where > represents the
        lexicographic order
        """
        for v, v1 in izip(V, V1):
            if v < v1:
                 return True
            elif v> v1:
                return False
        return False

    def Adj(self, v):
        """Search for all hyperplanes that forms the faces of the polytope"""
        l = Polytope(self.points, v).indexes
        for index in  l:
            yield tuple( c_i if index != j else c_i*(-1)
                         for j, c_i in enumerate(v))

if __name__ == '__main__':
    points = [[1,2],[2,3],[3,4],[4,5]]
    pointR = [-6,0,0]
    C = Arrangement(points, pointR)
    for j in C.reverse_search([(1,1,1,1)]):
        print j
    print C.f((-1,-1,1,1))
    print C.p

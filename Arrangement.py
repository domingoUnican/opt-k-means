from Avis_Fukuda_Enumeration import Enumerator
from itertools import izip

#Class Arrangement
class Arrangement(Enumerator):

    """
    This class  represents an arrangement of hyperplanes
    """

    def __init__(self, hyperplanes, pointR = [], processes = 1, filename = 'arrange',
                 directory = '/tmp'):
        """
        Constructor, which takes a list of hyperplanes, representing
        by lists of the same length and a initial point pointR.
        This point can be empty and the class generates it at random.
        """
        Enumerator.__init__(self, processes, filename, directory)
        self.hyperplanes = [[i/gcd(l) for i in l] for l in hyperplanes]
        self.V = VectorSpace(K, len(hyperplanes[0]))
        if pointR:
            self.pointR = self.V(pointR)
        else:
            #Pick a first cell at
            #random, it is represented by a point
            self.pointR=self.firstPoint()

        self.initial_c = tuple( sign(self.V(L).dot_product(self.pointR))
                                for L in self.hyperplanes)
        listAux = []
        for l in self.hyperplanes:
            L=self.V(l)
            listAux.append(L*sign(L.dot_product(self.pointR)))
        self.hyperplanes = listAux

    
    def firstPoint(self):
        """
        This method selects a random point which does not belong in
        any of the hyperplanes
        """
        product=0
        pointR=self.V.random_element()
        while any(self.V(l).dot_product(pointR)==0
                  for l in self.hyperplanes):
            pointR=self.V.random_element()
        return pointR


    def interior_point(self,c):
        """
        Returns an interior point of the cell that have
        the signs given by c, which must be non-empty.
        """
        cell = []
        for c_i, h_i  in izip(c, self.hyperplanes):
            cell.append((c_i * h_i).list())
        p_aux =Polytope(self.V.dimension(),cell).interiorPoint()
        return self.V(p_aux)

    def f(self, v):
        """
        Returns which elements go before this element
        """
        p = self.interior_point(v)
        self.p = p
        if p == self.V(0):
            print "Empty cell!"+str(c)
            return c
        distance=infinity
        position, counter = 0, -1
        betterHyperplane=self.hyperplanes[0]/(-p.dot_product(self.hyperplanes[0]))
        for  hyperplane, c_counter in izip(self.hyperplanes, v):
            counter += 1
            dotProduct = hyperplane.dot_product(-p)
            if hyperplane.dot_product(self.pointR-p)!=0:
                auxDistance = dotProduct/hyperplane.dot_product(self.pointR-p)
            else:
                auxDistance = infinity
            if ((distance > auxDistance and 0 < auxDistance < 1 and
                 c_counter ==-1) or
                 (distance==auxDistance and
                  self.order(betterHyperplane,hyperplane/(dotProduct)))
                ):
                position, distance = counter, auxDistance
                betterHyperplane=hyperplane/(dotProduct)
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
                 return true
            elif v> v1:
                return false
        return false

    def Adj(self, v):
        """Search for all hyperplanes that forms the faces of the polytope"""
        ineq = [(v_i* h_i).list()
                for h_i, v_i in izip(self.hyperplanes, v)]
        l = Polytope(self.V.dimension(),ineq).indexes
        for index in  l:
            yield tuple( c_i if index != j else c_i*(-1)
                    for j, c_i in enumerate(v))

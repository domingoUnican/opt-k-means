# -*- coding: utf-8 -*-

#Class Polytope
from pulp import *
from itertools import izip
K = float

class Polytope:
    """
    New class of polytope. It is suppose that it is
    faster than the polytope class of sage
    """

    def __init__(self, ineq, signs):
        """
        This is the constructor of the class Polytope.
        ineq is a list of inequalities and the signs denote
        the side of the hyperplane the point lies
        """
        self.dimension = len(ineq[0])
        self.length = len(ineq)
        self.ineq = [[K(i) for i in l] for l in ineq ]
        self.indexes = []
        self.signs = signs
        self.indexes = self.necessary()

    def indexes(self):
        """
        This method returns a list with the indexes (with respect to
        the list of all points) of the points which define the cluster
        """
        return self.indexes

    def necessary(self):
        """
        This method returns the indexes of the
        elements which appears as inequalities in the representation
        of the polytope
        """
        signs = self.signs
        ineq = self.ineq
        redundant = set()
        incognitas = LpVariable.dicts("x", range(self.dimension + 1))
        for i in xrange(self.dimension+1):
            incognitas[i].bounds(-1.0,1.0)
        for i in xrange(self.length):
            prob = LpProblem("Min",LpMinimize) if signs[i] > 0 else LpProblem("Max", LpMaximize)
            prob += lpSum([incognitas[k+1]*p for k, p in enumerate(ineq[i])])-incognitas[0], "Objective"
            for j, h in enumerate(izip(ineq, signs)):
                point, s = h
                if i != j and j not in redundant:
                    term = lpSum([incognitas[k + 1]*p for k, p in enumerate(point)])-incognitas[0]
                    if s > 0:
                        prob += term >= 0
                    else:
                        prob += term <= 0
            prob.solve((GLPK(msg=0)))
            if value(prob.objective) == K(0):
                redundant.add(i)
        return [j for j in xrange(self.length) if j not in redundant]
                
    def interiorPoint(self):
        """
        This method calculates an interior point of the polytope
        """
        incognitas =  LpVariable.dicts("x", range(self.dimension + 2))
        incognitas[self.dimension+1].bounds(0.0, 1.0)
        prob = LpProblem("Point", LpMaximize)
        prob += incognitas[self.dimension+1], 'Objective'
        for i in self.indexes:
            point = self.ineq[i]
            s = self.signs[i]
            term = lpSum([incognitas[k+1]*p for k,p in enumerate(point)])
            term -= incognitas[0]
            if s > 0:
                prob += term - incognitas[self.dimension+1] >= 0
            else:
                prob += term + incognitas[self.dimension+1] <= 0
        prob.solve(GLPK(msg=0))
        j = 0
        result = []
        for v in prob.variables():
            while str(j) not in v.name:
                j += 1
                result.append(0.0)
            result.append(v.varValue)
            j += 1
        return result[:-1]

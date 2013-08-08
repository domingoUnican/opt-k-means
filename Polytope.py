#NOTICE, IT IS IMPORTANT THAT THE INEQUALITIES ARE INTEGER NUMBERS!
#I don't know why, but sometimes the inequality is multiplied by a
#constant if the entries are rationals

K = QQ
PREC = 5
from itertools import izip

class Polytope:
    """
    New class of polytope. It is suppose that it is
    faster than the polytope class of sage
    """

    def __init__(self, dimension, ineq):
        """
        This is the constructor of the class Polytope.
        ineq is a list of inequalities and we distinguish between
        the homogenous and inhomogenous inequalities using the
        dimension
        """
        self.dimension = dimension
        self.length = len(ineq[0])
        self.ineq = copy(ineq)
        d = dimension + 1 -self.length
        listTemp = [([K(0)] * (d) + [K(i) for i in l]) for l in ined ]
        print listTemp, "listtemp"
        self.P = Polyhedron(ieqs = listTemp, base_ring = K)
        self.indexes = self.necessary(listTemp)

    def indexes(self):
        """
        This method returns a list with the indexes (with respect to
        the list of all inequalities) of the non redundant inequalities
        """
        return self.indexes

    def necessary(self, ineq):
        """
        This method returns the indexes of the
        elements which appears as inequalities in the representation
        of the polytope
        """
        return [ineq.index(l) for l in self.P.inequalities_list()]

    def interiorPoint(self):
        """
        This method calculates an interior point of the polytope
        """
        if self.P.dim()<self.dimension:
            raise Exception( "dimension of P:" + str(self.P.dim())
                             + "attribute: "+ str(self.dimension))

        problem = MixedIntegerLinearProgram(maximization = True)
        w = problem.new_variable()
        problem.set_objective(w[0])
        problem.set_max(w[0],1)
        for l in self.P.inequality_generator():
            restriction=w[0]
            l_i = (j for j in l)
            restriction=restriction + RDF(l_i.next())
            for i, k in enumerate(l_i):
                restriction -= RDF(k)*w[i + 1]
                problem.set_min(w[i + 1], None)
            problem.add_constraint(restriction<=0)
        valueProblem = problem.solve()
        solution=[]
        long = 0
        for i,v in problem.get_values(w).iteritems():
            solution.append(v)
            long=long+1
        if long<self.dimension:
            raise Exception( "Error! empty polytope")
        return [K(element) for element in solution[1:]]

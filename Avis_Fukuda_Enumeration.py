# coding = utf-8

class Enumerator:
    """
    This class is an abstract class to implement, in the most possible
    general way. The notation follow the one given in the article
    'Reverse search for enumeration' by Avis and Fukuda.
    There is one sutility, though: delta is not necessary for the
    implementation BUT it is necessary to exists.
    """

    def __init__(self, S ):
        """

        S is the set of Solutions
        """
        self.S = S

    def f(self, v):
        """
        This function is the local search function
        Arguments:
        - `self`:
        - `v`: this is the vertex
        """
        pass

    def Adj(self, v):
        """
        This is the adjacency list oracle. It suppose to be a
        generator that returns, one by one, each of the adjacencies of v.
        Arguments:
        - `self`:
        - `v`: denotes the vertex for which we are looking the
               adjacencies
        """
        pass

    def reverse_search(self):
        print "S", self.S
        for s in self.S:
            print "s,",s
            v = s
            do = True #In the original paper there was a do-while
            Adjacencies = self.Adj(v) #I suppose that it is a generator
            while do:
                b_while = True #to avoid the use of delta and j
                while b_while:
                    try:
                        #This is a minor thing, Avis and Fukuda
                        #proposed to use a distinguished element in
                        #the case there were no more adjacencies. In
                        #Python, it is customary to throw an exception
                        #which signals the end of the adjacencies
                        Next = Adjacencies.next()
                        if self.f(Next) == v:
                            v = Next
                            Adjacencies = self.Adj(v)
                            yield v

                    except StopIteration:
                        #no more adjacencies, Avis and Fukuda would
                        #write j>= delta
                        b_while = False
                try:
                    if v == s:
                        #This is a little different because the
                        #implementation this way is simpler, but it is
                        #actually the same thing
                        v = Adjacencies.next()
                        Adjacencies = self.Adj(v)
                    else:
                        u, v = v, self.f(v)
                        different = u != Adjacencies.next()
                        while different:
                            different = u != Adjacencies.next()
                except StopIteration:
                    do = False

#Class to represent general Clustering
from Cluster2 import Cluster2
from itertools import combinations_with_replacement, izip
from Avis_Fukuda_Enumeration import Enumerator

class Cluster(Enumerator):
    """
    This class is a representation of the set of all possible
    clustering of given data
    """

    def __init__(self, points, k, filename = 'k_clusters', processes = 1):
        """
        Constructor
        """
        self.filename = filename
        self.directory = '/tmp'
        ensure_dir(self.directory)
        self.processes = processes
        self.m_file = os.path.join(self.directory, self.filename)
        self.points = copy(points)
        self.d = len(points[0])
        self.n = len(points)

    def find_k_clusters(self):
        """
        This function launch several processes to calculate all
        possible clusters that form part of k-partition
        """
        c2 = Cluster2(points, processes = self.processes)
        all_p = {p for p in c2.codes_m_launch()}
        self.all_clusters = set()
        for s in combinations_with_replacement(all_p, self.k -2):
            temp = tuple(all((i>0 for i in l) for l in izip(*s)))
            for s1 in all_p:
                self.all_clusters.add( tuple(all((i > 0 for i in l))
                                  for l in izip(s1,temp)))

    def generate_dicts(self):
        """
        Private function, that it is used to generate the neighbours
        of a clusters, that is:
        Given a set S and a set of sets T, return the sets S1 such
        that S1 contains S and another point OR S contains S and
        another point
        """
        self.find_k_clusters()
        remove, add = dict(), dict()
        for cluster in self.all_clusters:
            list_c = list(cluster)
            add_point, remove_point = set([]), set([])
            for i in xrange(self.n):
                t = list_c[i]
                c = 1 if t == 0 else 0
                list_c[i] = c
                if tuple(list_c) in self.all_clusters:
                    if t == 0:
                        add_point.add(i)
                    else:
                        remove_point.add(i)
                list_c[i] = t
            add[cluster] = add_point
            remove[cluster] = remove_point
        self.add = add
        self.remove = remove

    def codes(self):
        """
        This is a generator, which returns all possible partitions
        into k clusterings
        """
        if self.k > 2:
            self.generate_dicts()
            for l in self.reverse_search():
                yield l
        else:
            c2 = Cluster2(points, processes = self.processes)
            for l in c2.codes():
                yield l

    def f(self, v):
        '''
        This comes from the article of Avis and Fukuda to enumerate
        using a local search.
        This function is a local search, f is an algorithm wich
        applied several times to the same node it gives the trivial
        partition, i. e. all the points belong to the same cluster.

        f recieves a partition (represented by a list of tuples
        ordered) a return another partition defined by a Voronoi
        diagram where one of the points of the cluster with less
        points has been put in the cluster with more points
        '''
        i = len(v) - 1
        j = i
        if i == 0:
            #TODO: Understand why I need this
            return v
        u = [list(t) for t in v]
        B = True
        while B :
            j -= 1
            a, r = self.add[tuple(u[j])], self.remove[tuple(u[i])]
            intersection = a.intersection(r)
            if intersection:
                B  = False
            elif j  ==  0 :
                i -= 1
                j = i
        pos = min(intersection)
        u[j][pos], u[i][pos] = 1, 0
        if not any(u[i]):
            del u[i]
        result = [tuple(t) for t in u]
        result.sort(key = sum, reverse = True)
        return result

    def Adj(self, v):
        '''
        This function returns a list of all the adjacents of a
        partition. We say that a partition is adjacent to another iff
        they are only different in one point
        '''
        u = [list(t) for t in v]
        result = [tuple(t) for t in u]
        length = len(u)
        if length < k :
            for t in u:
                for r in self.remove[tuple(t)]:
                    result.remove(tuple(t))
                    t[r] = 0
                    temp = [0]*self.dimY
                    temp[r] = 1
                    result.append(tuple(temp))
                    result.append(tuple(t))
                    result.sort(key = sum, reverse = True)
                    yield result
                    result.remove(tuple(t))
                    result.remove(tuple(temp))
                    t[r] = 1
                    result.append(tuple(t))
        if length > 1:
            for t0, t1 in itertools.combinations(u, 2):
                inter = self.remove[tuple(t0)]
                inter = inter.intersection(self.add[tuple(t1)])
                for r in inter:
                    result.remove(tuple(t0))
                    result.remove(tuple(t1))
                    t0[r] = 0
                    t1[r] = 1
                    if any(t0):
                        result.append(tuple(t0))
                    if any(t1):
                        result.append(tuple(t1))
                    result.sort(key = sum, reverse = True)
                    yield result
                    if any(t0):
                        result.remove(tuple(t0))
                    if any(t1):
                        result.remove(tuple(t1))
                    t0[r] = 1
                    t1[r] = 0
                    result.append(tuple(t0))
                    result.append(tuple(t1))
                # TODO: Eliminate the duplicate code
                inter = self.add[tuple(t0)]
                inter = inter.intersection(self.remove[tuple(t1)])
                for r in inter:
                    result.remove(tuple(t0))
                    result.remove(tuple(t1))
                    t0[r] = 1
                    t1[r] = 0
                    if any(t0):
                        result.append(tuple(t0))
                    if any(t1):
                        result.append(tuple(t1))
                    result.sort(key = sum, reverse = True)
                    yield result
                    if any(t0):
                        result.remove(tuple(t0))
                    if any(t1):
                        result.remove(tuple(t1))
                    t0[r] = 0
                    t1[r] = 1
                    result.append(tuple(t0))
                    result.append(tuple(t1))

    def codes_m_launch(self):
        """
        Method that launchs several processes to generate all possible
        partitions into k clusters.
        """
        if self.k > 2:
            self.generate_dicts()
            for l in self.reverse_search():
                yield l
        else:
            c2 = Cluster2(points, processes = self.processes)
            for l in c2.codes_m_launch():
                yield l

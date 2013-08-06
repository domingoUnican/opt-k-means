#!/opt/local/bin/python2.7

from argparse import ArgumentParser
import warnings # TODO: search for the warning
import pickle
import scipy.linalg
import numpy
import itertools
import os, copy, sys
from numpy import random
from scipy import linalg, matrix, array, sum, compress, transpose
from scipy.cluster.vq import vq, kmeans, kmeans2
import time
import multiprocessing
import ctypes
from multiprocessing import Process
from numpy import float64 as float
from itertools import izip, product
from enumeration import alternate, enumerate_list

MESSAGE = "for %d clusters the intercluster measure is \
 OPTIMUM: %.2f "

def combinations_with_replacement(iterable, r):
    '''
    Copy and paste of the generator that returns the different
    combinations with replacement of a set of elements given as an
    iterable. This function can be found in the official docs.
    '''
    pool = tuple(iterable)
    n = len(pool)
    if not n and r:
        return
    indices = [0] * r
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != n - 1:
                break
        else:
            return
        indices[i:] = [indices[i] + 1] * (r - i)
        yield tuple(pool[i] for i in indices)

def null(A1, eps=1e-19):
    '''
    Returns the kernel of matrix A1. Implementation taken from
    http://stackoverflow.com/questions/5889142/
    '''
    rows, columns = A1.shape
    if (rows < columns):
        A = numpy.vstack([A1, [[0] * columns for i in
                               xrange(columns - rows)]])
    else:
        A = A1
    u, s, vh = scipy.linalg.svd(A)
    null_mask = (s <= eps)
    null_space = scipy.compress(null_mask, vh, axis=0)
    return scipy.transpose(null_space)


def signGet(p, p1, h, lu):
    '''
    This function checks in which side of the hyperplane h*x=0
    lies point p.
    If it is on one side, it returns 1 or -1. If it is in the
    hyperplane, then returns  all possible signs.
    '''
    d = p.shape[1]
    if numpy.all(p == p1):
        return tuple(numpy.sign(signs[0]) for signs in
                     product([ float(1), float(0), float(-1)],
                             repeat = d))
    p_temp = p-p1
    sol = scipy.linalg.lu_solve(lu,p_temp.T)
    if abs((p_temp*h)[0,0])>1e-19:
        return numpy.sign((p_temp*h)[0,0])
    result = []
    for signs in itertools.product([float(1),float(0),float(-1)],repeat=d):
        signs_1 = [signs[0]]+[signs[0]-e for e in signs[1:]]
        v = numpy.matrix(signs_1)
        temp = (v*sol)[0,0]+signs[0]
        result.append(numpy.sign(temp))
    return tuple(result)

def support_f(support):
    """
    This function takes as input a list  and returns one point
    and a matrix with maximum rank. Appending the point and the
    rows of the matrix gives exactly the support.
    Arguments:
    - `support`: this is the list of points
    """
    d = len(support)
    for i in xrange(d):
        p = support[i]
        support_vectors = [l for j,l in enumerate(support) if not i==j]
        list_linear = [[e[0]-e[1] for e in zip(p,q)]
                       for q in support_vectors]
        p1 = numpy.matrix(p, dtype=float)
        matrix_linear = numpy.matrix(list_linear)
        if (numpy.linalg.matrix_rank(matrix_linear)==d-1):
            h = null(matrix_linear)
            temp = numpy.matrix(h.T.tolist()+list_linear)
            lu = scipy.linalg.lu_factor(temp.T)
            yield p1,h,lu


def split(partition):
    '''
    partitions are given in a special format, just for the sake of
    speed. Indeed, partition represent several partitions at one
    time.
    partition is a list where at each position has a sign or a list of
    signs. V. g. if the list is (0,(1,0),(1,0)), then the real
    partitions are (0,1,1) and (0,0,0). Notice that we are taking the
    elements in the same position in both list.
    Now, we transform each partition in something more
    manageable.
    '''
    size=1
    for element in partition:
        if isinstance(element,tuple):
            size = max(size,len(element))
    for i in xrange(size):
        positive, negative = [], []

        for element in partition:
            if isinstance(element,tuple):
                b = element[i] > 0
            else:
                b = element > 0
            positive.append( int(b))
            negative.append(int (not b))
        yield tuple(positive)
        yield tuple(negative)


def intra_cluster(cluster):
    '''
    return the intra cluster measure of a cluster.
    '''
    if not cluster:
        return float(0)
    centroid = array([numpy.sum(cluster,axis=0)/float(len(cluster))])
    m = numpy.matrix(cluster)
    return numpy.sum(vq(m,centroid)[1])

def ensure_dir(d):
    '''
    creates a directory if it does not exists
    '''
    if not os.path.exists(d):
        os.makedirs(d)




class dataset:

    def __init__(self, dimX, dimY, filename='', processes=1):
        '''
        Constructor of the class, only stores the data
        '''
        #We just instantiate a shared matrix for all the processes
        #Data and combinations should be shared to avoid replication
        #between processes ~ time and memory overhead.
        #This first approach is not very optimal,
        #combinations may be generated in parallel for each
        #process. TODO
        self.directory = 'temp'
        ensure_dir(self.directory)
        self.nombre = os.path.join(self.directory,'part_')
        self.nombre_clusters = os.path.join(self.directory,
                                            'clusters_')
        self.m_file = os.path.join(self.directory,
                                   'minimum_cluster_')
        self.i_file = os.path.join(self.directory,
                                   'kmeans_cluster_')

        self.dimY = dimY #dimY is the number of rows of the matrix
        self.dimX=dimX #dimX is the number of columns of the matrix
        self.processes = processes
        shared_array_base = multiprocessing.Array(ctypes.c_double, dimX*dimY)
        shared_array = numpy.ctypeslib.as_array(shared_array_base.get_obj())
        shared_array = shared_array.reshape(dimY, dimX)
        self.data = shared_array
        if not filename:
            numpy.random.seed(10)
            for j in xrange(dimY):
                for i in xrange(dimX):
                    self.data[j][i]=numpy.random.randn()
        else:
            with open(filename,'r') as f:
                data = [[float(n) for n in row.split(',')] for row in
                        f.readlines()[:dimY]]
                for j in xrange(dimY):
                    for i in xrange(dimX):
                        self.data[j][i]=data[j][i]



    def inter_cluster(self,clusters):
        '''
        return the inter cluster measure of a partition.
        clusters is a list of indicator functions, e. g.
        clusters[i] is a vector of 0 and 1's such that if
        self.data[j] in C_i iff clusters[i][j] == 1.
        To save just a litte of memory, the length of clusters is
        going to be k-1. The points in C_{k-1} are the points that are
        not in any of the other clusters. It is nice to notice that
        the mass centers are important, the intra_cluster measure
        depends heavily in the intra_cluster measure and it is not
        difficult to find examples, where the intracluster measure is
        smaller taking "fake" centroids.
        '''

        partition = []
        dist = float(0)
        for cluster in clusters:
            part = []
            for p, i in izip (self.data, cluster):
                if i>0:
                    part.append(p)
            dist += intra_cluster(part)
        part = []
        for d in izip(self.data,*clusters):
            if not any(i>0 for i in d[1:]):
                part.append(d[0])
        dist += intra_cluster(part)
        return dist/self.dimY


    def find_optimum_two_launch(self):
        '''
        This function launch several processes to calculate the
        optimum partition of a set in two clusters
        '''
        p_list=[]
        for i in xrange(self.processes):
            p_list.append(Process(target=self.find_optimum_two,
                                  args = (i,)))
        [p.start() for p in p_list]
        [p.join() for p in p_list]

    def find_optimum_two(self, pid ):
        '''
        This function find the minimum when the data is split into two
        different clusters
        '''
        min_dist = numpy.infty
        min_par = []
        d=self.dimX
        total_proc = self.processes
        #parallelize across half of the combinations
        all_p1 = set([])
        alternate_gen = alternate(enumerate_list(self.data,
                                                 self.dimX),
                                  period=total_proc,
                                  phase=pid)
	for supportVectors in alternate_gen:
            for p1, h, lu in support_f(supportVectors):
                partition=tuple(signGet(numpy.matrix(p,dtype=float),p1,h,lu)
                                for p in self.data)
                for partition1 in split(partition):
                    all_p1.add(partition1)
                    new_dist = self.inter_cluster([partition1])
                    if min_dist>new_dist:
                        min_dist = new_dist
                        min_par = partition1
        m_file = self.m_file + str(pid)
        with open(m_file,'w') as f:
            pickle.dump(min_dist, f)
            pickle.dump(min_par, f)
        nombre_fichero = self.nombre+str(pid)
        with open(nombre_fichero,'w') as f:
            pickle.dump(all_p1,f)

    def cluster_k_launch(self, k):
        '''
        This function launch several processes to calculate all possible clusters
        that form part of k-partition
        '''
        all_p = set()
        for i in xrange(self.processes):
            f = open(self.nombre+str(i),'r')
            all_p |= pickle.load(f)
            f.close()
            #remove the files after reading from them to prevent strange errors
            os.remove(self.nombre+str(i))
        dimX = len(all_p)
        shared_array_base = multiprocessing.Array(ctypes.c_int,
                                                  self.dimY*dimX)
        shared_array = numpy.ctypeslib.as_array(shared_array_base.get_obj())
        shared_array = shared_array.reshape(dimX,self.dimY)
        self.k2 = shared_array
        for i, p in enumerate(all_p):
            for j, r in enumerate(p):
                self.k2[i][j] = 1 if r > 0 else 0
        p_list = []
        for i in xrange(self.processes):
            p_list.append(Process(target = self.cluster_k,
                                  args = (i, k) ))
        [p.start() for p in p_list]
        [p.join() for p in p_list]

    def cluster_k(self, pid, k):
        '''
        This function saves to a file all the possible clusters in
        a file. This is necessary to find all possible partitions
        '''
        d=self.dimX
        all_clusters=set()
        total_proc = self.processes
        #parallelize across half of the combinations
        mySlice = len(self.k2)/total_proc
        final=((pid+1)==total_proc) and ((len(self.k2)%total_proc)>0)
        myLines=self.k2[pid*mySlice:((pid+1)*mySlice + (final))]
        out_file = open(self.nombre_clusters+str(pid),"w")
        cont = 0
        for l1 in myLines:
            for l in itertools.combinations_with_replacement(self.k2,k-2):
                temp = tuple(all((i > 0 for i in l))
                                 for l in izip(l1,*l))
                all_clusters.add(temp)
        pickle.dump(all_clusters, out_file)
        out_file.close()


    def find_general_optimum_launch(self, k):
        '''
        This function launch several processes
        to calculate all possible clusters
        that form part of k-partition
        '''
        all_clusters = set()
        for i in xrange(self.processes):
            f = open(self.nombre_clusters+str(i),'r')
            all_clusters |= pickle.load(f)
            f.close()
        remove, add = dict(), dict()
        for cluster in all_clusters:
            list_c = list(cluster)
            add_point, remove_point = set([]), set([])
            for i in xrange(self.dimY):
                t = list_c[i]
                c = 1 if t == 0 else 0
                list_c[i] = c
                if tuple(list_c) in all_clusters:
                    if t == 0:
                        add_point.add(i)
                    else:
                        remove_point.add(i)
                list_c[i] = t
            add[cluster] = add_point
            remove[cluster] = remove_point
        self.add = add
        self.remove = remove
        state = list([tuple([1] * self.dimY)])
        min_dist = self.inter_cluster(state)
        several_states = [state]
        while len(several_states) < self.processes:
            new_states = []
            for s in several_states:
                for v in self.Adj(s,k):
                    if self.f(v) == s:
                        new_states.append(list(v))
                        min_temp = self.inter_cluster(v)
                        min_dist = min(min_temp, min_dist)
                several_states = new_states
        length = len(several_states)
        proc = self.processes
        p_list = []
        pid = 0
        for state in several_states:
            p_list.append(Process(
                target = self.reverse_search,
                args = (state, k, min_dist, pid)))
            pid += 1
        for i in xrange(length/proc):
            temp, p_list = p_list[:proc], p_list[proc:]
            [p.start() for p in temp]
            [p.join() for p in temp]
        [p.start() for p in p_list]
        [p.join() for p in p_list]

    def f(self, v):
        '''
        This comes from the article of Avis and Fukuda to enumerate
        using a local search.
        This function is a local search, f is an algorithm wich
        applied several times to the same node it gives the clustering
        where the first one
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


    def Adj(self, v, k):
        '''
        This comes from the article of Avis and Fukuda to enumerate
        using a local search.
        This function returns a list of all the adjacents of an
        node
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


    def reverse_search(self, point, k, minimum, pid):
        do = True
        v = point
        Adja = self.Adj(v, k)
        min_dist = min ( minimum, self.inter_cluster(v))
        min_par = []
        while do :
            b_while = True
            while b_while:
                try:
                    Next = Adja.next()
                    if self.f(Next) == v:
                        v = Next
                        Adja = self.Adj(v, k)
                        dist = self.inter_cluster(v)
                        if dist < min_dist:
                            min_dist = dist
                            min_par = tuple(tuple(temp)
                                       for temp in v)
                except StopIteration:
                    b_while = False
            if point == v:
                try:
                    v  = Adja.next()
                    Adja = self.Adj(v, k)
                except StopIteration:
                    do = False
            else:
                u, v = v, self.f(v)
                Adja = self.Adj(v, k)
                different = u != Adja.next()
                while different:
                    different = u != Adja.next()

        m_file = self.m_file + str(pid)
        with open(m_file,'w') as f:
            pickle.dump(min_dist, f)
            pickle.dump(min_par, f)


def testMode():
    points=[i for i in range(4,30)]
    dims=[i for i in range(2,3)]
    clusters = [3]
    numpy.seterr(all='raise')
    for dim in dims:
        for point in points:
            for k in clusters:
                d=dataset(dim,point,'linux.txt',processes = 2)
                t1=time.time()
                d.find_optimum_two_launch()
                if k > 2:
                    d.cluster_k_launch(k)
                    d.find_general_optimum_launch(k)
                opttime=time.time()
                print point,opttime-t1
if __name__=='__main__':
    dppoint = 2
    points = 10
    filen="linux.txt"
    nproc = 4
    k=2
    d_s = 'Calculate the optimum k-means centroids for a given dataset'
    parser = ArgumentParser(description=d_s)
    parser.add_argument('-f','--file', help='Filename of dataset,\
    the default name is "linux.txt"', required=False)
    parser.add_argument('-d','--dim',
                        help='number of features in the dataset,\
    2 are used by default', required=False)
    parser.add_argument('-n','--points',
                        help='number of lines in the dataset,\
    more files in the dataset are not considered, the default is 10',
                        required=False)
    parser.add_argument('-p','--procs',
                        help='number of processes to be used,\
    4 are used by default', required=False)
    parser.add_argument('-k','--clusters',
                        help='number of clusters,\
    2 are used by default', required=False)
    parser.add_argument('-b','--benchmark',
                        help='run a simple benchmark',
                        required=False)
    args = vars(parser.parse_args())
    if args['benchmark']:
        testMode()
        exit()
    if args['file']:
        filen=args['file']
    if args['dim']:
        dppoint=int(args['dim'])
    if args['points']:
        points=int(args['points'])
    if args['procs']:
        nproc=int(args['procs'])
    if args['clusters']:
        k=int(args['clusters'])

    numpy.seterr(all='raise')
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        d=dataset(dppoint,points,filen,processes = nproc)
    t1=time.time()
    print d.data
    d.find_optimum_two_launch()
    min_dist = numpy.infty
    min_par = []
    if k > 2:
        d.cluster_k_launch(k)
        d.find_general_optimum_launch(k)
        # we search the minimum now
    for directory, subdir, files in os.walk(d.directory):
        fil_min = [os.path.join(d.directory,name) for name in files
                   if d.m_file in os.path.join(d.directory,name)]
    for m_file in fil_min:
        with open(m_file) as f:
            dist = pickle.load(f)
            par = pickle.load(f)
            if dist < min_dist:
                min_dist = dist
                min_par  = par

    list_par = []
    print "min_par", min_par
    if k > 2:
        for i in izip(*min_par):
            list_par.append( i.index(1))
    print MESSAGE %(k, min_dist)
    print d.data
    with open(d.m_file[:-1],'w') as f:
        f.write(str(min_dist))
        f.write('\n')
        f.write(str(list(list_par)))
    print "time: %.2f" %(time.time()-t1,)

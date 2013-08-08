#Class Enumerator
import pickle, os
from multiprocessing import Process

def ensure_dir(d):
    '''
    creates a directory if it does not exists
    '''
    if not os.path.exists(d):
        os.makedirs(d)


class Enumerator:
    """
    This class is an abstract class to implement, in the most possible
    general way. The notation follow the one given in the article
    'Reverse search for enumeration' by Avis and Fukuda.
    There is one sutility, though: delta is not necessary for the
    implementation BUT it is necessary to exists.
    """

    def __init__(self, processes = 1, filename = 'enumeration',
                 directory = '/tmp' ):
        """
        Constructor
        processes is the number of
        processes which our enumerator will launch, filename and
        directory are used for bookmarking
        """
        self.filename = filename
        self.directory = directory
        self.m_file = os.path.join(self.directory, 
                                   self.filename)
        self.processes = processes
        ensure_dir(self.directory)


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

    def reverse_m_pid(self, S, pid):
        """
        This is an auxiliary method, it shouldn't be called from
        another programmed (indeed, it should be private)
        """
        m_file = self.m_file + str(pid)
        results = {l for l in self.reverse_search(S)}
        with open(m_file,'w') as f:
            pickle.dump(results, f)

    def reverse_m(self, S):
        """
        This is the wrapper to make things go parallel. This functions
        greates as many processes as needed where each of the
        processes operates in the different branches of the
        algorithm. All the clustering is written to the hard disk and
        then given back to the user as a generator.
        """
        several_elements = S
        while len(several_elements) <= self.processes:
            for element in several_elements:
                yield element
            new_elements = []
            for s in several_elements:
                for v in self.Adj(s):
                    if self.f(v) == s:
                        new_elements.append(v)
            several_elements = new_elements
        length = len(several_elements)
        proc = self.processes
        p_list = []
        pid = 0
        for element in several_elements:
            p_list.append( Process(
                target = self.reverse_m_pid,
                args = (set([element]), pid)
                ))
            pid += 1
        for i in xrange(length/proc):
            temp, p_list = p_list[:proc], p_list[proc:]
            [p.start() for p in temp]
            [p.join() for p in temp]
        t1 =[p.start() for p in p_list]
        t2 = [p.join() for p in p_list]
        for i in xrange(pid):
            m_file = self.m_file + str(i)
            with open(m_file) as f:
                for l in pickle.load(f):
                    yield l
            

    def reverse_search(self, S):
        """
        This is the main algorithm, which is a generator
        function. This means that outputs all the elements without
        keeping them in memory.
        """
        for s in S:
            yield s
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
                        Adjacencies = self.Adj(v)
                        different = u != Adjacencies.next()
                        while different:
                            different = u != Adjacencies.next()
                except StopIteration:
                    do = False

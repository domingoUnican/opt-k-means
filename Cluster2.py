#Class for generating all possible voronoi clusters when the number of
#clusters is two
from Arrangement import Arrangement
K = QQ


class Cluster2:
    """
    This class is a generator, which gives all possible clustering defined by a voronoi
    region using a tuple t, where t[i] == 1 iff p[i] belongs to cluster 1.
    """

    def __init__(self, points, filename = '2_clusters', processes = 1):
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

    def codes(self):
        """
        This is a generator, which returns all possible clusters
        codified as a tuple t satisfying:
        t[i] == 1 iff points[i] belong to cluster 1
        """

        bound = max(max(self.points))
        points_aux = [[1] + [ 2 * i for i in l]
                      for l in self.points]
        pointR = [bound] + [0] * self.d
        ar = Arrangement(points_aux, pointR, filename = self.filename) 
        for l in ar.reverse_search({tuple([1]*len(self.points))}):
            yield l


    def codes_m_launch(self):
        '''
        Function that launchs several processes to generate all
        possible two clusters. It is needed writing to disc first in
        as many separated files as processes all possible two clusterings 
        '''
        bound = max(max(self.points))
        points_aux = [[1] + [ 2 * i for i in l]
                      for l in self.points]
        pointR = [bound] + [0] * self.d
        ar =  Arrangement(points_aux, pointR, processes = self.processes)
        for l in ar.reverse_m({tuple([1]*len(self.points))}):
            yield l

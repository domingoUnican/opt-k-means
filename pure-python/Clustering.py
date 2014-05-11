#!/opt/local/bin/python2.7
# -*- coding: utf-8 -*-
#Class Arrangement
import csv, os, time, pickle
from copy import copy
from Arrangement import Arrangement
from Enumerator import ensure_dir
from argparse import ArgumentParser
from Tree import genera_arboles

K = float


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
        self.points = [[ K(i) for i in l] for l in points]
        self.d = len(points[0])

    def codes(self):
        """
        This is a generator, which returns all possible clusters
        codified as a tuple t satisfying:
        t[i] == 1 iff points[i] belong to cluster 1
        """

        bound = max(max(self.points))
        points_aux = [[ K(i) for i in l] for l in self.points]
        pointR = [-K(bound)] + [0] * self.d
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
        points_aux = [[ K(i) for i in l] for l in self.points]
        pointR = [-K(bound)] + [0] * self.d
        ar =  Arrangement(points_aux, pointR, processes = self.processes)
        for l in ar.reverse_m({tuple([1]*len(self.points))}):
            yield l


if __name__=='__main__':
    dppoint=2
    points=3
    filen="linux.txt"
    nproc=2
    d_s = 'Calculate the optimum k-means centroids for a given dataset'
    parser = ArgumentParser(description=d_s)
    parser.add_argument('-f','--file', help='Filename of dataset,\
    the default name is "linux.txt" is used', required=False)
    parser.add_argument('-d','--dim',
                        help='number of features in the dataset,\
    2 are used by default', required=False)
    parser.add_argument('-n','--points',
                        help='number of lines in the dataset,\
    more files in the dataset are not considered, the default is 10',
                        required=False)
    parser.add_argument('-p','--procs',
                        help='number of processes to be used,\
    12 are used by default', required=False)
    args = vars(parser.parse_args())
    if args['file']:
        filen = args['file']
    if args['dim']:
        dppoint = int(args['dim'])
    if args['points']:
        points = int(args['points'])
    if args['procs']:
        nproc = int(args['procs'])
    with open(filen) as csvfile:
        lector = csv.reader(csvfile, delimiter = ',')
        filas = list(lector)
        data = [row[:dppoint] for row in filas[:points]]
    d = Cluster2(data,processes = nproc)
    signos = tuple(j for j in d.codes_m_launch())
    with open('output','w') as f:
        for arbol in genera_arboles(signos):
            arbol.rename()
            f.write(arbol.to_string())
            f.write('\n')

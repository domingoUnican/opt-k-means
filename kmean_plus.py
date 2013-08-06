from scipy import linalg, matrix, array, sum, compress, transpose
from scipy.linalg import norm
from scipy.cluster.vq import vq, kmeans, kmeans2

def kmeans_plus(data, k, itera =1000):
    """
    Naive implementation of kmeans++.  This algorithm finds k random
    centroids, taken under a special distribution. Then, normal kmeans
    is applied. This is repeated a
    sufficient number of times and take the centroids corresponding to
    the minimum intercluster measure
    Arguments:
    - `data`: The data, it is necessary to be a scipy matrix
    - `k`: Number of clusters
    - `itera`: Number of iterations to be applied the algorithm
    """
    min_dist = numpy.infty
    min_centroids = None
    min_code = None
    for i in xrange(itera):
        centroids = generate_centroids(data, k)
        kmeans_centroids, kmeans_code = kmeans2(data,
                                               centroids,
                                               minit = 'matrix')
        kmeans_dist = numpy.sum(vq(d.data,kmeans_centroids)[1])
        if kmeans_dist < min_dist:
            min_dist = kmeans_dist
            min_centroids = kmeans_centroids
            min_code = kmeans_code
    return min_centroids, min_dist, min_code

from scipy import linalg, matrix, array, sum, compress, transpose
from scipy.linalg import norm
from scipy.cluster.vq import vq, kmeans, kmeans2

def generate_centroids(data, k):
    """
    generate k centroids for the  points in l
    """
    llen = data.shape[0]
    result = [ data[random.randint(0,llen-1)]]
    for i in xrange(k-1):
        probabilities=[min([norm(element-centroid)
                            for centroid in result])**2
                            for element in data]
        totalSum= sum(probabilities)
        rvalue = random.uniform(0,totalSum)
        total_sum = 0
        position = -1
        while(position <= llen and total_sum <= rvalue):
            total_sum += probabilities[0]
            probabilities = probabilities[1:]
            position += 1
        result.append(data[position])
    return matrix(result)


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

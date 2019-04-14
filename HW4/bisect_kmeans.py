import kmeans
import clusters as utils

choice_dist = utils.pearson
clusternum = 8


def bisekt(clusters, vectors, distance=utils.euclidean, k=4):
    if len(clusters) == k:
        return clusters

    my_sse = None
    indi_clus = None
    for i in range(len(clusters)):
        cluster = clusters[i]
        score = 0

        centroid = kmeans.get_centroid(cluster, vectors)

        for country in cluster:
            score += pow(distance(vectors[country], centroid), 2)

        if my_sse is None or score > my_sse:
            my_sse = score
            indi_clus = i

    indi_orig = []
    for index in clusters[indi_clus]:
        indi_orig.append(index)

    newclus = utils.kcluster([vectors[index] for index in clusters.pop(indi_clus)], distance=distance, k=2)
    for cluster in newclus:
        for i in range(len(cluster)):
            cluster[i] = indi_orig[cluster[i]]

    return bisekt(clusters + newclus, vectors, distance = distance, k=clusternum)


def main(nameof_file):
    (countries, vectors) = kmeans.readfile(nameof_file)

    clusters = bisekt([list(range(len(vectors)))], vectors, distance=choice_dist, k=clusternum)
    chckd_clust = []
    for i in range(clusternum):
        if len(clusters[i]) == 0:
            continue

        chckd_clust.append(clusters[i])
        print('cluster {}:'.format(i + 1))
        print([countries[r] for r in clusters[i]])

    print("SSE: " + str(kmeans.sse(chckd_clust, vectors)))


if __name__ == "__main__":
    main("C:/Users/akars/clustering_lab/HW4/Preprocess.py")
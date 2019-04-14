import kmeans
import clusters as utils

choice_dist = utils.cosine
clusternum = 6

def get(cluster, ids):
    if cluster.id < 0:
        if cluster.left is not None:
            get(cluster.left, ids)
    if cluster.right is not None:
        get(cluster.right, ids)
    else :
        ids.append(cluster.id)

def main(nameof_file):
    (countries, vectors) = kmeans.readfile(nameof_file)
    clusters = utils.hcluster(vectors, distance = choice_dist)
    utils.drawdendrogram(clusters, list(map(lambda x: x[1], countries)), jpeg = "C:/Users/akars/clustering_lab/processedhierarchical.jpg")

    opt_clust = [clusters.left, clusters.right.left, clusters.right.right.left.left,
    clusters.right.right.left.right.left, clusters.right.right.left.right.right,
    clusters.right.right.right.right, clusters.right.right.right.left
]

    cluster_level = []
    for cluster in opt_clust:
     country_ids = []
    get(cluster, country_ids)
    cluster_level.append(country_ids)

    for i in range(clusternum):
        print('cluster {}:'.format(i + 1))
        print([countries[r]
        for r in cluster_level[i]
])
    print("SSE: " + str(kmeans.sse(cluster_level, vectors)))

    if __name__ == "__main__":
        main("C:/Users/akars/clustering_lab/processed/preprocessed.csv")
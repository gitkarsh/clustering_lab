import wordcloud
import clusters as utils
import word_cloud

my_rng = range(2, 8)
clusternum = 8
choice_dist = utils.cosine


def readfile(nameof_file):
    countries = []
    vectors = []

    my_data = open(nameof_file)

    for line in my_data:
        arr = line.rstrip().split(',')

        countries.append((arr[0], arr[1]))
        vectors.append([int(arr[i]) for i in my_rng])

    my_data.close()
    return countries, vectors


def postdo(final_clust, postfile):
    output = open(postfile, "w")
    output.write("[['Country', 'Value'],\n")

    for i in range(len(final_clust)):
        cluster = final_clust[i]

        for country in cluster:
            output.write("['" + country + "', " + str(i) + "],\n")  # Manually fix the end

    output.close()


def country_centr(cluster, vectors):
    centroid = [0 for i in range(len(vectors[0]))]

    for index in cluster:
        for i in range(len(vectors[0])):
            centroid[i] += vectors[index][i]

    centroid = [round(centroid[i]/len(cluster)) for i in range(len(centroid))]
    return centroid


def make_clust(clusters, values):
    f = open("C:/Users/akars/clustering_lab/HW4/dimensions_keywords.csv - dimensions_keywords.csv.csv")
    lines = f.read().split('\n')
    k = []
    for i in range(len(lines)):
        if i == 0:
            continue
        k.append(lines[i].split(',')[1:])
    for j in range(len(clusters)):
        cluster = clusters[j]
        word = []
        centroid = country_centr(cluster, values)
        for i in range(len(centroid)):
            if centroid[i] > 50:
                label = 0
            else:
                label = 1
            word += k[i][label].split(' ')
        d = {}
        for w in word:
            if w in d:
                d[w] += 1
            else:
                d[w] = 1
        word_counts = [(w, count/20) for w, count in d.items()]
        word_cloud.create_cloud("{}.png".format(str(j)), word_counts)


def sse(clusters, vectors):
    score = 0

    for cluster in clusters:
        centroid = country_centr(cluster, vectors)

        for country in cluster:
            score += pow(choice_dist(vectors[country], centroid), 2)

    return score


def main(nameof_file, output_f):
    (countries, vectors) = readfile(nameof_file)
    print(countries)
    print(vectors)

    clusters = utils.kcluster(vectors, distance=choice_dist, k = clusternum)
    chcked_clustr = []
    final_clustr = []
    for i in range(clusternum):
        if len(clusters[i]) == 0:
            continue

        chcked_clustr.append(clusters[i])
        print('cluster {}:'.format(i + 1))
        print([countries[r] for r in clusters[i]])
        final_clustr.append([countries[r][1] for r in clusters[i]])

    print("SSE: " + str(sse(chcked_clustr, vectors)))
    postdo(final_clustr, output_f)
    make_clust(clusters, vectors)



if __name__ == "__main__":
    main("C:/Users/akars/clustering_lab/processed/preprocessed.csv", "C:/Users/akars/clustering_lab/processed/finalk_clusters.json")
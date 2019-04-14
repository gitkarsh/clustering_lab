import wordcloud
import clusters as utils

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


def create_clouds(clusters, vectors):
    #will create using keywords
    keyword_file = open("C:/Users/akars/clustering_lab/HW4/dimensions_keywords.csv - dimensions_keywords.csv.csv")
    lines = keyword_file.read().split('\n')
    keywords = []
    for i in range(len(lines)):
        if i == 0:
            continue
        keywords.append(lines[i].split(',')[1:])

    for j in range(len(clusters)):
        cluster = clusters[j]
        words = []
        centroid = country_centr(cluster, vectors)

        for i in range(len(centroid)):
            if centroid[i] > 50:
                label = 0
            else:
                label = 1

            words += keywords[i][label].split(' ')

        my_arr = {}
        for x in words:
            if x in my_arr:
                my_arr[x] += 1
            else:
                my_arr[x] = 1

        numword = [(w, count/20) for w, count in my_arr.items()]
        wordcloud.WordCloud("clouds/{}.png".format(str(j)), numword)


def country_centr(cluster, vectors):
    centroid = [0 for i in range(len(vectors[0]))]

    for index in cluster:
        for i in range(len(vectors[0])):
            centroid[i] += vectors[index][i]

    centroid = [round(centroid[i]/len(cluster)) for i in range(len(centroid))]
    return centroid


def sse(clusters, vectors):
    score = 0

    for cluster in clusters:
        centroid = country_centr(cluster, vectors)

        for country in cluster:
            score += pow(choice_dist(vectors[country], centroid), 2)

    return score


def main(input_f, output_f):
    (countries, vectors) = readfile(input_f)
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
    create_clouds(clusters, vectors)


if __name__ == "__main__":
    main("C:/Users/akars/clustering_lab/processed/preprocessed.csv", "C:/Users/akars/clustering_lab/processed/finalk_clusters.json")
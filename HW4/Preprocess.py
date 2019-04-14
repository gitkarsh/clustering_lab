import csv
import clusters

new_collect = []
my_indi = range(2, 8)
empty = []

def readfile(nameof_file):
    my_data = open(nameof_file)

    my_count = -2
    for line in my_data:
        my_count += 1
        if my_count == -1:  # Skip headers
            continue

        arr = line.rstrip().split(',')
        if '' in arr:
            empty.append(my_count)
        new_collect.append(arr)
    my_data.close()


def procfile(new_file):
    output = open(new_file, "w")

    for line in new_collect:
        for i in range(len(line)):
            output.write(line[i] + ('\n' if i == (len(line) - 1) else ','))

    output.close()

def chk_near(country, beseen):
    similarities = []
    listcountry = [int(country[i]) for i in beseen]

    for i in range(len(new_collect)):
        if '' in new_collect[i]:
            continue

        list_see = [int(new_collect[i][j]) for j in beseen]
        similarities = sorted(similarities + [(clusters.pearson(listcountry, list_see), i)])[:3]

    return [new_collect[i] for i in map(lambda x: x[1], similarities)]

#filling using averages(method 2)
def fill(country):
    available = list(my_indi)
    country_missing = []

    for index in my_indi:
        if country[index] == '':
            available.remove(index)
            country_missing.append(index)

    similar_countries = chk_near(country, available)

    for index in country_missing:
        country[index] = str(round(sum(map(lambda x: int(x[index]), similar_countries))/3))

def main(nameof_file, new_file):
    readfile(nameof_file)

    for index in empty:
        fill(new_collect[index])

    procfile(new_file)

if __name__ == "__main__":
    main("C:/Users/akars/clustering_lab/processed/dataset.csv", "C:/Users/akars/clustering_lab/processed/preprocessed.csv")

    for l in new_collect:
        print(l)



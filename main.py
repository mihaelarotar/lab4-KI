import random
from node import Node
import sys
import numpy as np
import matplotlib.pyplot as plt


def random_100():
    list_nodes = []

    for i in range(100):
        x = random.randrange(0, 100)
        y = random.randrange(0, 100)
        node = Node(i, x, y)
        list_nodes.append(node)

    return list_nodes


def euclidean_distance(node1, node2):
    p1 = np.array((node1.get_x(), node1.get_y()))
    p2 = np.array((node2.get_x(), node2.get_y()))

    return round(np.linalg.norm(p1 - p2))  # fara round?


def swap(obj1, obj2):
    aux = obj1
    obj1 = obj2
    obj2 = aux
    return obj1, obj2


def random_numbers():
    number1 = random.randint(0, 99)
    number2 = random.randint(0, 99)

    return number1, number2


def vertauschende_mutation(cities):
    aux_cities = cities.copy()

    number1, number2 = random_numbers()
    while number1 == number2:
        number1, number2 = random_numbers()

    if number1 > number2:
        number1, number2 = swap(number1, number2)

    for j in range(number1, number2 + 1):
        aux_cities[number1 + number2 - j] = cities[j]

    return aux_cities


def kanten_rekombinationen(parent1, parent2):
    adjacency_list = {}

    length = 100
    # vecini p1
    for index, val in enumerate(parent1):  # i ia indice base ia val
        adjacency_list[val] = {parent1[index - 1], parent1[(index + 1) % length]}

    # vecini p2
    for index, val in enumerate(parent2):
        adjacency_list[val].add(parent2[index - 1])
        adjacency_list[val].add(parent2[(index + 1) % length])

    choose = random.randint(1, 2)

    if choose == 1:
        nod = parent1[0]
    else:
        nod = parent2[0]

    final_list = [nod]

    while len(final_list) < 100:
        neighbours = adjacency_list[nod].copy()
        del adjacency_list[nod]
        for key in adjacency_list:
            if nod in adjacency_list[key]:
                adjacency_list[key].remove(nod)

        # verificam ce nod sa luam dupa
        if len(neighbours) == 0:
            nod_nou = random.choice(list(adjacency_list))
            final_list.append(nod_nou)
            nod = nod_nou

        else:
            minimum = 5
            min_list = []
            for i in neighbours:
                list_length = len(adjacency_list[i])

                if list_length < minimum:
                    minimum = list_length

            for i in neighbours:
                list_length = len(adjacency_list[i])
                if list_length == minimum:
                    min_list.append(i)

            nod_nou = random.choice(min_list)
            final_list.append(nod_nou)
            # print(nod_nou)
            nod = nod_nou

    return final_list


def plot_anfang_punkte(liste_punkte):
    for punkt in liste_punkte:
        plt.plot(punkt.get_x(), punkt.get_y(), color='black', linestyle='solid', linewidth=2,
                 marker='o', markerfacecolor='blue', markersize=8)
    plt.show()


def fitness_function(list_nodes):
    distance = 0
    list_length = len(list_nodes)
    node_inceput = list_nodes[0]
    nod_sfarsit = list_nodes[list_length - 1]
    node1 = list_nodes[0]

    i = 1
    while i < list_length:
        node2 = list_nodes[i]
        distance = distance + euclidean_distance(node1, node2)
        node1 = node2
        i = i + 1

    distance = distance + euclidean_distance(node_inceput, nod_sfarsit)
    return distance


def plot_generation(generation, best_route):
    fig, ax = plt.subplots()
    for previous, current in zip(best_route, best_route[1:]):
        ax.plot([previous.get_x(), current.get_x()], [previous.get_y(), current.get_y()], 'g', linestyle="--")
    ax.plot([best_route[-1].get_x(), best_route[0].get_x()], [best_route[-1].get_y(), best_route[0].get_y()],
            'g', linestyle="--")
    ax.set_title(generation)
    plt.show()


def travelling_salesman_problem(parents):
    generation = 0

    best_distance = sys.maxsize
    best_route = []

    best_distance_global = sys.maxsize
    best_route_global = []

    dict_parents = []
    for parent in parents:
        dict_parents.append((parent, fitness_function(parent)))
        if fitness_function(parent) < best_distance:
            best_distance = fitness_function(parent)
            best_route = parent

    best_distances = [best_distance]

    print("----------------" + str(generation) + "--------------------")
    # plot la best pe segment
    plot_generation(generation, best_route)
    print("Best Distance: " + str(best_distance))

    generation += 1

    while generation <= 2000:
        children = []
        for i in range(40):
            parent1 = random.choice(list(zip(*dict_parents))[0])
            nr = random.random()
            # print("----------------" + str(generation) + "--------------------")
            if nr < 0.3:
                parent2 = random.choice(list(zip(*dict_parents))[0])
                parent1 = kanten_rekombinationen(parent1, parent2)
            child = vertauschende_mutation(parent1)
            children.append(child)

        dict_children = []
        for child in children:
            dict_children.append((child, fitness_function(child)))
            if fitness_function(child) < best_distance:
                best_distance = fitness_function(child)
                best_route = child

        if generation in (500, 1000, 1500, 2000):
            print("----------------" + str(generation) + "--------------------")
            # plot la best pe segment
            plot_generation(generation, best_route)
            print("Best Distance: " + str(best_distance))

        best_distances.append(best_distance)

        if best_distance < best_distance_global:
            best_distance_global = best_distance
            best_route_global = best_route
        best_distance = sys.maxsize
        best_route = []

        # schimb parintii pt urmatoarea generatie
        dict_parents.extend(dict_children)
        dict_parents = sorted(dict_parents, key=lambda elem: elem[1])[:10]
        generation = generation + 1

    # plot la grafic
    generations = [i for i in range(2001)]
    plt.plot(generations, best_distances, color='green', linewidth=3)
    plt.xlabel('Generations')
    plt.ylabel('Distances')
    plt.title('Graph')
    plt.show()

    return best_distance_global, best_route_global


if __name__ == '__main__':
    points = random_100()

    plot_anfang_punkte(points)

    perm_list = []

    for r in range(10):
        temp = points.copy()
        random.shuffle(temp)
        perm_list.append(temp)

    dist, route = travelling_salesman_problem(perm_list)
    print("Best distance global: " + str(dist))

    plot_generation("Best", route)

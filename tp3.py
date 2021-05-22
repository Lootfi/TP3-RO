from math import floor
from collections import namedtuple
import uuid
from fractions import Fraction
# comment this out if you don't wish to see the branching graph
from graphviz import Digraph


Item = namedtuple(
    "Item", ['index', 'value', 'weight'])

Nodes = []  # list of total nodes, only used for the final plotting


class Noeud:
    def __init__(self, level, value, weight, bound, contains, objets, my_id, parent_id):
        self.level = level
        self.value = value
        self.weight = weight
        self.bound = bound
        self.contains = contains
        self.objets = objets
        self.parent_id = parent_id
        self.my_id = my_id


"""
    params:
u: noeud
k: capacité maximale
n: nombre d'objets
v: liste des utilités
w: liste des poids
"""


def borne_maximale_pour_noeud(u, k, n, v, w):
    if u.weight > k:
        return 0, False
    else:
        borne_max = u.value
        wt = u.weight
        j = u.level
        while j < n and wt + w[j] <= k:
            borne_max += v[j]
            wt += w[j]
            u.objets[j] = str(1)
            j += 1

        # remplir le sac à dos avec une fraction de w[j]
        if j < n:
            # une fraction d'utilité
            borne_max += (k - wt) * float(v[j]) / w[j]
            u.objets[j] = str(Fraction((k - wt) / w[j]))  # just for the graphe
        # returning the upper bound and the isRelaxed(0/1)
        return borne_max


def knapsack(items, capacity):
    Nodes = []

    item_count = len(items)

    v = [0]*item_count  # list of values
    w = [0]*item_count  # list of weights

    # sort items by ci/pi
    items = sorted(items, key=lambda k: float(k.value)/k.weight, reverse=True)

    # add ordered values and weights to v,w
    for i, item in enumerate(items, 0):
        v[i] = int(item.value)
        w[i] = int(item.weight)

    # init a queue
    q = []

    # init a root node
    root = Noeud(0, 0, 0, 0.0, [], [0]*item_count, uuid.uuid1(), None)
    root.bound = borne_maximale_pour_noeud(
        root, capacity, item_count, v, w)

    q.append(root)

    Zmin = 0  # utilité
    taken = [0]*item_count
    best = set()

    while q != []:
        c = q.pop(0)
        Nodes.append(c)
        if c.bound > Zmin:
            level = c.level+1

        # check 'left' node (if item is added to knapsack)
        left = Noeud(level, c.value + v[level-1],
                     c.weight + w[level-1], 0.0, c.contains[:], [0]*item_count, uuid.uuid1(), c.my_id)
        left.bound = borne_maximale_pour_noeud(
            left, capacity, item_count, v, w)

        left.contains.append(level)

        if left.weight <= capacity:
            if left.value > Zmin:
                Zmin = left.value
                best = set(left.contains)
            if left.bound > Zmin:
                q.append(left)
        # check 'right' node (if items is not added to knapsack)
        right = Noeud(level, c.value, c.weight, 0.0,
                      c.contains[:], [0]*item_count, uuid.uuid1(), c.my_id)
        right.bound = borne_maximale_pour_noeud(
            right, capacity, item_count, v, w)
        if right.weight <= capacity:
            if right.value > Zmin:
                Zmin = right.value
                best = set(right.contains)
            if right.bound > Zmin:
                q.append(right)
    for b in best:
        taken[b-1] = 1
    Zmin = sum([i*j for (i, j) in zip(v, taken)])
    return str(Zmin), Nodes


def graph_it(N):
    dot = Digraph(comment="L'arbre de séparation")
    for node in N:
        dot.node(str(node.my_id), str(node.bound))
        if node.parent_id:
            text = "(("
            for i, x in enumerate(node.objets, 1):
                if node.objets[i-1] != 0 and i != len(node.objets):
                    text += str(node.objets[i-1]) + " x" + str(i) + " + "
                if node.objets[i-1] != 0:
                    text += str(node.objets[i-1]) + " x" + str(i)
            text += "))"
            dot.edge(str(node.parent_id), str(node.my_id), text)
    dot.render(filename='separation.gv',
               directory='output', view=True, format='svg')  # svg,png,pdf ..etc
    return 0


if __name__ == "__main__":
    # td2 exo5
    # Nodes = []
    # W = 50
    # arr = [Item(1, 70, 31),
    #         Item(2, 20, 10),
    #         Item(3, 39, 20),
    #         Item(4, 35, 18),
    #         Item(5, 7, 4),
    #         Item(6, 5, 3),
    #         Item(7, 9, 6)]
    # Z, N = knapsack(arr, W)
    # print("td2 exo5: ", Z)

    # td2 exo7
    Nodes = []
    W = 14
    arr = [Item(1, 20000, 4),
           Item(2, 18000, 6),
           Item(3, 32000, 8),
           Item(4, 45000, 10),
           Item(5, 6000, 1)]
    Z, N = knapsack(arr, W)
    print("td2 exo7: ", Z)

    graph_it(N)

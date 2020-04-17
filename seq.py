from itertools import permutations


def get_order(dim, edges, numbers):
    out = ""
    for e in edges:
        if numbers[e[0]] > numbers[e[1]]:
            out += "0"
        else:
            out += "1"
    return out


def generate_hyperoctahedral_group(dim, edges, done=[]):
    elements = []
    for p in permutations(range(2**dim)):
        ren_edges = [tuple(p[j] for j in i) for i in edges]
        for i, j in ren_edges:
            if (min(i, j), max(i, j)) not in edges:
                break
        else:
            elements.append(p)
    return elements


def references(dim):
    # generate the edges of a dim-dimensional cube
    edges = []
    if dim >= 1:
        edges = [(0, 1)]
    for d in range(1, dim):
        e = [i for i in edges]
        e2 = [tuple(j + 2**d for j in i) for i in edges]
        e3 = [(i, i+2**d) for i in range(2**d)]
        edges = e + e2 + e3

    # generate the hyperoctahedral group
    transforms = generate_hyperoctahedral_group(dim, edges)

    # Try all numberings of vertices
    orients = []
    torients = []
    for n in permutations(range(2**dim)):
        o = get_order(dim, edges, n)
        if o not in torients:
            torients.append(o)
        for p in transforms:
            if get_order(dim, edges, [p[i] for i in n]) in orients:
                break
        else:
            orients.append(o)
    return len(orients), len(torients)


for i in range(5):
    print(references(i))

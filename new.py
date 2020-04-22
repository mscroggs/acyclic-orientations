from itertools import combinations

def has_cycles(edges, orient):
    vertices = 0
    for o, e in zip(orient, edges):
        vertices = max(vertices, e[0]+1, e[1]+1)
    for i in range(vertices):
        after = [i]
        p = 0
        while p != len(after):
            p = len(after)
            for o, e in zip(orient, edges):
                if o and e[0] in after:
                    if e[1] == i:
                        return True
                    if e[1] not in after:
                        after.append(e[1])
                if not o and e[1] in after:
                    if e[0] == i:
                        return True
                    if e[0] not in after:
                        after.append(e[0])
    return False


def generate_hyperoctahedral_group(vcount, edges, done=[]):
    if len(done) == vcount:
        return [done]
    elements = []
    for i in range(vcount):
        if i not in done:
            numbers = done + [i]
            for e in edges:
                if max(e) < len(numbers):
                    vertices = [numbers[e[0]], numbers[e[1]]]
                    new_e = (min(vertices), max(vertices))
                    if new_e not in edges:
                        break
            else:
                elements += generate_hyperoctahedral_group(vcount, edges, numbers)
    return elements


def generate_edge_maps(transform, edges):
    """Generates the effect of each permutation on the edges."""
    out = []
    for t in transform:
        new_t = []
        for e in edges:
            new_e = (t[e[0]], t[e[1]])
            if new_e in edges:
                new_t.append((edges.index(new_e), True))
            else:
                new_t.append((edges.index((new_e[1], new_e[0])), False))
        out.append(new_t)
    return out


def unique_acyclic_permutations(edges, edge_t, printing=False, done=[]):
    for d, e in zip(done, edges):
        if e[0] == 0 and not d:
            return 0
            # Edges from 0 at the start of the list must be oriented True
            # as otherwise a larger number can be found by rotating
        if e[0] != 0:
            break
    if len(done) == len(edges):
        o = "".join(["1" if i else "0" for i in done])
        for p in edge_t:
            o2 = "".join(["1" if j == done[i] else "0" for i, j in p])
            if o2 > o:
                return 0
        if printing:
            print(o)
        return 1

    out = 0
    for i in [True, False]:
        if not has_cycles(edges, done + [i]):
            out += unique_acyclic_permutations(edges, edge_t, printing,
                                               done + [i])
    return out


def calculate_term(n, printing=False):
    if n < 3:
        return None

    edges = [(0,n-1), (n,2*n-1)]
    for i in range(n-1):
        edges.append((i, i+1))
        edges.append((i+n, i+1+n))
    for i in range(n):
        edges.append((i, i+n))

    faces = [tuple(range(n)), tuple(range(n,2*n))]
    for i in range(n):
        faces.append((i, (i+1)%n, i+n, (i+1)%n + n))

    print(edges)
    # generate the hyperoctahedral group
    transforms = generate_hyperoctahedral_group(2*n, edges)

    # Remake edges adding in diagonals on faces
    edges = []
    for e in faces:
        for i in combinations(e, 2):
            i = (min(i), max(i))
            if i not in edges:
                edges.append(i)
    edges.sort()

    print(edges)

    edge_transforms = generate_edge_maps(transforms, edges)

    return unique_acyclic_permutations(edges, edge_transforms, printing)


with open("b3343--.txt", "w") as f:
    pass

for n in range(5):
    a_n = calculate_term(n, True==0)
    with open("b3343--.txt", "a") as f:
        f.write(str(n) + " " + str(a_n) + "\n")
    print(n, a_n)

from itertools import product


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


def generate_hyperoctahedral_group(dim, edges, done=[]):
    """Generates all the permutations of the dim-dimensional cube."""
    if len(done) == 2**dim:
        return [done]
    elements = []
    for i in range(2**dim):
        if i not in done:
            numbers = done + [i]
            for e in edges:
                if max(e) < len(numbers):
                    vertices = [numbers[e[0]], numbers[e[1]]]
                    new_e = (min(vertices), max(vertices))
                    if new_e not in edges:
                        break
            else:
                elements += generate_hyperoctahedral_group(dim, edges, numbers)
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


def calculate_term(dim, printing=False):
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
    edge_transforms = generate_edge_maps(transforms, edges)

    return unique_acyclic_permutations(edges, edge_transforms, printing)

    # Try all numberings of vertices
    orients = []
    edge_count = dim * 2 ** (dim-1)
    assert len(edges) == edge_count
    for n in product([True, False], repeat=edge_count):
        if not has_cycles(edges, n):
            o = "".join(["1" if i else "0" for i in n])
            for p in edge_transforms:
                o2 = "".join(["1" if j == n[i] else "0" for i, j in p])
                if o2 in orients:
                    break
            else:
                orients.append(o)
                if printing:
                    print(o, len(orients))
    return len(orients)


# Test the code
print("Testing calculate_term(1)")
assert calculate_term(1, True) == 1
print("PASS")

print("Testing calculate_term(2)")
assert calculate_term(2) == 3
print("PASS")

print("Testing calculate_term(2)")
assert calculate_term(3) == 54
print("PASS")
# End testing

with open("b334248.txt", "w") as f:
    pass

for n in range(1, 5):
    a_n = calculate_term(n, True)
    with open("b334248.txt", "a") as f:
        f.write(str(n) + " " + str(a_n) + "\n")
    print(n, a_n)

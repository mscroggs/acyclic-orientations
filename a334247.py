# TODO: change this to evaluate chromatic polynomials at -1


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


def acyclic_permutations(edges, done=[]):
    if len(done) == len(edges):
        return 1
    out = 0
    for i in [True, False]:
        if not has_cycles(edges, done + [i]):
            out += acyclic_permutations(edges, done + [i])
    return out


def calculate_term(dim):
    # generate the edges of a dim-dimensional cube
    edges = []
    if dim >= 1:
        edges = [(0, 1)]
    for d in range(1, dim):
        e = [i for i in edges]
        e2 = [tuple(j + 2**d for j in i) for i in edges]
        e3 = [(i, i+2**d) for i in range(2**d)]
        edges = e + e2 + e3

    return acyclic_permutations(edges)


# Test known terms of sequence
assert has_cycles([(0, 1), (2, 3), (0, 2), (1, 3)], [True, False, False, True])
assert calculate_term(1) == 2
assert calculate_term(2) == 14
assert calculate_term(3) == 1862
# End test

with open("b334247.txt", "w") as f:
    pass

for n in range(1, 4):
    a_n = calculate_term(n)
    with open("b334247.txt", "a") as f:
        f.write(str(n) + " " + str(a_n) + "\n")
    print(n, a_n)

from itertools import product, permutations


def has_cycles(dim, orient, edges):
    for i in range(2**dim):
        after = [i]
        p = 0
        while p != len(after):
            p = len(after)
            for (a,b), d in zip(edges, orient):
                if d and a in after:
                    if b == i:
                        return True
                    if b not in after:
                        after.append(b)
                if not d and b in after:
                    if a == i:
                        return True
                    if a not in after:
                        after.append(a)
    return False


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

    # Try all numberings of vertices
    edge_count = dim * 2 ** (dim-1)
    assert len(edges) == edge_count
    count = 0
    for n in product([True, False], repeat=edge_count):
        if not has_cycles(dim, n, edges):
            count += 1
    return count


# Test known terms of sequence
assert calculate_term(1) == 2
assert calculate_term(2) == 14
assert calculate_term(3) == 1862

for i in range(1,8):
    print(i, calculate_term(i))


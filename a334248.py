from itertools import product, permutations


def get_order(dim, edges, numbers):
    out = ""
    for e in edges:
        if numbers[e[0]] > numbers[e[1]]:
            out += "0"
        else:
            out += "1"
    return out


def has_cycles(dim, orient, edges):
    for i in range(2**dim):
        after = [i]
        p = 0
        while p != len(after):
            p = len(after)
            for (a, b), d in zip(edges, orient):
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

    # Try all numberings of vertices
    orients = []
    edge_count = dim * 2 ** (dim-1)
    assert len(edges) == edge_count
    for n in product([True, False], repeat=edge_count):
        if not has_cycles(dim, n, edges):
            o = "".join(["1" if i else "0" for i in n])
            for p in edge_transforms:
                o2 = "".join(["1" if j == n[i] else "0" for i, j in p])
                if o2 > o:
                    break
                if o2 in orients:
                    break
            else:
                orients.append(o)
                if printing:
                    print(o, len(orients))
    return len(orients)


def calculate_term_old(dim, printing=False):
    """This is slower than the above version, and is only used for testing."""
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
    for n in permutations(range(2**dim)):
        o = get_order(dim, edges, n)
        for p in transforms:
            o2 = get_order(dim, edges, [n[i] for i in p])
            if o2 > o:
                break
            if o2 in orients:
                break
        else:
            orients.append(o)
            if printing:
                print(o, len(orients))
    return len(orients)


# Test the code
data = {}
for i in range(1, 4):
    data[i] = {"new": calculate_term(i),
               "old": calculate_term_old(i)}

print("Testing calculate_term(1)")
assert data[1]["new"] == 1
print("PASS")

print("Testing calculate_term(2)")
assert data[2]["new"] == 3
print("PASS")

for i in range(1, 4):
    print("Testing calculate_term(" + str(i) + ")"
          " == calculate_term_old(" + str(i) + ")")
    assert data[i]["new"] == data[i]["old"]
    assert data[i]["new"] == data[i]["old"]
    print("PASS")
# End testing

with open("b334248.txt", "w") as f:
    pass

for n in range(1, 5):
    a_n = calculate_term(n, True)
    with open("b334248.txt", "a") as f:
        f.write(str(n) + " " + str(a_n) + "\n")
    print(n, a_n)

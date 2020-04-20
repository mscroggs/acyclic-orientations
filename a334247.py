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


def generate_hyperoctahedral_group(dim, edges, done=[]):
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

def references(dim, printing=False):
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
    torients = []
    edge_count = dim * 2 ** (dim-1)
    assert len(edges) == edge_count
    for n in product([True, False], repeat=edge_count):
        if not has_cycles(dim, n, edges):
            o = "".join(["1" if i else "0" for i in n])
            if o not in torients:
                torients.append(o)
            for p in edge_transforms:
                o2 = "".join(["1" if j == n[i] else "0" for i,j in p])
                if o2 in orients:
                    break
            else:
                orients.append(o)
                if printing:
                    print(o, len(orients))
    return len(orients), len(torients)


def treferences(dim, printing=False):
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
    torients = []
    edge_count = dim * 2 ** (dim-1)
    assert len(edges) == edge_count
    count = 0
    for n in product([True, False], repeat=edge_count):
        if not has_cycles(dim, n, edges):
            count += 1
    return count


def references_old(dim, printing=False):
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
            if printing:
                print(n, len(orients))
    return len(orients), len(torients)


for i in range(1,8):
    print(i, treferences(i))

# Test the code
data = {}
for i in range(1,4):
    data[i] = {"new":references(i),
               "old":references_old(i)}

print("Testing references(1)")
assert data[1]["new"][0] == 1
print("PASS")

print("Testing references(2)")
assert data[2]["new"][0] == 3
print("PASS")

print("Testing references(3)")
assert data[3]["new"][1] == 1862
print("PASS")

for i in range(1,4):
    print("Testing references("+str(i)+") == references_old("+str(i)+")")
    assert data[i]["new"][0] == data[1]["old"][0]
    assert data[i]["new"][1] == data[1]["old"][1]
    print("PASS")

with open("s1", "w") as f:
    pass
with open("s2", "w") as f:
    pass

for i in range(1,5):
    a,b = references(i, True)
    with open("s1", "a") as f:
        f.write(str(a)+"\n")
    with open("s2", "a") as f:
        f.write(str(b)+"\n")


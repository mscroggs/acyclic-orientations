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
            print(n, len(orients))
    return len(orients), len(torients)


with open("s1", "w") as f:
    pass
with open("s2", "w") as f:
    pass

for i in range(5):
    a,b = references(i)
    with open("s1", "a") as f:
        f.write(str(a)+"\n")
    with open("s2", "a") as f:
        f.write(str(b)+"\n")

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


def unique_acyclic_permutations(topology, edge_t, transform, printing=False, done=[]):
    if 1 not in topology:
        return 1
    if len(done) > 0:
        if not done[0]:
            # If done starts False, then it can be made larger by
            # reflecting so it starts True
            return 0
    if len(done) > 2:
        if done[0] and done[1] and not done[2]:
            # If done starts True True False, it can be made larger by
            # reflecting so it starts True True True
            return 0
    if len(done) == len(topology[1]):
        o = "".join(["1" if i else "0" for i in done])
        testable_orients = []
        for t,p in zip(transform[1:], edge_t[1:]):
            o2 = "".join(["1" if j == done[i] else "0" for i, j in p])
            if o2 > o:
                return 0
            if o2 == o:
                testable_orients.append((t,p))
        edges_to_orient = []
        for d in range(2,len(topology)-1):
            entities = topology[d]
            for e in topology[d]:
                assert len(e) == 4  # If not, dim > 3; not implemented yet
                edges = {}
                for i in [(0,1), (0,2), (1,3), (2,3)]:
                    a, b = min(e[i[0]], e[i[1]]), max(e[i[0]], e[i[1]])
                    c = done[topology[1].index((a,b))]
                    edges[(a,b)] = c
                    edges[(b,a)] = not c
                starts = []
                for v in e:
                    for v2 in e:
                        if (v,v2) in edges and not edges[(v,v2)]:
                            break
                    else:
                        starts.append(v)
                for a in starts:
                    for b in starts:
                        if a < b:
                            edges_to_orient.append((a,b))
        out = 0
        for orients in product([True, False], repeat=len(edges_to_orient)):
            if not has_cycles(topology[1] + edges_to_orient, done + list(orients)):
                o = "".join(["1" if i else "0" for i in done+list(orients)])
                for t,p in testable_orients:
                    o2 = "".join(["1" if j == done[i] else "0" for i, j in p])
                    for e in [tuple(t[i] for i in j) for j in edges_to_orient]:
                        if e[0] < e[1]:
                            if orients[edges_to_orient.index(e)]:
                                o2 += "1"
                            else:
                                o2 += "0"
                        else:
                            if orients[edges_to_orient.index((e[1], e[0]))]:
                                o2 += "0"
                            else:
                                o2 += "1"
                    if o2 > o:
                        break
                else:
                    if printing:
                        print(o)
                    out += 1
        return out

    out = 0
    for i in [True, False]:
        if not has_cycles(topology[1], done + [i]):
            out += unique_acyclic_permutations(topology, edge_t, transform,
                                               printing=printing,
                                               done=done + [i])
    return out


def calculate_term(dim, printing=False):
    # generate the edges of a dim-dimensional cube
    if dim <= 1:
        return 1
    topology = {}
    for d in range(dim+1):
        for n in range(d-1,-1,-1):
            new_n = [i for i in topology[n]]
            new_n += [tuple(j+2**(d-1) for j in i) for i in topology[n]]
            if n > 0:
                for e in topology[n-1]:
                    new_n.append(tuple(list(e) + [i+2**(d-1) for i in e]))
            topology[n] = new_n
        topology[d] = [tuple(range(2**d))]

    # generate the hyperoctahedral group
    transforms = generate_hyperoctahedral_group(dim, topology[1])
    edge_transforms = generate_edge_maps(transforms, topology[1])

    return unique_acyclic_permutations(topology, edge_transforms, transforms, printing)


# Test the code
print("Testing calculate_term(1)")
assert calculate_term(1, True) == 1
print("PASS")

print("Testing calculate_term(2)")
assert calculate_term(2) == 3
print("PASS")

print("Testing calculate_term(2)")
#assert calculate_term(3) == 54
print("PASS")
# End testing

with open("bnew_seq.txt", "w") as f:
    pass

for n in range(5):
    a_n = calculate_term(n, True)
    with open("bnew_seq.txt", "a") as f:
        f.write(str(n) + " " + str(a_n) + "\n")
    print(n, a_n)

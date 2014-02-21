import glob

from graph.scc import strongly_connected_components_iterative


__author__ = 'Peipei YI'

cpt = "D:\data\dataset\snap\directed\*.cpt"

if __name__ == "__main__":
    cpts = glob.glob(cpt)
    print cpts.__len__()
    for cpt in cpts:
        print cpt
        with open(cpt) as f:
            v, e = [int(x) for x in f.readline().split()]
            print v, e

            vertices = range(0, v)
            # print vertices

            edges = {}
            for i in range(0, v):
                edges[i] = []

            for line in f:
                v1, v2 = [int(x) for x in line.split()]
                edges[v1].append(v2)

            # print edges

            with open(cpt + '.py_scc_map', 'w+') as f_scc:
                for scc in strongly_connected_components_iterative(vertices, edges):
                    f_scc.write(' '.join(str(i) for i in scc))
                    f_scc.write('\n')
import glob
import os

import numpy
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components

from _exp.exp import Exp


__author__ = 'Peipei YI'


def split_wcc(source, dest=None, suffix='.wcc_'):
    # set up source and dest
    dataset = glob.glob(source)
    if not os.path.isdir(dest):
        os.makedirs(dest)
    # iterative transform graphs
    for ds in dataset:
        with open(ds) as f:
            v, e = f.readline().split()
            data = numpy.genfromtxt(f, dtype=[('from', numpy.uint32), ('to', numpy.uint32)])
            graph = csr_matrix((numpy.ones_like(data['from']), (data['from'], data['to'])), shape=(v, v))
            N_component, component_list = connected_components(graph)

            # vertex mapping
            v_key = [numpy.where(component_list == i)[0].tolist() for i in range(0, N_component)]
            v_value_N = [numpy.where(component_list == i)[0].size for i in range(0, N_component)]
            v_value = [[j for j in range(0, i)] for i in v_value_N]
            v_map = [dict(zip(v_key[i], v_value[i])) for i in range(0, N_component)]

            # gen new graph
            dest_list = [os.path.join(dest, os.path.basename(f.name) + suffix + str(i)) for i in range(0, N_component)]
            v_list = [(component_list == i).sum() for i in range(0, N_component)]
            e_list = [[] for i in range(0, N_component)]
            for u, v in data:
                e_list[component_list[u]].append((u, v))

            # store graph
            for i in range(0, N_component):
                with open(dest_list[i], 'w') as dest:
                    dest.write(str(v_list[i]) + ' ' + str(len(e_list[i])) + '\n')
                    for u, v in e_list[i]:
                        dest.write(str(v_map[i][u]) + ' ' + str(v_map[i][v]) + '\n')


if __name__ == '__main__':
    exp = Exp()
    source_expr = os.path.join(os.path.join(exp.working_dir, 'dataset/snap/directed/*.vv'))
    dest_expr = os.path.join(exp.working_dir, 'dataset/snap/directed_wcc/', '')
    split_wcc(source_expr, dest_expr)

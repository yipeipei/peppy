import sys
from _exp.reach.biclique import BiClique
from graph.graph import Digraph

__author__ = 'Peipei YI'

if __name__ == '__main__':
    biclique =BiClique()
    with open(sys.argv[1]) as f:
        for line in f:
            line = [int(i) for i in line.split()]
            biclique.add_edge((line[0], line[1]))

    print "load finished"

    with open(sys.argv[1] + '.mb', 'w+') as f:
        for mb in biclique.find_cliques():
            f.write(' '.join([str(i) for i in mb[0]]))
            f.write('\n')
            f.write(' '.join([str(i) for i in mb[1]]))
            f.write('\n\n')

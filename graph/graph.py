import collections
import os
import sys
import math
import time

__author__ = 'Peipei YI'


class Digraph:
    def __init__(self, path=None, type=None):
        self.vertices = set()
        self.edges = collections.defaultdict(set)

    def __iter__(self):
        for v in self.vertices:
            yield v

    def add_edge(self, u, v):
        self.vertices.add(u)
        self.vertices.add(v)
        self.edges[u].add(v)

    def get_neighbour(self, v):
        return self.edges[v]

    def transitive_closure_iterative(self):
        """
        This is a non-recursive inplace transitive closure implementation.
        """
        stack = []  # hold path from source
        index = {}  # hold stack length
        traversed = set()  # hold traversed vertices

        for s in self:
            self.edges[s].add(s)
            index.clear()
            if s not in traversed and len(self.edges[s]):
                to_do = [('VISIT', s)]
                while to_do:
                    op, v = to_do.pop()
                    if op == 'VISIT':

                        traversed.add(v)
                        index[v] = len(stack)
                        stack.append(v)
                        to_do.append(('POSTVISIT', v))
                        to_do.extend([('VISITEDGE', w) for w in self.edges[v]])

                    elif op == 'VISITEDGE':
                        if v not in index:
                            to_do.append(('VISIT', v))
                        elif v in traversed:
                            for i in stack:
                                self.edges[i] |= self.edges[v]
                    elif op == 'POSTVISIT':
                        del stack[index[v]:]
                        for i in stack[:-1]:
                            self.edges[i].add(v)
        return self

    def dfs_iterative(self, source):
        pass


if __name__ == '__main__':
    t = time.time()
    if 3 != len(sys.argv) or not os.path.isfile(sys.argv[1]):
        print 'usage:', sys.argv[0], '[input file path]', '[vv|vdvv]'
        sys.exit(-1)

    g = Digraph()

    if sys.argv[2] == 'vdvv':
        with open(sys.argv[1]) as f:
            for line in f:
                line = [int(i) for i in line.split()]
                if len(line) < 3:
                    continue
                for i in line[2:]:
                    g.add_edge(line[0], i)
    if sys.argv[2] == 'vv':
        with open(sys.argv[1]) as f:
            for line in f:
                line = [int(i) for i in line.split()]
                if len(line) != 2:
                    continue
                g.add_edge(line[0], line[1])
    # print g.edges
    g.transitive_closure_iterative()
    count = [len(edges) for edges in g.edges.values()]
    print sum(count), "@", str(time.time() - t)

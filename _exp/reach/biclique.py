import collections
import random
import time

__author__ = 'Peipei YI'


class GraphError(Exception):
    pass


class BiClique:
    """
    source: https://github.com/escherba/undirected_graph
    """

    def __init__(self, base=None):
        if base is None:
            self.U2V = collections.defaultdict(set)  # left to right mapping dict
            self.V2U = collections.defaultdict(set)  # right to left mapping dict
            self.edges = {}
        else:
            if not isinstance(base, self.__class__):
                raise TypeError('base object has incorrect type')
            '''copy of base object'''
            self.U2V = collections.defaultdict(set, base.U2V)
            self.V2U = collections.defaultdict(set, base.V2U)
            self.edges = dict(base.edges)

    def _map_edge(self, edge):
        u, v = edge
        if u is None or v is None:
            raise GraphError('an edge must connect two nodes')
        self.U2V[u].add(v)
        self.V2U[v].add(u)

    def add_edge(self, edge):
        self._map_edge(edge)

    def remove_edge(self, edge):
        u, v = edge
        if u is None or v is None:
            raise GraphError('an edge must connect two nodes')
        self.U2V[u].remove(v)
        self.V2U[v].remove(u)

    @property
    def edge_count(self):
        return len(self.edges)

    @property
    def U(self):
        """
        returns a set of all "left" nodes
        """
        return self.U2V.keys()

    @property
    def V(self):
        """
        returns a set of all "right" nodes
        """
        return self.V2U.keys()

    def __repr__(self):
        return '\n'.join([str(self.U2V), str(self.V2U), str(self.edges)])

    def find_cliques(self, nodes=None):
        """
        MBEA algorithm from Zhang et al. (2008)
        Enumerate all maximal bicliques in an undirected bipartite graph.
        Python implementation by Eugene Scherba (Boston University, 2010).

        Adapted from: Zhang, Y., Chesler, E. J. & Langston, M. A. "On
        finding bicliques in bipartite graphs: a novel algorithm with
        application to the integration of diverse biological data types."
        Hawaii International Conference on System Sciences 0, 473+ (2008).
        URL http://dx.doi.org/10.1109/HICSS.2008.507.

        This non-recursive version implemented in Python by Eugene
        Scherba (2010)

        L - a set of vertices in U that are common neighbors of vertices
            in R
        R - a set of vertices in V belonging to the current biclique
        P - a set of vertices in V that can be added to R
        Q - a set of vertices in V that have been previously added to R
        """

        if nodes is None:
            # search nodes for the entire graph
            # L = self.U  # modify to suit py2k
            L = set(self.U)
            P = set(self.V)
        else:
            # search only the specified subset
            # L = nodes[0]  # modify to suit py2k
            L = set(nodes[0])
            P = set(nodes[1])

        stack = [(L, set(), P, set())]
        while (stack):
            L, R, P, Q = stack.pop()
            while P:  # len(P) > 0:
                x = P.pop()
                # extend biclique
                R_prime = R | {x}
                L_prime = L & self.V2U[x]
                # create new sets
                P_prime = set()
                Q_prime = set()
                # check maximality
                is_maximal = True
                for v in Q:
                    # checks whether L_prime is a subset of all adjacent nodes
                    # of v in Q
                    Nv = L_prime & self.V2U[v]
                    if len(Nv) == len(L_prime):
                        is_maximal = False
                        break
                    elif Nv:  # len(Nv) > 0:
                        # some vertices in L_prime are not adjacent to v:
                        # keep vertices adjacent to some vertex in L_prime
                        Q_prime.add(v)
                if is_maximal:
                    for v in P:
                        # get the neighbors of v in L_prime
                        Nv = L_prime & self.V2U[v]
                        if len(Nv) == len(L_prime):
                            R_prime.add(v)
                        elif Nv:  # len(Nv) > 0:
                            # some vertices in L_prime are not adjacent to v:
                            # keep vertices adjacent to some vertex in L_prime
                            P_prime.add(v)
                    yield (L_prime, R_prime)  # report maximal biclique
                    if P_prime:  # len(P_prime) > 0:
                        stack.append((L_prime, R_prime, P_prime, Q_prime))
                # move x to former candidate set
                Q.add(x)


if __name__ == '__main__':
    biclique = BiClique()

    for i in range(1, 10):
        edge = 0, i
        biclique.add_edge(edge)

    biclique.remove_edge((0, 5))
    print biclique

    for bc in biclique.find_cliques():
        print bc

    # benchmark for cit-patents
    t0 = time.time()
    v_max = 3774768
    e_max = 16518947
    for i in range(0, e_max):
        edge = random.randint(0, v_max - 1), random.randint(0, v_max - 1)
        biclique.add_edge(edge)
    print 'elapsed time:', time.time() - t0

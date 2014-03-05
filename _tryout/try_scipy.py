import os
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra
from scipy.sparse.csgraph import connected_components
from scipy.spatial.distance import pdist, squareform
from _exp.exp import Exp

__author__ = 'Peipei YI'


exp = Exp()

'''
Example: Word Ladders
'''
word_list = open(os.path.join(exp.working_dir + 'dataset/linux.words')).readlines()
word_list = map(str.strip, word_list)

word_list = [word for word in word_list if len(word) == 3]
word_list = [word for word in word_list if word[0].islower()]
word_list = [word for word in word_list if word.isalpha()]
word_list == map(str.lower, word_list)
print len(word_list)

word_list = np.asarray(word_list)
print word_list.dtype
word_list.sort()

word_bytes = np.ndarray((word_list.size, word_list.itemsize), dtype='int8', buffer=word_list.data)
print word_bytes.shape

hamming_dist = pdist(word_bytes, metric='hamming')
graph = csr_matrix(squareform(hamming_dist < 1.5 / word_list.itemsize))

i1 = word_list.searchsorted('ape')
print word_list[i1]
i2 = word_list.searchsorted('man')
print word_list[i2]

distances, predecessors = dijkstra(graph, indices=i1, return_predecessors=True)
print distances[i2]

path = []
i = i2
while i != i1:
    path.append(word_list[i])
    i = predecessors[i]
path.append(word_list[i1])
print path[::-1]

N_components, component_list = connected_components(graph)
print N_components

print [np.sum(component_list == i) for i in range(15)]

print [list(word_list[np.where(component_list == i)]) for i in range(1, 15)]

distances, predecessors = dijkstra(graph, return_predecessors=True)
print np.max(distances[~np.isinf(distances)])

i1, i2 = np.where(distances == 8)
print zip(word_list[i1], word_list[i2])
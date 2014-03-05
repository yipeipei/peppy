import glob
import os

import numpy as np
from _exp.exp import Exp


__author__ = 'Peipei YI'


class TFLabel():
    """
    TFLabel python helper.

    References
    ----------
    .. [1] Cheng, James, et al. "TF-Label: a topological-folding labeling scheme
       for reachability querying in a large graph." SIGMOD'13. ACM, 2013.

    """

    def __init__(self, files):
        """
        Parameters
        ----------
        files : list
            File list contains the 4 output files of the original tflabel implement.

        Examples
        --------
        files = ['*_dag_label', '*_TL', '*_tlstart', '*_topolabel']

        """
        if not len(files) == 4:
            raise Exception('length of f_list must be exact 4')
        else:
            # load from cxx output files, explict open file with 'rb' mode is important!
            self.dag_label = np.fromfile(open(files[0], 'rb'), dtype=np.uint32)
            self.topo_level = np.fromfile(open(files[3], 'rb'), dtype=np.uint32)
            self.tflabel_size = np.fromfile(open(files[2], 'rb'), dtype=np.uint32)
            # load tflabel
            self.tflabel = []
            with open(files[1], 'rb') as f:
                for s in self.tflabel_size:
                    self.tflabel.append(np.fromfile(f, dtype=np.uint32, count=s))
            # affiliate info
            self.name = os.path.basename(files[0])
            self.v = len(self.dag_label)
            # check constraint
            assert len(self.dag_label) == os.stat(files[0]).st_size/4
            assert len(self.topo_level) == os.stat(files[3]).st_size/4
            assert len(self.tflabel_size) == os.stat(files[2]).st_size/4
            for label, s in zip(self.tflabel, self.tflabel_size):
                assert len(label) == s

    def query(self, u, v):
        """
        answer reachability query using tflabel
        """
        return np.intersect1d(self.tflabel[u], self.tflabel[self.v + v], True)

    def gen_tc(self):
        """
        generate transitive closure by enumerating all query(u, v)
        """
        tc = np.ndarray((self.v, self.v), dtype=bool)
        for u in range(0, self.v):
            for v in range(0, self.v):
                tc[u][v] = len(self.query(u, v))
        return tc

    def size(self):
        """
        return size of current tflabel, by sum() the tflabel_size
        """
        return self.tflabel_size.sum()

    def keep(self):
        """
        return set of label without self-self reachability
        """
        label_keep = set()
        for index, label in enumerate(self.tflabel):
            for c in [center for center in label if not center == index and not center == (index - self.v)]:
                label_keep.add(c)
            # for center in np.setdiff1d(label, [index, index - self.v], assume_unique=True):
            #     label_keep.add(center)

            # for v in label:
            #     if not v == index and not v == (index - self.v):
            #         label_keep.add(v)
        return label_keep

    def stats(self):
        """
        return some key statistical info of tflabel
        """
        return [self.name, self.v, self.size(), len(self.keep())]

    def show_label(self, v='all'):
        if 'all' == v:
            for index, label in enumerate(self.tflabel):
                print index % self.v, label
        else:
            if 0 <= v <= self.v:
                raise NotImplemented

    def __repr__(self):
        if self.v > 100:
            raise Exception('number of vertices exceeds 1000, abort.')
        else:
            return '\n'.join(['dag_label', str(self.dag_label.tolist()),
                              'topo_level', str(self.topo_level.tolist()),
                              'tflabel_size', str(self.tflabel_size.tolist()),
                              'tflabel', '\n'.join([str(label.tolist()) for label in self.tflabel])])


if __name__ == '__main__':
    exp = Exp()

    tflabel_path = os.path.join(exp.temp_dir, 'tflabel_k1', '')
    # names = ['small', 'complex']
    names = ['']
    print tflabel_path
    print '\t'.join(['dataset', 'V', 'label_size', 'keep'])
    for name in names:
        files = glob.glob(tflabel_path + name + '*')
        for i in range(0, len(files)/4):
            # print os.stat(files[4*i + 1]).st_size / 4
            tflabel = TFLabel(files[4*i: 4*(i+1)])
            # for n in range(0, len(tflabel.tflabel_size)):
            #     if tflabel.tflabel_size[n] != 1:
            #         print n, tflabel.tflabel_size[n]
            # print tflabel.tflabel_size.argmax()
            print '\t'.join(str(i) for i in tflabel.stats())

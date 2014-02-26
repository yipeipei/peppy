import glob

import numpy as np


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
            self.dag_label = np.fromfile(open(files[0]), dtype=np.uint32)
            self.topo_level = np.fromfile(open(files[3]), dtype=np.uint32)
            self.tflabel_size = np.fromfile(open(files[2]), dtype=np.uint32)
            f_tflabel = open(files[1])
            self.tflabel = []
            for s in self.tflabel_size:
                self.tflabel.append(np.fromfile(f_tflabel, dtype=np.uint32, count=s))
            self.v = len(self.dag_label)

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
            for v in label:
                if not v == index and not v == (index - self.v):
                    label_keep.add(v)
        return label_keep

    def stats(self):
        """
        return some key statistical info of tflabel
        """
        return [self.v, self.size(), len(self.keep())]

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
    names = ['small', 'complex']
    tflabel_path = 'D:/data/dataset/snap/tflabel/'
    for name in names:
        print '\n', name
        files = glob.glob(tflabel_path + name + '*')
        tflabel = TFLabel(files)
        print tflabel.__repr__()
        print '\t'.join(str(i) for i in tflabel.stats())
        print tflabel.gen_tc()
        print tflabel.keep()
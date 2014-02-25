import glob

import numpy as np


__author__ = 'Peipei YI'


class TFLabel():
    def __init__(self, files):
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

    def __repr__(self):
        if len(self.dag_label) > 100:
            raise Exception('number of vertices exceeds 1000, abort.')
        else:
            return '\n'.join(['dag_label', str(self.dag_label.tolist()),
                              'topo_level', str(self.topo_level.tolist()),
                              'tflabel_size', str(self.tflabel_size.tolist()),
                              'tflabel', '\n'.join([str(label.tolist()) for label in self.tflabel])])

if __name__ == '__main__':
    f_list = glob.glob('D:/data/dataset/snap/tflabel/complex.test.body.cpt.dag*')
    tflabel = TFLabel(f_list)
    print tflabel.__repr__()

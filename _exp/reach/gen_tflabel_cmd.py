import glob
import os

__author__ = 'Peipei YI'

tflabel_path = 'D:/data/TF_label_release'
dag_path = 'D:/data/dataset/snap/directed/*.clean'
in_path_cygwin = '/cygdrive/d/data/dataset/snap/directed/'
out_path_cygwin = '/cygdrive/d/data/dataset/snap/tflabel/'

if __name__ == '__main__':
    with open(tflabel_path + '/run', 'w+') as f:
        f.write('#!/bin/bash')
        f.write('\n')
        # compile
        f.write('g++ -o pre_processing/pre_check.exe pre_processing/pre_check.cpp -O3\n')
        # index
        for dataset in glob.glob(dag_path):
            filename = os.path.basename(dataset)
            f.write(
                'pre_processing/pre_check.exe ' + in_path_cygwin + filename + ' -i ' + out_path_cygwin + filename + ' &> ' + out_path_cygwin + filename + '.log\n')

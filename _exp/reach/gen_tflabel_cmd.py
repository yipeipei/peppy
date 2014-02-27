#! /usr/bin/env python

import glob
import os
import re

__author__ = 'Peipei YI'

dataset = '~/working/dataset/snap/'
dataset = os.path.expanduser(dataset)

tflabel = '~/working/TF_label_release/'
tflabel  = os.path.expanduser(tflabel)

output = '/tmp/csppyi/'

re_k = re.compile('const int K = [\d]+;')


def gen_cmd(k):
    script_path = tflabel + 'tflabel_k' + str(k) + '.sh'
    new_k = 'const int K = ' + str(k) + ';'

    tflabel_path = output + 'tflabel_out/tflabel_k' + str(k) + '/'
    tflabel_log_path = output + 'tflabel_out/tflabel_k' + str(k) + '_log/'
    # make dirs for tFlabel output
    if not os.path.exists(tflabel_path):
        os.makedirs(tflabel_path)
    if not os.path.exists(tflabel_log_path):
        os.makedirs(tflabel_log_path)
    # update pre_check.cpp with new assignment for k
    # cpp = open(cpp_path, 'r').read()
    # cpp = re.sub(re_k, new_k, cpp, count=1)
    # open(cpp_path, 'w').write(cpp)
    # generate shell script
    with open(script_path, 'wb+') as f:
        cmd = '#! /bin/bash\n'
        # compile
        cmd += 'g++ -o '+ tflabel + 'pre_processing/pre_check.exe ' + tflabel + 'pre_processing/pre_check.cpp -O3\n'
        # index
        for dname in sorted(glob.glob(dataset + '/*.clean')):
            filename = os.path.basename(dname)
            cmd += tflabel + 'pre_processing/pre_check.exe ' + dataset + filename + ' -i ' + tflabel_path + filename + ' &>  ' + tflabel_log_path + filename + '.log\n'
        f.write(cmd)


if __name__ == '__main__':
    for i in range(0, 10):
        gen_cmd(2**i)

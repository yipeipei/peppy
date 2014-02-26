import glob
import os
import re

__author__ = 'Peipei YI'

base_win = 'D:/data/dataset/snap/'
base_cygwin = '/cygdrive/d/data/dataset/snap/'
cpp_path = base_win + 'TF_label_release/pre_processing/pre_check.cpp'
re_k = re.compile('const int K = [\d]+;')


def gen_cmd(k):
    script_path = 'tflabel_k' + str(k) + '.sh'
    new_k = 'const int K = ' + str(k) + ';'

    tflabel_path = 'tflabel_out/tflabel_k' + str(k) + '/'
    tflabel_log_path = 'tflabel_out/tflabel_k' + str(k) + '_log/'
    # make dirs for tflabel output
    if not os.path.exists(base_win + tflabel_path):
        os.makedirs(base_win + tflabel_path)
    if not os.path.exists(base_win + tflabel_log_path):
        os.makedirs(base_win + tflabel_log_path)
    # update pre_check.cpp with new assignment for k
    # cpp = open(cpp_path, 'r').read()
    # cpp = re.sub(re_k, new_k, cpp, count=1)
    # open(cpp_path, 'w').write(cpp)
    # generate shell script
    with open(base_win + script_path, 'wb+') as f:
        cmd = '#! /bin/bash\n'
        # compile
        cmd += 'g++ -o TF_label_release/pre_processing/pre_check.exe TF_label_release/pre_processing/pre_check.cpp -O3\n'
        # index
        for dataset in glob.glob(base_win + 'directed/*.clean'):
            filename = os.path.basename(dataset)
            cmd += 'TF_label_release/pre_processing/pre_check.exe ' + 'directed/' + filename + ' -i ' + tflabel_path + filename + ' &>  ' + tflabel_log_path + filename + '.log\n'
        f.write(cmd)


if __name__ == '__main__':
    for i in range(0, 10):
        gen_cmd(2**i)
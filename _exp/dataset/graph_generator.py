import os
import sys

__author__ = 'Peipei YI'


def gen_path_graph(n, dir):
    f_out = os.path.join(dir, 'digraph_path_n' + str(n))
    with open(f_out, 'w') as f:
        f.write(str(n) + ' ' + str(n - 1) + '\n')
        for u in range(0, n - 1):
            f.write(str(u) + ' 1 ' + str(u + 1) + '\n')


def gen_star_graph(n, dir=None):
    f_out = os.path.join(dir, 'digraph_instar_n' + str(n))
    with open(f_out, 'w') as f:
        f.write(str(n) + ' ' + str(n - 1) + '\n')
        for u in range(0, n - 1):
            f.write(str(u) + ' 1 ' + str(n-1) + '\n')

    f_out = os.path.join(dir, 'digraph_outstar_n' + str(n))
    with open(f_out, 'w') as f:
        f.write(str(n) + ' ' + str(n - 1) + '\n')
        f.write('0 ' + str(n-1) + ' ')
        f.write(' '.join([str(i) for i in range(1, n)]))


if __name__ == '__main__':
    if 4 != len(sys.argv):
        print 'usage', sys.argv[0], '[type]', '[N]', '[dest]'
        sys.exit(-1)

    if not os.path.isdir(sys.argv[3]):
        print '[dest] should be an existing dir.'
        sys.exit(-1)

    if sys.argv[1] == 'path':
        gen_path_graph(int(sys.argv[2]), sys.argv[3])
    elif sys.argv[1] == 'star':
        gen_star_graph(int(sys.argv[2]), sys.argv[3])
    elif sys.argv[1] == 'all':
        gen_path_graph(int(sys.argv[2]), sys.argv[3])
        gen_star_graph(int(sys.argv[2]), sys.argv[3])
    else:
        print "[type] can only accept [path, star, all]"
        sys.exit(-1)
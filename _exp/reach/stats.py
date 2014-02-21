import glob
import os
import re

__author__ = 'Peipei YI'

snap = 'D:/data/dataset/snap/'
directed = snap + 'directed/'
tflabel = snap + 'tflabel/'
tflabel_log = snap + 'tflabel_log/'

data = {
    'origin': directed + '*.txt',
    'header': directed + '*.header',
    'cpt': directed + '*.cpt',
    'dag': directed + '*.dag',
    'clean': directed + '*.clean',
    'tflabel_log': tflabel_log + '*.log'
}

# for f in glob.glob(data['tflabel_log']):
#     os.rename(f, f.replace('clean_', 'clean.'))

name = [os.path.splitext(os.path.basename(p))[0] for p in glob.glob(data['origin'])]
print name.__len__()

ve_snap = []
p_ve = re.compile('# Nodes: ([\d]+) Edges: ([\d]+)')
for header in glob.glob(data['header']):
    flag = False
    for line in open(header):
        m = p_ve.match(line)
        if m:
            flag = True
            ve_snap.append([m.group(1), m.group(2)])
    if not flag:
        ve_snap.append(('N/A', 'N/A'))
print ve_snap.__len__()

ve_cpt = []
for cpt in glob.glob(data['cpt']):
    ve_cpt.append([int(n) for n in open(cpt).readline().split()])
print ve_cpt.__len__()

ve_dag = []
for dag in glob.glob(data['dag']):
    ve_dag.append([int(n) for n in open(dag).readline().split()])
print ve_dag.__len__()

ve_dag_clean = []
for clean in glob.glob(data['clean']):
    ve_dag_clean.append([int(n) for n in open(clean).readline().split()])
print ve_dag_clean.__len__()

tf_log = []
p_extra = [re.compile('1 th highdegree vertex: ([\d]+) out degree'),
           re.compile('([\d]+) original topological level'),
           re.compile('([\d]+)total DAG levels after deleting high-degree vertices'),
           re.compile('([\d]+) total round in TF hierarchy ')]
for log in glob.glob(data['tflabel_log']):
    extra = []
    for line in open(log):
        for p in p_extra:
            m = p.match(line)
            if m:
                extra.append(m.group(1))
    tf_log.append(extra)
print tf_log.__len__()


# print header
col = 'name', 'V(snap)', 'E(snap)', 'V(cpt)', 'E(cpt)', 'V(dag)', 'E(dag)', 'V(clean)', 'E(clean)' \
    , '1stHiDG', 'TopoLevel', 'DAGLevel', 'total round'
print '\t'.join(col)
# print record
for i in range(0, len(name)):
    record = name[i], ve_snap[i][0], ve_snap[i][1], ve_cpt[i][0], ve_cpt[i][1] \
        , ve_dag[i][0], ve_dag[i][1], ve_dag_clean[i][0], ve_dag_clean[i][1] \
        , tf_log[i][0], tf_log[i][1], tf_log[i][2], tf_log[i][3]
    print '\t'.join([str(attr) for attr in record])
## -*- coding: utf-8 -*-

import os, codecs, sqlite3, sys
try:
    import simplejson as json
except:
    import json

os.chdir(os.path.dirname(__file__))
from collections import defaultdict

d = defaultdict(list) 
for l in codecs.open('2.csv', 'r', 'utf-8'):
    line = [s.strip() for s in l.split('\t')]
    k = line[0]
    c = line[3:]
    d[k].append(c)
open('icd9_to_10.json', 'wb').write(json.dumps(d))

d = {}
for l in codecs.open('ICD_EX_CODE.txt', 'r', 'utf-8'):
    icd10, icd10e = [s.strip() for s in l.split(',')]
    d[icd10] = icd10e
    d[icd10e] = icd10
open('dic_icd10_enc.json', 'wb').write(json.dumps(d))

sys.exit()

allnum = '0123456789'
dd10 = json.loads(open('icd9_to_10.json', 'rb').read())
dk10 = set(dd10.keys())

def icd9_corrected(c):
    # normal lookup
    if c in dk10:
        return True, c, c 

    # custom lookup: some special cases
    if c in ['042.9', '044.9']:
        return True, c, '042'
    elif c == '245.90':
        return True, c, '245.9'
    elif c == '645.03':
        return True, c, '645.20'
    elif c == '718.60':
        return True, c, '718.65'
    elif c == '779.6': # XXX questionable
        return True, c, '779.8'
    
    # add some characters to search
    nc = len(c.replace('.', ''))
    if nc == 4:
        for s in allnum:
            cc = c + s
            if cc in dk10:
                return True, c, cc 
    elif nc == 3:
        if '.' in c:
            for s in allnum:
                cc = c + s
                if cc in dk10:
                    return True, c, cc 
                else:
                    for ss in allnum:
                        ccc = cc + s
                        if ccc in dk10:
                            return True, c, ccc
        else:
            for s in allnum:
                cc = c + '.' + s
                if cc in dk10:
                    return True, c, cc 

    return False, c, '' 

cn = sqlite3.connect('/home/cytu/usr/admin/cwtu/mycis/mycis.db')
cr = cn.cursor()
rlist = [r[0] for r in cr.execute('select code from diag').fetchall()]
icd9s = sorted(list(set(rlist)))
ik = set(icd9s)
culprit = [ll for ll in sorted(list(ik - dk10)) if ll[0] in allnum]
culprit = [ll for ll in sorted(list(dk10 - ik)) if ll[0] in allnum]
print len(culprit)

culprit_new = []
for c in culprit:
    ans, c_orig, c_ext= icd9_corrected(c)
    if not ans:
        culprit_new.append(c_orig)

r = cr.execute('select distinct diag.code, diag.name from tk_diag inner join diag on tk_diag.diag_id = diag.id where diag.code in (%s)' % ','.join('?' * len(culprit_new)), culprit_new).fetchall()
 
codecs.open('culprits.txt', 'w', 'utf-8').write('\n'.join(['\t\t'.join(rr) for rr in r]))

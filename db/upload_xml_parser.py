# -*- coding: utf-8 -*-

import os, time, sys
from fnmatch import fnmatch
import xml.etree.ElementTree as ET

os.chdir(os.path.dirname(__file__))
cat = os.path.join

fl = []
for root, dirs, files in os.walk(r'C:\VSBW\upload'):
    # exclude subfolder 'DBG'
    dirs[:] = [d for d in dirs if d != 'DBG'] 
    for f in files:
        if fnmatch(f, 'upload_*.xml'):
            fl.append(cat(root, f))

fl = sorted(fl)
n_fl = len(fl)
tks = []
#fl = ['c:/vsbw/upload/upload_1041204125611.xml']
#fl = ['c:/vsbw/upload/upload_1050202214544.xml']

def log(msg, in_place=False):
    if in_place:
        sys.stdout.write(msg + '\r')
        sys.stdout.flush()
    else:
        print(msg)

start_time = time.time()
log('start collecting all tks...')
for nn, f in enumerate(fl):
    log('now doing file %s (%d / %d, %d%%)' % (f, nn + 1, n_fl, int(100. * (nn + 1) / n_fl)), in_place=True)
    # ElementTree does not accept multibyte encoding
    try:
        root = ET.fromstring(open(f, 'rb').read().decode('big5', 'ignore').replace('<?xml version="1.0" encoding="BIG5"?>', '<?xml version="1.0"?>').replace(u'<1050101生效先改回------------------------------- />', ''))
    except:
        log('error in file %s' % f)
        continue

    for child in enumerate(root):
        d = {'treatments': [], 'header': {}, 'info': {}}
        for c in child[1]:
            t = c.tag 
            if t == 'MB2':
                dd = {}
                for cc in c:
                    if cc.text is not None:
                        dd[cc.tag] = cc.text
                d['treatments'].append(dd) 
            elif t == 'MB1':
                for cc in c:
                    if cc.text is not None:
                        d['info'][cc.tag] = cc.text 
            else:
                for cc in c:
                    if cc.text is not None:
                        d['header'][cc.tag] = cc.text
        tks.append(d)
log('Completed collecting tks; Used %f seconds.' % (time.time() - start_time,))

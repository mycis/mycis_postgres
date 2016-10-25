# -*- coding: utf-8 -*-

import os, re, codecs, time 
from dbfread import DBF as dbf

startpath = r'c:\VSBW' 
cat = os.path.join
p = re.compile(r'^[0-9A-F]{40}$')

print('start searching...')
start_time = time.time()

dbfs = []
s = [] 
for root, dirs, files in os.walk(startpath):
    dirs[:] = [d for d in dirs if d not in ['upload',]]
    level = root.replace(startpath, '').count(os.sep)
    indent = ' ' * 4 * (level)
    s.append('{}{}/'.format(indent, os.path.basename(root)))
    subindent = ' ' * 4 * (level + 1)
    for f in files:
        b = (os.path.splitext(f)[1]).lower() in ('.dbf',)
        if b:
            s.append('{}{}'.format(subindent, f))
            dbfs.append(cat(root, f))

s.append('\n++++++++++++++++++++++++++++++++++++++++++++++++++')
s.append('\nThere are %s dbf files:' % str(len(dbfs)))
s.append('\n++++++++++++++++++++++++++++++++++++++++++++++++++')
        
ss, ss1 = [], []
n_ss = 0
errors = []
for db in dbfs:
    name = os.path.splitext(os.path.split(db)[1])[0]
    
    try:
        table = dbf(db)
        if len(table):
            sizes = []
            for i, field in enumerate(table.fields):
                field_name, size = field.name, field.length
                if size >= 40:
                    sizes.append((i, size))
                    s1 = '%-15s  %3d' % (field_name, size)
                    ss.append(s1)
            
            if sizes: 
                ss.append('\n' + name)
                ss.append('-' * 20 + '\n')
                n_ss += 1
                b = False
                for record in table:
                    for i, field in enumerate(table.fields):
                        if i in [sz[0] for sz in sizes]:
                            data = record[field.name]
                            if re.search(p, data):
                                ss1.append(u'key in ' + db)
                                print('key in ' + db)
                                b = True
                                break
                    if b:
                        break
                            #if data == 'FE46943D9BD7AC3DF751D04323624F52AF898634':
                            #    ss.append('Found key!! In ' + db)
                            #    break
    except:
        errors.append(db)
        ss.append('\n(table %s aborted.)\n' % name) 

print('searched %s files: using %f seconds.' % (n_ss, time.time() - start_time))
codecs.open(r'c:\inspect_dbf_report.txt', 'w', 'utf-8').write(u'\n'.join(s + ss + ss1))
codecs.open(r'c:\error_dbfs.txt', 'w', 'utf-8').write(u'\n'.join(errors))

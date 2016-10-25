# -*- coding: utf-8 -*-

import os, fnmatch, subprocess, codecs

os.chdir(os.path.dirname(__file__))
#pr = os.path.basename(os.getcwd())
pr = 'mycis'
cat = os.path.join

def all_files(root, patterns='*', single_level=False, yield_folders=False):
    # Expand patterns from semicolon-separated string to list
    patterns = patterns.split(';')
    
    for path, subdirs, files in os.walk(root):
        if yield_folders:
            files.extend(subdirs)
        files.sort( )
        for name in files:
            for pattern in patterns:
                if fnmatch.fnmatch(name, pattern):
                    yield cat(path, name)
                    break
        if single_level:
            break

QRC = '''<!DOCTYPE RCC>
<RCC version="1.0">
<qresource>
%s
</qresource>
</RCC>'''

files = []
for path in all_files('./res/img', '*.png', yield_folders=False):
    files.append(path.replace('\\', '/'))

open(cat('res', pr + '.qrc'), 'w').write(QRC % ('\n'.join(['<file>../%s</file>' % f[2:] for f in files])))

for i, path in enumerate(all_files('./designer', '*.ui')):
    f = os.path.basename(path)[:-3]
    ff = os.path.abspath(path)
    ft = codecs.open(ff, 'r', 'utf-8')
    s = ft.read()
    ft.close()
    
    codecs.open(ff, 'w', 'utf-8').write(s.replace(u'微軟正黑體', 'Microsoft JhengHei'))

    subprocess.call('pyuic4 -x -o ./ui/%s.py %s' % (f, ff), shell=True)
subprocess.call(['pyrcc4', '-o', './ui/%s_rc.py' % pr, cat('res', '%s.qrc' % pr)])

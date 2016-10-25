# -*- coding: utf-8 -*-

import codecs, os, urllib, time, sqlite3, sys, re
try:
    import simplejson as json
except:
    import json

from xml.etree.ElementTree import Element, SubElement
import xml.etree.ElementTree as ET
from operator import itemgetter

from xml.etree import ElementTree
from xml.dom import minidom

def prettify(elem): # from PyMOTW
    '''Return a pretty-printed XML string for the Element.'''
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent='  ')

def rule(s, b_decor=False):
    s0 = s.strip().replace(' ', '').replace('(', u'（').replace(')', u'）')
    if s0 == u'全':
        s0 = ''
    elif s0[0] == u'連':
        s0 = s0[1:]
    elif s0 == u'單全':
        s0 = u'單'
    elif s0 == u'雙全':
        s0 = u'雙'
    if b_decor:
        return u'（' + s0 + u'）' if s0 else ''
    return s0 if s0 else ''

os.chdir(os.path.dirname(__file__))
cat = os.path.join

fn_zip = 'zip.xml'
fn_json = 'list_zip.json'

if os.path.isfile(fn_zip):
    tree = ET.parse(fn_zip) 
    zips = tree.getroot()
    d = json.loads(open(fn_json, 'rb').read())
    for i in sorted(d.keys()):
        print i
    for i in zips.findall('city'):
        print i.text.strip()
    
else:
    #fn = 'zip_city_area.txt' 
    #if not os.path.isfile(fn):
    #    start_time = time.time()
    #    print u'下載中華郵政郵遞區號純文字檔，請稍候...'
    #urllib.urlretrieve('http://download.post.gov.tw/post/download/Xml_10508.xml',fn)
    #    print u'下載完畢，使用 %f 秒。地址資料處理中...' % (time.time() - start_time)
    #l = []
    #for ii, i in enumerate(codecs.open(cat(os.getcwd(), fn), 'r', 'utf-8')):
    #    l.append((i[0:5], i[5:8], i[8:11].strip(), i[13:25].strip()))
    #l = sorted(list(set([ll[1:] for ll in l])), key=itemgetter(0, 1, 2))
    
    start_time = time.time()
    #print u'下載中華郵政郵遞區號 xml 檔，請稍候...'
    fn = '/home/cytu/Downloads/Xml_10508.xml'
    #urllib.urlretrieve('http://download.post.gov.tw/post/download/Xml_10508.xml',fn)
    #print u'下載完畢，使用 %f 秒。地址資料處理中...' % (time.time() - start_time)
    tree = ET.parse(fn)
    root = tree.getroot()
    l = []
    for ii, child in enumerate(root):
        ll = [''] * 4
        for cc in child:
            ll[int(cc.tag[2]) - 1] = cc.text.strip()
        l.append((ll[0], ll[-1][:3], ll[-1][3:], ll[1], ll[2].strip().replace(' ', '')))
    l = sorted(l, key=itemgetter(1, 2, 3, 0, 4))

    codecs.open(cat('db', 'txt', 'zip.txt'), 'w', 'utf-8').write('\n'.join([ll[0] + '   ' + ll[1] + ' ' + ll[2] + ' ' + ll[3] + rule(ll[4], True) for ll in l]))

    open(fn_json, 'wb').write(json.dumps(l))
    #for (i, j) in sorted(list(set([(ll[0][:3], ll[1] + ' ' + ll[2]) for ll in l]))):
    #    print(j)

    #p1 = ur'^(單|雙)?(\d+(號|巷|弄)|\d+之\d+(號|巷|弄))以(上|下)$'
    #p2 = ur'^(單|雙)?(\d+(號|巷|弄)|\d+之\d+(號|巷|弄))至(\d+(號|巷|弄)|\d+之\d+(號|巷|弄))(含附號)?(全)?$'
    #p3 = ur'^(\d+(號|巷|弄)|\d+之\d+(號|巷|弄))((單|雙)?全|含附號)?$'
    #p4 = ur'^(單|雙)$'
    #p5 = ur'^\d+之\d+至之\d+(號|巷|弄)$'
    #p6 = ur'^\d+(號|巷|弄)(單|雙|連)?(\d+(號|巷|弄)|\d+之\d+號)(以(上|下)|(單|雙)?全)?$'
    #p7 = ur'^\d+(號|巷|弄)(單|雙|連)?(\d+(號|巷|弄)|\d+之\d+(號|巷|弄))至(\d+(號|巷|弄)|\d+之\d+(號|巷|弄))$'
    #p8 = ur'^\d+號(\d+樓|\d+至\d+樓|\d+樓以(上|下))$'
    #p9 = ur'^\d+附號全$'
    #p10 = ur'^\d+巷\d+弄(單|雙|連)\d+號以(上|下)$'
    #p11 = ur'^\d+號（'
    #t1 = re.compile(p1)
    #t2 = re.compile(p2)
    #t3 = re.compile(p3)
    #t4 = re.compile(p4)
    #t5 = re.compile(p5)
    #t6 = re.compile(p6)
    #t7 = re.compile(p7)
    #t8 = re.compile(p8)
    #t9 = re.compile(p9)
    #t10 = re.compile(p10)
    #t11 = re.compile(p11)
    #l0 = [ll for ll in l if rule(ll[4])]
    #l1 = [ll for ll in l0 if t1.match(rule(ll[4]))]
    #l2 = [ll for ll in l0 if t2.match(rule(ll[4]))]
    #l3 = [ll for ll in l0 if t3.match(rule(ll[4]))]
    #l4 = [ll for ll in l0 if t4.match(rule(ll[4]))]
    #l5 = [ll for ll in l0 if t5.match(rule(ll[4]))]
    #l6 = [ll for ll in l0 if t6.match(rule(ll[4]))]
    #l7 = [ll for ll in l0 if t7.match(rule(ll[4]))]
    #l8 = [ll for ll in l0 if t8.match(rule(ll[4]))]
    #l9 = [ll for ll in l0 if t9.match(rule(ll[4]))]
    #l10 = [ll for ll in l0 if t10.match(rule(ll[4]))]
    #l11 = [ll for ll in l0 if t11.match(rule(ll[4]))]
    #print(len(l1), len(l2), len(l3), len(l4), len(l5), len(l6), len(l7), len(l8), len(l9), len(l10))
    #s0 = set(l0) - set(l1) - set(l2) - set(l3) - set(l4) - set(l5) - set(l6) - set(l7) - set(l8) - set(l9) - set(l10) - set(l11)
    #L = sorted(list(s0)) 
    #codecs.open('/home/cytu/Downloads/remains.txt', 'w', 'utf-8').write('\n'.join([ll[0] + '   ' + ll[1] + ' ' + ll[2] + ' ' + ll[3] + rule(ll[4], True) for ll in L]))
    #sys.exit()
    
    sys.exit()
    cn = sqlite3.connect(':memory:')
    cr = cn.cursor()

    def create_ix(t, i):
        cr.execute('create index ix_%s_%s on %s(%s)' % (t, i, t, i))

    cr.execute('''create table zip (id integer primary key,
                                    city text not null,
                                    area text not null,
                                    road text not null, 
                                    unique(city, area, road))''')
    for s in ['city', 'area', 'road']:
        create_ix('zip', s)

    cr.executemany('insert into zip (city, area, road) values (?, ?, ?)', l)
    
    d = {}
    zips = Element('zip')
    for r0 in cr.execute('select distinct city from zip order by city').fetchall():
        t0 = r0[0]
        city = SubElement(zips, 'city')
        city.text = t0
        d[t0] = []
        for r1 in cr.execute('select distinct area from zip where city = ? order by area', (t0,)).fetchall():
            t1 = r1[0]
            area = SubElement(city, 'area')
            area.text = t1
            d[t0].append(t1)
            d[t0 + '/' + t1] = []
            for r2 in cr.execute('select distinct road from zip where city = ? and area = ? order by road', (t0, t1)).fetchall():
                t2 = r2[0]
                road = SubElement(area, 'road')
                road.text = t2
                d[t0 + '/' + t1].append(t2)

    #codecs.open(fn_zip, 'w', 'utf-8').write(prettify(zips))
    #open(fn_json, 'wb').write(json.dumps(d))

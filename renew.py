# -*- coding: utf-8 -*-

import os, sys, subprocess, urllib2, re, fnmatch, tempfile, sqlite3, time, codecs
from shutil import copyfile, rmtree
from operator import itemgetter

os.chdir(os.path.dirname(__file__))
cat = os.path.join

tmp = 'tmp'
nhi = 'http://www.nhi.gov.tw'

from bs4 import BeautifulSoup

def log(t):
    print t

def zh(t):
    h = ''
    if t == 'ord':
        h = u'處置'

    elif t == 'med': 
        h = u'藥品'
    
    elif t == 'mat':
        h = u'特殊材料'
    
    elif t == 'hosp':
        h = u'醫療院所'

    return h

def download(td, t):
    if t == 'ord':
        wid = 3633 
        q = ur'支付標準壓縮檔\(NHI Fee Schedule\)\(\.txt\)'

    elif t == 'med':
        wid = 873
        q = u'查詢檔--'
    
    elif t == 'mat':
        wid = 4745 
        q = u'txt檔'
    
    elif t == 'hosp':
        wid = 660
        q = ur'健保特約醫療院所名冊壓縮檔'

    arc = cat(td, 'tmp.exe')
    log(u'\n下載最新%s壓縮檔中，請稍候...' % zh(t))
    url = nhi + '/webdata/webdata.aspx?webdata_id=%s' % wid
    try:
        src = BeautifulSoup(urllib2.urlopen(url), 'html.parser')
    except:
        log(u'無法下載%s，請查看%s版面是否移除，或檢查網路連線！' % (zh(t), zh(t)))
        import webbrowser
        webbrowser.open(url)
        return 0
    
    all_li = src.find_all(string=re.compile(q))
    for i in all_li:
        a = i.find_next('a')
        open(arc, 'wb').write(urllib2.urlopen(nhi + a['href']).read())
        break

    log(u'%s壓縮檔下載成功，解壓縮中...' % zh(t))
    subprocess.call(['c:/Program Files/7-Zip/7z.exe' if os.name == 'nt' else '7z', 
                     'e', arc, '-o%s' % td, '-aoa'])
    return 1

def list_new(typ):
    l = []
    td = tempfile.mkdtemp(dir=tmp)
    r = download(td, typ)
    if not r:
        cls(td)
        return l

    if typ == 'ord':
        for i in os.listdir(td):
            if fnmatch.fnmatch(i, 'MHCT_PAYITEM_*'):
                target = i
                break

        for ll in open(cat(td, target), 'r'):
            s = [g.decode('utf-8', 'ignore').strip() for g in ll.split('^')][:-1]
            #s[1] = int(s[1])
            for i in (2, 3):
                s[i] = str(int(s[i][:4]) - 1911).zfill(3) + s[i][4:]
            # XXX swap s[4] and s[5] for uniformization of db table listings
            #     id - code - name - name_en >> id - code - name_en - name
            s4 = s[4]
            s5 = s[5]
            s[4] = s5
            s[5] = s4
            l.append(tuple(s))

    elif typ == 'mat':
        # ========================================================================
        # 健保特殊材料品項欄位格式說明(105.05.24更新)
        #
        #    欄位名稱          起   迄
        #1   特材代碼          2    13      code
        #2   中英文品名        17   161     name
        #3   產品型號/規格     165  1162    model
        #4   單位              1168 1175    unit
        #5   支付點數          1179 1188
        #6   生效日期          1192 1201
        #7   事前審查生效日期  1205 1214    exam_effective_date
        #8   事前審查          1218 1221    exam
        #9   給付規定代碼      1225 1231    payment_code
        #10  生效迄日          1235 1244    
        #11  申請者簡稱        1248 1267    applier
        #12  衛生署許可證字號  1271 1390    allowance_code
        # ========================================================================

        for i in os.listdir(td):
            if fnmatch.fnmatch(i, '*.txt'):
                target = i
                break
        
        for n, i in enumerate(open(cat(td, target), 'r')):
            if n > 3: # only started at line 5....
                li = [i[1:13], i[16:161], i[164:1162], i[1167:1175], 
                      i[1178:1188], i[1191:1201], i[1204:1214], i[1217:1221], 
                      i[1224:1231], i[1234:1244], i[1247:1267], i[1270:1390],]
                s = [g.decode('big5', 'ignore').strip() for g in li]
                #s[4] = float(s[4])
                s[7] = u'N' if not s[7] else s[7] # idiot g8s...
                s[8] = '' if s[8] == u'無' else s[8]
                for g in (5, 6, 9):
                    s[g] = s[g].replace('/', '')
                l.append(tuple(s))

    elif typ == 'med':
        # =======================================================================
        #               健保用藥品項查詢檔欄位格式說明
        #
        #序號 欄位中文名稱                 屬性  長度   起始   迄末
        #1    New_mark                     C        2      1      2  mark_new
        #2    口服錠註記                   C       10      4     13  mark_internal
        #3    單/複方註記                  C        2     15     16  mark_complex
        #4    藥品代碼                     C       10     18     27  code
        #5    藥價參考金額                 N      9,2     29     37  price
        #6    藥價參考日期                 D        7     39     45  valid_from
        #7    藥價參考截止日期             D        7     47     53  valid_till
        #8    藥品英文名稱                 C      120     55    174  name
        #9    藥品規格量                   N      7,2    176    182  spec_amount
        #10   藥品規格單位                 C       52    184    235  spec_unit
        #11   成份名稱                     C       56    237    292  content_name
        #12   成份含量                     N     12,3    294    305  content_amount
        #13   成份含量單位                 C       51    307    357  content_unit
        #14   藥品劑型                     C       18    359    376  med_type
        #15   空白                         C        6    378    383  
        #16   空白                         C       60    385    444
        #17   空白                         C      158    446    603
        #18   藥商名稱                     C       20    605    624  vendor
        #19   空白                         C      141    626    766  
        #20   藥品分類                     C        1    768    768  med_class
        #21   品質分類碼                   C        1    770    770  quality_code
        #22   藥品中文名稱                 C      128    772    899  name_zh
        #23   分類分組名稱                 C      300    901   1200  class_group
        #24   （複方一）成份名稱           C       56   1201   1256  content1
        #25   （複方一）藥品成份含量       N     11,3   1259   1269  content_amount1
        #26   （複方一）藥品成份含量單位   C       51   1271   1321  content_unit1
        #27   （複方二）成份名稱           C       56   1323   1378  content2
        #28   （複方二）藥品成份含量       N     11,3   1380   1390  content_amount2
        #29   （複方二）藥品成份含量單位   C       51   1392   1442  content_unit2
        #30   （複方三）成份名稱           C       56   1444   1499  content3
        #31   （複方三）藥品成份含量       N     11,3   1501   1511  content_amount3
        #32   （複方三）藥品成份含量單位   C       51   1513   1563  content_unit3
        #33   （複方四）成份名稱           C       56   1565   1620  content4
        #34   （複方四）藥品成份含量       N     11,3   1622   1632  content_amount4
        #35   （複方四）藥品成份含量單位   C       51   1634   1684  content_unit4
        #36   （複方五）成份名稱           C       56   1686   1741  content5
        #37   （複方五）藥品成份含量       N     11,3   1743   1753  content_amount5
        #38   （複方五）藥品成份含量單位   C       51   1755   1805  content_unit5
        #39   製造廠名稱                   C       42   1807   1848  manufacturer
        #40   ATC CODE                     C        8   1850   1857  atc_code
        #========================================================================

        all_b5 = [i for i in os.listdir(td) if fnmatch.fnmatch(i, '*.b5')]    
        for b5 in all_b5:
            for i in open(cat(td, b5), 'r'):
                li = [i[0:2], i[3:13], i[14:16], i[17:27], i[28:37], i[38:45], i[46:53], i[54:174], i[175:182], i[183: 235], i[236:292], i[293:305], i[306:357], i[358:376], i[377:383], i[384:444], i[445:603], i[604:624], i[625:766], i[767:768], i[769:770], i[771:899], i[900:1200], i[1200:1256], i[1258:1269], i[1270:1321], i[1322:1378], i[1379:1390], i[1391:1442], i[1443:1499], i[1500:1511], i[1512:1563], i[1564:1620], i[1621:1632], i[1633:1684], i[1685:1741], i[1742:1753], i[1754:1805], i[1806:1848], i[1849:1857],]
                s = [g.decode('big5', 'ignore').strip() for g in li]
                for k in (4, 8, 11, 24, 27, 30, 33):
                    #s[k] = float(s[k]) if s[k] else 0.0
                    s[k] = str(s[k]) if s[k] else str(0)
                l.append(tuple(s))
    
    elif typ == 'hosp':

        ##0   分局別
        ##1   醫事機構代碼	
        ##2   醫事機構名稱
        ##3   機構地址
        ##4   電話區域號碼
        ##5   電話號碼
        ##6   特約類別

        d = {
        '1': '醫學中心',
        '2': '區域醫院',
        '3': '地區醫院',
        '4': '診所',
        '5': '藥局',
        '6': '居家護理',
        '7': '康復之家',
        '8': '助產所',
        '9': '檢驗所',
        'A': '物理治療所',
        'B': '特約醫事放射機構',
        'X': '不詳',
        }
        ##7   型態別
        ##8   醫事機構種類
        ##9   終止合約或歇業日期

        for i in os.listdir(td):
            if fnmatch.fnmatch(i, 'hospbsc*'):
                target = i
                break

        for n, i in enumerate(open(cat(td, target), 'r')):
            if n > 0: # only started at line 2....
                s = [g.decode('big5', 'ignore').strip().replace('"', '') for g in i.split(',')]
                l.append(tuple(s))
    rmtree(td)
    return l 

def create_new(t, cr):
    def create_ix(t, i):
        cr.execute('create index ix_%s_%s on %s(%s)' % (t, i, t, i))

    start_time = time.time()
    print('now start collecting table %s data ...' % t)
    l = list_new(t)
    print('completed collecting %s: %f seconds.' % (t, time.time() - start_time,))
    cr.execute('select * from %s limit 0' % (t,))
    nl = [desc[0] for desc in cr.description][1:]
    start_time = time.time()
    print('now start creating table %s ...' % t)
    if t == 'med':
        #sql = 'insert into %s (%s) values (%s)' % (t, ', '.join(nl), ', '.join(['?'] * len(nl)))
        #sql = sql.replace('?', '%s')
        #cr.executemany(sql, sorted(list(set([(ll[3],) + ll[7:14] + (ll[17], ll[19]) + ll[20:40] for ll in l])))) 
        ll_ = sorted(list(set([(ll[3],) + ll[7:14] + (ll[17], ll[19]) + ll[20:40] for ll in l])))
        ll_ = [[i.replace('\t', ' ') for i in ll] for ll in ll_]
        codecs.open(t, 'wb','utf-8').write('\n'.join(['\t'.join(ll) for ll in ll_]))

        start_time0 = time.time()
        print('now start copying %s ...' % t)
        cr.copy_from(codecs.open(t, 'rb', 'utf-8'), t, columns=tuple(nl))
        print('completed copying %s. elapsed: %f seconds.' % (t, time.time() - start_time0))
        for i in ['code', 'name']:
            create_ix(t, i)
        dd = {}
        cr.execute('select * from %s' % t)
        for r in cr.fetchall():
            dd[r[1]] = str(r[0])

        start_time0 = time.time()
        print('now start constructing %s related effect...' % t)
        # can't just use executemany to avoid duplicates
        for eff_date in sorted(list(set([(ll[5],) for ll in l]))):
            cr.execute('select * from effect where effective_date = %s', eff_date)
            r = cr.fetchone()
            if not r:
                cr.execute('insert into effect (effective_date) values (%s)', 
                            eff_date)
        print('completed constructing %s related effect. elapsed: %f seconds.' % (t, time.time() - start_time))

        dd1= {}
        cr.execute('select * from effect')
        for r in cr.fetchall():
            dd1[r[1]] = str(r[0])

        #sql = 'insert into %s_effect(%s_id, effect_id, price) values((select id from %s where code = ?), (select id from effect where effective_date = ?), ?)' % (t, t, t)
        #sql = sql.replace('?', '%s')
        #cr.executemany(sql, [(ll[3], ll[5], ll[4]) for ll in l])
        start_time0 = time.time()
        print('now start constructing %s_effect...' % t)
        list_effect = []
        for ll in l:
            iid = dd[ll[3]]
            effect_id = dd1[ll[5]]
            list_effect.append((iid, effect_id, ll[4]))
        codecs.open('%s_effect' % t, 'wb', 'utf-8').write('\n'.join(['\t'.join(ll) for ll in list_effect]))
        cr.copy_from(codecs.open('%s_effect' % t, 'rb', 'utf-8'), '%s_effect' % t)
        print('completed constructing %s_effect. elapsed: %f seconds.' % (t, time.time() - start_time0))

    elif t == 'ord':
        #sql = 'insert into %s (%s) values (%s)' % (t, ', '.join(nl), ', '.join(['?'] * len(nl)))
        #sql = sql.replace('?', '%s')
        #cr.executemany(sql, sorted(list(set([(ll[0],) + ll[4:] for ll in l]))))
        ll_ = sorted(list(set([(ll[0],) + ll[4:] for ll in l])))
        ll_ = [[i.replace('\t', ' ') for i in ll] for ll in ll_]
        codecs.open(t, 'wb','utf-8').write('\n'.join(['\t'.join(ll) for ll in ll_]))
         
        start_time0 = time.time()
        print('now start copying %s ...' % t)
        cr.copy_from(codecs.open(t, 'rb', 'utf-8'), t, columns=nl)
        print('completed copying %s. elapsed: %f seconds.' % (t, time.time() - start_time0))
        for i in ['code',]:
            create_ix(t, i)

        dd = {}
        cr.execute('select * from %s' % t)
        for r in cr.fetchall():
            dd[r[1]] = str(r[0])

        start_time0 = time.time()
        print('now start constructing %s related effect...' % t)
        for eff_date in sorted(list(set([(ll[2],) for ll in l]))):
            cr.execute('select * from effect where effective_date = %s', eff_date)
            r = cr.fetchone()
            if not r:
                cr.execute('insert into effect (effective_date) values (%s)', 
                           eff_date)
        print('completed constructing %s related effect. elapsed: %f seconds.' % (t, time.time() - start_time0,))
        
        dd1 = {}
        cr.execute('select * from effect')
        for r in cr.fetchall():
            dd1[r[1]] = str(r[0])

        #sql = 'insert into %s_effect(%s_id, effect_id, price) values((select id from %s where code = ?), (select id from effect where effective_date = ?), ?)' % (t, t, t)
        #sql = sql.replace('?', '%s')
        #cr.executemany(sql, [(ll[0], ll[2], ll[1]) for ll in l])
        start_time0 = time.time()
        print('now start constructing %s_effect...' % t)
        list_effect = []
        for ll in l:
            iid = dd[ll[0]]
            effect_id = dd1[ll[2]]
            list_effect.append((iid, effect_id, ll[1]))
        codecs.open('%s_effect' % t, 'wb', 'utf-8').write('\n'.join(['\t'.join(ll) for ll in list_effect]))
        cr.copy_from(codecs.open('%s_effect' % t, 'rb', 'utf-8'), '%s_effect' % t)
        print('completed constructing %s_effect. elapsed: %f seconds.' % (t, time.time() - start_time0))

    elif t == 'mat':
        #sql = 'insert into %s (%s) values (%s)' % (t, ', '.join(nl), ', '.join(['?'] * len(nl)))
        #sql = sql.replace('?', '%s')
        #cr.executemany(sql, sorted(list(set([ll[:4] + ll[10:] for ll in l]))))
        ll_ = sorted(list(set([ll[:4] + ll[10:] for ll in l])))
        ll_ = [[i.replace('\t', ' ') for i in ll] for ll in ll_]
        codecs.open(t, 'wb','utf-8').write('\n'.join(['\t'.join(ll) for ll in ll_]))
        start_time0 = time.time()

        print('now start copying %s ...' % t)
        cr.copy_from(codecs.open(t, 'rb', 'utf-8'), t, columns=tuple(nl))
        print('completed copying %s. elapsed: %f seconds.' % (t, time.time() - start_time0))
        
        for i in ['code', 'name']:
            create_ix(t, i)
        dd = {}
        cr.execute('select * from %s' % t)
        for r in cr.fetchall():
            dd[r[1]] = str(r[0])

        start_time0 = time.time()
        print('now start constructing %s related effect...' % t)
        for eff_date in sorted(list(set([(ll[5],) for ll in l] + [(ll[6],) for ll in l]))):
            cr.execute('select * from effect where effective_date = %s', eff_date)
            r = cr.fetchone()
            if not r:
                cr.execute('insert into effect (effective_date) values (%s)', 
                           eff_date)
        print('completed constructing %s related effect. elapsed: %f seconds.' % (t, time.time() - start_time0,))

        dd1 = {}
        cr.execute('select * from effect')
        for r in cr.fetchall():
            dd1[r[1]] = str(r[0])

        #sql = 'insert into %s_effect (%s_id, effect_id, effect_exam_id, price, exam, payment_code) values((select id from %s where code = ?), (select id from effect where effective_date = ?), (select id from effect where effective_date = ?), ?, ?, ?)' % (t, t, t)
        #sql = sql.replace('?', '%s')
        #cr.executemany(sql, [(ll[0], ll[5], ll[6], ll[4], ll[7], ll[8]) for ll in l])
        start_time0 = time.time()
        print('now start constructing %s_effect...' % t)
        list_effect = []
        for ll in l:
            iid = dd[ll[0]]
            effect_id = dd1[ll[5]]
            effect_exam_id = dd1[ll[6]]
            list_effect.append((iid, effect_id, effect_exam_id, ll[4], ll[7], ll[8]))
        codecs.open('%s_effect' % t, 'wb', 'utf-8').write('\n'.join(['\t'.join(ll) for ll in list_effect]))
        cr.copy_from(codecs.open('%s_effect' % t, 'rb', 'utf-8'), '%s_effect' % t)
        print('completed constructing %s_effect. elapsed: %f seconds.' % (t, time.time() - start_time0))

    print('insert into %s: %f seconds.' % (t, time.time() - start_time,))

def update(t, cr, l):
    err_n = 0
    cr.execute('select * from %s limit 0' % (t,))
    nl = [desc[0] for desc in cr.description][1:]
    if t == 'med':
        l = sorted(l, key=itemgetter(3, 5))
        for ll in l:
            code = ll[3]
            cr.execute('select id from med where code = %s', (code,))
            r = cr.fetchone()
            if r:
                med_id = r[0]
            else:
                sql = 'insert into med (%s) values (%s) returning id' % (', '.join(nl), ', '.join(['?'] * len(nl)))
                sql = sql.replace('?', '%s')
                cr.execute(sql, (ll[3],) + ll[7:14] + (ll[17], ll[19]) + ll[20:40])
                med_id = cr.fetchone()[0]

            effective_date = ll[5]
            cr.execute('select id from effect where effective_date = %s',
                           (effective_date,))
            r = cr.fetchone()
            if r:
                effect_id = r[0]
            else:
                cr.execute('insert into effect (effective_date) values(%s) returning id', (effective_date,))
                effect_id = cr.fetchone()[0]
        
            cr.execute('select * from med_effect where med_id = %s and effect_id = %s', (med_id, effect_id))
            r = cr.fetchone()
            if not r:
                cr.execute('insert into med_effect (med_id, effect_id, price) values (%s, %s, %s)', (med_id, effect_id, ll[4]))
    
    return err_n

def renew(cn):
    cr = cn.cursor()

    log(u'開始資料庫更新作業！')
    for t in ['med',]:#'ord', 'med']:
        zht = zh(t)
        l = list_new(t)
        if not l:
            log(u'無法更新%s資料，請檢查！' % zht)
            return False

        log(u'更新%s資料中，請稍候...' % zht)
        err_n = update(t, cr, l)
        if err_n:
            log(u'%s資料更新錯誤；錯誤項目請參照 tmp/error_%s.txt！' % (zht, t))
            return False

    try:
        cn.commit()
        return True
    
    except:
        cn.rollback()
        log(u'發生錯誤，本機資料庫無法更新！')
        return False

if __name__ == '__main__':
    
    td = tempfile.mkdtemp(dir=tmp)
    db = 'mycis.db'
    
    # working on db copy
    dbc = cat(td, 'mycis_c.db')
    copyfile(db, dbc)
    
    # make a copy of mycis.db
    dbi = cat(td, 'mycis_i.db')
    copyfile(db, dbi) 
    
    # make a copy of res/db/mycis.db
    dbr_ = cat('res', 'db', db)
    dbr = cat(td, 'mycis_r.db')
    copyfile(dbr_, dbr)

    cn = sqlite3.connect(dbc)
    cr = cn.cursor()
    
    b = False
    if renew(cn):
        cr.execute('vacuum')
        cn.commit()
        from backup import backup_remote_all
        if backup_remote_all(dbc):
            try:
                copyfile(dbc, db)
                copyfile(dbc, dbr_)
                log(u'本機資料庫更新完畢！')
                b = True

            except:
                try:
                    log(u'本機資料庫更新錯誤，回復原始資料庫中...')
                    copyfile(dbi, db)
                    copyfile(dbr, dbr_)
                    log(u'本機資料庫回復成功，請檢查！')
                    b = True

                except:
                    log(u'本機資料庫回復失敗，相關檔案儲存在 %s 資料夾！' % td)
    else:
        b = True

    if b:
        cn.close()
        rmtree(td)

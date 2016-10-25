# -*- coding: utf-8 -*-

import os, sqlite3, codecs, sys, shutil, time, datetime, re
from bisect import bisect
from collections import defaultdict
try:
    import simplejson as json
except:
    import json
import passlib

os.chdir(os.path.dirname(__file__))
cat = os.path.join

import psycopg2
import psycopg2.extensions
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

cn = psycopg2.connect(database='mycis', user='mycis', password='mycis') 
cr = cn.cursor()

def dt_now():
    return datetime.datetime.now()

def dt_tw(dt, date_only=False):
    s = str(dt.year - 1911).zfill(3) + dt.strftime('%m%d%H%M%S')
    return s[:7] if date_only else s

def now():
    return dt_tw(dt_now())

db_visw = 'visw.db'
cn_visw = sqlite3.connect(db_visw)
cr_visw = cn_visw.cursor()

# co01m 病患資料
# co02h 主訴 
# co02m 醫令簽章
# co02p 醫令
# co03i IC卡序號、sam、掛號簽章
# co05o 診斷
# co09d 藥代
# co11a 套餐

print('constructing sam ...')
# sam
cr.executemany('insert into sam (code) values (%s)', [r for r in cr_visw.execute('select distinct isam from co03i order by isam').fetchall()])

# staff XXX should import from vis00: vname, vidno
from passlib.hash import sha512_crypt
encrypt = sha512_crypt.encrypt
verify = sha512_crypt.verify

print('constructing staff ...')
cr.executemany('insert into staff (pid, name, pwd) values (%s, %s, %s)',
               [('R220154944', u'魏筱筠', encrypt('101'),),
                ('R220847686', u'張維珊', encrypt('DR'),),
                ('BC00070935', u'鄭義銅', encrypt('102'),),
                ('E220076712', u'李姿儀', encrypt('103'),),
               ])

print('constructing dictionaries for easy lookup ...')
start_time0 = time.time()
# create dictionary for easier lookup
dic_all = defaultdict(dict)
for t in ('sam', 'amend', 'tktype', 'insttype', 'selfpay', 'ocode', 'fee', 'state', 
          'usage', 'freq', 'ord', 'med', 'mat'):
    cr.execute('select code, id from %s' % t)
    for r in cr.fetchall():
        dic_all[t][r[0]] = r[1]

dic_all_inv = defaultdict(dict)
for t in ('ord', 'med', 'mat', 'diag'):
    cr.execute('select code, id from %s' % t)
    for r in cr.fetchall():
        dic_all_inv[t][r[1]] = r[0]

d__ = {}
cr.execute('select code, id from diag')
for r in cr.fetchall():
    d__[r[0]] = r[1] 

print('completed dic_all, dic_inv. elapsed: %f seconds.' % (time.time() - start_time0,))

print('constructing icd9/10 dictionaries ...')
start_time0 = time.time()
# old diags are in icd9 => icd10 => id
data = [[ll.strip().replace('"', '') for ll in l.split('\t')] for l in codecs.open(cat('txt', 'diag.txt'), 'r', 'utf-8')]
d_icd9_to_icd10 = defaultdict(list)

icd9s = {}
for d in data:
    icd9s[d[0].replace('.', '')] = d[0]
icd10s = {}
for d in data:
    icd10s[d[3].replace('.', '')] = d[3]

for d in data:
    d_icd9_to_icd10[d[0]].append(d[3])

for icd9 in d_icd9_to_icd10.keys():
    dic_all['diag'][icd9] = d__[d_icd9_to_icd10[icd9][0]]

dic_diag = {}
for k in list(set([d[3] for d in data])):
    dic_diag[k] = d__[k] 
dic_diag_name = dict(list(set([(d[0], d[2]) for d in data])))

def icd_corrected(c):
    allnum = '0123456789'

    # normal lookup
    if c in icd9s:
        return 1, c, icd9s[c]

    elif c in icd10s:
        return 2, c, icd10s[c]

    else:
        # add some characters to search
        if len(c) in (3, 4):
            for s in allnum:
                cc = c + s
                if cc in icd9s:
                    return 1, cc, icd9s[cc]

                elif cc in icd10s:
                    return 2, cc, icd10s[cc]
                
                else:
                    for ss in allnum:
                        ccc = cc + s
                        if ccc in icd9s:
                            return 1, ccc, icd9s[ccc]
                        elif ccc in icd10s:
                            return 2, ccc, icd10s[ccc]

        return 0, c, '' 
print('completed icd9/10 dictionaries. elapsed: %f seconds.' % (time.time() - start_time0,))

dic_price = json.loads(open(cat('..', 'cache', 'dic_price.json'), 'rb').read())
def get_price(typ, code, dt): 
    d = dic_price[typ][code]
    # XXX ord has no complete pricing history!
    return d['price'][bisect(d['effective_date'],'1051001' if typ == 'ord' else dt)]

# ((u'["", "2", "", "3"]',   u'一般處置'),
# (u'["", "3", "", "4"]',    u'特殊材料'),
# (u'["0", "1", "01", "1"]', u'院所自調之藥品'),
# (u'["0", "1", "05", "2"]', u'院所自調之連續處方籤'),
# (u'["1", "4", "02", "1"]', u'處方釋出之藥品或檢驗'),
# (u'["1", "4", "06", "2"]', u'處方釋出之連續處方籤'),
# (u'["2", "2", "02", "1"]', u'病理'),
# (u'["self", "", "", ""]',  u'自費'),
# (u'["free", "", "", ""]',  u'贈送'),

def ocode_def(code, typ='', is_cont=False, b_ph=True):
    BIOPSY = ('25001C', '25002C', '25003C', '25004C', '25024C', '25025C')
    if not typ: 
        nc = len(code)
        if nc == 2 or nc == 6 or code in ('21+L1001C', '25+L1001C'):
            typ = 'ord'
        elif nc == 12:
            typ = 'mat'
        elif nc == 10:
            typ = 'med'
        else:
            typ = 'none'

    if typ == 'ord':
        if code in BIOPSY:
            return (u'2', u'2', u'02', u'1')
        elif '19001C' <= code <= '19018C' and len(code) == 6: # echo
            return (u'', u'2', u'', u'3')
        elif '06001C' <= code <= '36021C' and len(code) == 6:
            return (u'1', u'4', u'02', u'1')
        return (u'', u'2', u'', u'3')

    elif typ == 'med':
        if b_ph: # 藥劑師本院調劑
            if is_cont:
                return (u'0', u'1', u'05', u'2')
            return (u'0', u'1', u'01', u'1')
        else:    # 釋出處方
            if is_cont:
                return (u'1', u'4', u'06', u'2')
            return (u'1', u'4', u'02', u'1')
    
    elif typ == 'mat': 
        return (u'', u'3', u'', u'4')

    else:
        return (u'self', '', '', '')

start_time = time.time()
print(u'insert into favs ...')
d_kdrug = {}
shortcuts = cr_visw.execute('select distinct kdrug, ddesc, dno, dlmu, dfreq, ddays from co09d where kdrug in (select distinct kdrug from co02p) order by kdrug').fetchall()
for sh in shortcuts:
    kdrug, ddesc, dno, dlmu, dfreq, ddays = sh

    typ = 'none'
    len_dno = len(dno)
    if len_dno == 12: # mat
        typ = 'mat' 
    
    elif len_dno == 10: # med
        typ = 'med' 
   
    elif len_dno == 2: # 預防保健
        typ = 'ord'

    elif len_dno == 6 or dno in ['21+L1001C', '25+L1001C']: 
        if re.match(r'\d{5}[ABCabc]', dno): # ord
            if dno[-1].lower() in ['a', 'b']:
                continue
            typ = 'ord' 
    
    percent = 100
    if re.match(r'^(\d|[ .])+$', dlmu):
        dlmu = dlmu.strip()
        if dlmu:
            l_dlmu = [l.strip() for l in dlmu.split('.') if l.strip()]
            if l_dlmu[0] in ['53', '66', '67']:
                percent += int(l_dlmu[0])
    
    code = dno

    # create fav
    cr.execute('''insert into fav (code, name, staff_id) values (%s, %s, %s) 
                  returning id''', (kdrug.lower(), ddesc, 1))
    fav_id = cr.fetchone()[0]

    if typ in ['ord', 'med', 'mat']:
        ocode_id = dic_all['ocode'].get(json.dumps(ocode_def(code, typ)))
        #if get_price(typ, code, dt) > 0.01:
        iid = dic_all[typ][code]
        if typ == 'med':
            usage_id = dic_all['usage'].get('PO')

            freq_id = dic_all['freq'].get(dfreq, 0)
            if not freq_id:
                freq_id = dic_all['freq'].get('BID')

            days = int(ddays) if ddays else 3 
            dosage = 1
            cr.execute('insert into fav_med values (%s, %s, %s, %s, %s, %s, %s)',
                        (fav_id, iid, usage_id, freq_id, ocode_id, days, dosage))
        else:
            sql = 'insert into fav_%s values (?, ?, ?, ?, ?)' % (typ,)
            sql = sql.replace('?', '%s')
            cr.execute(sql, (fav_id, iid, ocode_id, percent, 1))

        d_kdrug[kdrug.lower()] = [typ + '_' + str(iid), code]
        
    else:
        pass
        
d_amp = {}
for s in [str(i) for i in range(11, 100)]:
    if s in ('11', '12', '13', '15', '16', '17', '19', 
             '71', '72', '73', '75', '76', '77', '79'):
        h = 'V202' 
    elif s in [str(i) for i in range(41, 61)]:
        h = 'V221' 
    elif s in ['31', '35', '37']:
        h = 'V762' 
    elif s in ['91', '93']:
        h = 'V7612'
    elif s in ['85']:
        h = 'V7651'
    elif s in ['95', '97']:
        h = 'V7642'
    elif s in ['21', '22', '23', '24']:
        h = 'V70'
    else:
        h = ''
    d_amp[s] = h if h else ''

all_diags = []
r = cr_visw.execute('select distinct tacd from co05o').fetchall()
for rr in r:
    diags = [i for i in rr[0].split(',') if i]
    for di in diags:
        if di[0] == '@':
            di1 = di[1:]
            if di1 == '11':
                dii = 'V202'
            elif di1 == '21':
                dii = 'V70'
            elif di1 == '31':
                dii = 'V762'
            elif di1 == '85':
                dii = 'V7651'
            elif di1 == '95':
                dii = 'V7642'
            elif '41' <= di1 <= '60':
                dii = 'V221'
        else:
            dii = di
        all_diags.append(dii)
all_diags = set(all_diags)
diags_ = []
for di in all_diags: 
    result, c_corr, c_orig = icd_corrected(di)
    if result == 1: # just want icd9
        diags_.append(c_orig)

for di in sorted(list(set(diags_))):
    cr.execute('''insert into fav (code, name, staff_id) values (%s, %s, %s)
            returning id''', (di.replace('.', '').lower(), dic_diag_name[di], 1))
    fav_id = cr.fetchone()[0]
    cr.execute('insert into fav_diag (fav_id, diag_id) values (%s, %s)',
            (fav_id, dic_all['diag'][di]))

# note that in this case all kdrugs are in co02p
suites = cr_visw.execute('select distinct asmnm from co11a').fetchall()
for nn, ss in enumerate(suites):
    l = cr_visw.execute('select prmk, kdrug, pfq, pps, pday, ptqty, poqty from co11a where asmnm = ?', ss).fetchall()
    if not l:
        continue
    cr.execute('''insert into fav (code, name, staff_id) values (%s, %s, %s)
                    returning id''', (ss[0].lower(), u'favs ' + str(nn+1), 1))
    fav_id = cr.fetchone()[0]
    for ll in l:
        prmk, kdrug, pfq, pps, pday, ptqty, poqty = ll
        id_ = d_kdrug.get(kdrug.lower(), None)
        if id_:
            typ, iid = id_[0].split('_')
            iid = int(iid)
            ocode_id = dic_all['ocode'].get(json.dumps(ocode_def(id_[1], typ)))
            if typ == 'med':
                usage_id = dic_all['usage'].get(pps, 0)
                if not usage_id:
                    usage_id = dic_all['usage']['PO']
                freq_id = dic_all['freq'].get(pfq, 0)
                if not freq_id:
                    freq_id = dic_all['freq']['BID']
                days = int(pday) if pday else 3 
                dosage = 1
                cr.execute('insert into fav_med values(%s, %s, %s, %s, %s, %s, %s)',
                        (fav_id, iid, usage_id, freq_id, ocode_id, days, dosage))
            else:
                percent = 100
                sql = 'insert into fav_%s values (?, ?, ?, ?, ?)' % (typ,)
                sql = sql.replace('?', '%s')
                cr.execute(sql, (fav_id, iid, ocode_id, percent, 1))

print('favs completed. elapsed: %f seconds' % (time.time() - start_time,))

# patient -> inst -> tk
def create_tk(inst_id=0, name='', pid='', birthday='', addr_code='', tel_code='', card_code='', state_code='3', newborn='', newbornmark='', newbornprobe='', tktype_code='01', amend_code='1', dt='', serial='', sign='', sam_code='', staff_pid_doctor='', staff_pid_pharmacist='', soap='', note=''):    
    sam_id = dic_all['sam'][sam_code]
    amend_id = dic_all['amend'][amend_code] 
    tktype_id = dic_all['tktype'][tktype_code] 
    state_id = dic_all['state'][state_code] 
    
    # patient
    cr.execute('select id from patient where pid = %s', (pid,))
    r = cr.fetchone()
    if r:
        patient_id = r[0]

    else:
        # XXX custom_code generation
        p4 = pid[-4:] 
        cr.execute('''select count(custom_code) from patient 
                      where substr(custom_code, 1, 4) = %s''', (p4,))
        r = cr.fetchone()[0]
        custom_code = p4 + '-' + str(r + 1)
        cr.execute('''insert into patient (pid, name, birthday, custom_code, note) 
                      values (%s, %s, %s, %s, %s) returning id''', 
                        (pid, name, birthday, custom_code, note))
        patient_id = cr.fetchone()[0]

    d = {}
    d['card_code'] = card_code
    d['addr_code'] = addr_code
    d['tel_code'] = tel_code
    # card, addr, tel
    for i in ['card', 'addr', 'tel']:
        sql = 'select id from %s where code = ?' % i
        sql = sql.replace('?', '%s')
        cr.execute(sql, (d['%s_code' % i],))
        r = cr.fetchone()
        if r:
            d['%s_id' % i]  = r[0]
        else:
            sql = 'insert into %s (code) values (?) returning id' % i
            sql = sql.replace('?', '%s')
            cr.execute(sql, (d['%s_code' % i],))
            d['%s_id' % i] = cr.fetchone()[0] 
            sql = '''insert into patient_%s (patient_id, %s_id) 
                     values (?, ?)''' % (i, i)
            sql = sql.replace('?', '%s')
            cr.execute(sql, (patient_id, d['%s_id' % i]))
    # XXX
    staff_id_doctor = 1
    staff_id_pharmacist = 1

    cr.execute('''insert into tk (inst_id,
                                  patient_id,
                                  amend_id,
                                  tktype_id, 
                                  sam_id, 
                                  state_id, 
                                  staff_id_doctor,
                                  staff_id_pharmacist,
                                  card_id, 
                                  newborn, 
                                  newbornmark, 
                                  newbornprobe, 
                                  sign, 
                                  dt, 
                                  serial,
                                  soap) 
          values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                  returning id''',
                                 (inst_id,
                                  patient_id,
                                  amend_id, 
                                  tktype_id, 
                                  sam_id, 
                                  state_id, 
                                  staff_id_doctor,
                                  staff_id_pharmacist,
                                  d['card_id'], 
                                  newborn, 
                                  newbornmark,
                                  newbornprobe, 
                                  sign, 
                                  dt, 
                                  serial, 
                                  soap))
    tk_id = cr.fetchone()[0]
    return tk_id

start_time = time.time()
print('start importing visw data ...')
n_sign, n_duplicate, n_missing, n_empty = 0, 0, 0, 0

tks = cr_visw.execute('select kcstmr, idate, itime, icno, itp, isqno, ierrcd, isam, isgn, isgn2 from co03i').fetchall()[-500:]
for tk in tks:
    kcstmr, idate, itime, card_code, tktype_code, serial, serial_1, sam_code, isgn, isgn2 = tk
    if tktype_code == 'ZB' or itime > '235959':
        continue
    sign = isgn + isgn2
    serial = serial if serial else serial_1
    dt = idate + itime

    # patient
    patient = cr_visw.execute('select mname, mbirthdt, mtelh, mpersonid, mexinx, maddr, mremark from co01m where kcstmr = ?', (kcstmr,)).fetchone()
    name, birthday, tel_code, pid, custom_code, addr_code, note = patient
    note = note.strip()

    # soap
    soap = ''
    r = cr_visw.execute('select stext, sisrs from co02h where kcstmr = ? and sdate = ? and stime = ?', (kcstmr, idate, itime)).fetchone() 
    if r:
        soap = r[0].strip()

    # diag
    diags = []
    r = cr_visw.execute('select tacd from co05o where kcstmr = ? and tbkdate = ? and tbegtime = ?', (kcstmr, idate, itime)).fetchone()
    if r:
        diags = [i for i in r[0].split(',') if i and i[0] != '@' and len(i) > 2] 

    # ord, med, mat
    ords, meds, mats = [], [], []
    pp = cr_visw.execute('''select plm, prmk, kdrug, ptp, pqty, poqty, ptqty, ppr, pdp1, pdp5, pfq, ptfq, pps, pday, ptday, pmu from co02p where kcstmr = ? and pdate = ? and ptime = ?''', (kcstmr, idate, itime)).fetchall()
    #plm: ' ', A, 9, 3, 4, 7
    for p in pp:
        plm, prmk, kdrug, ptp, pqty, poqty, ptqty, ppr, pdp1, pdp5, pfq, ptfq, pps, pday, ptday, pmu = p
        id_ = d_kdrug.get(kdrug.lower(), None)
        if id_:
            typ, iid = id_[0].split('_')
            iid = int(iid)
            code = id_[1]
            ocode_id = dic_all['ocode'].get(json.dumps(ocode_def(code, typ)))
                
            # get sign
            start_t = time.time()
            r_ = cr_visw.execute('''select isgn from co02m 
                where kcstmr = ? and idate = ? and dno = ? and isgn <> "" ''', 
                     (kcstmr, idate, code)).fetchall()
            sign = r_[0][0] if r_ else ''
            if sign:
                n_sign += 1
            nr_ = len(r_)
            if nr_ > 1:
                n_duplicate += 1
                r_ = cr_visw.execute('''select isgn from co02m 
       where kcstmr = ? and idate = ? and itime = ? and dno = ? and isgn <> "" ''', 
                    (kcstmr, idate, itime, code)).fetchall()
                nr_ = len(r_)
                if nr_ > 1:
                    print('duplicated matching ord sign data') 
                elif nr_ == 0:
                    print('no matching ord sign data')
                else:
                    sign = r_[0][0]

            elif nr_ == 0:
                n_missing += 1

            b_in = -1
            if typ == 'med':
                usage_id = dic_all['usage'].get(pps, 0)
                if not usage_id:
                    usage_id = dic_all['usage'].get('PO')
                freq_id = dic_all['freq'].get(pfq, 0)
                if not freq_id:
                    freq_id = dic_all['freq'].get('BID')
                days = int(pday) if pday else 3 
                dosage = 1
                for ii, m in enumerate(meds):
                    if iid == m[0]:
                        b_in = ii 
                        break
                if b_in != -1:
                    #print('got duplicated med')
                    meds[b_in][-3] += days
                else:
                    meds.append([iid, usage_id, freq_id, ocode_id, days, dosage, sign])
            elif typ in ('ord', 'mat'):
                try:
                    percent = int(100 * float(pmu))
                except:
                    percent = 100
                
                if typ == 'ord':
                    for ii, o in enumerate(ords):
                        if iid == o[0]:
                            b_in = ii 
                            break
                    if b_in != -1:
                        print('got duplicated ord')
                        ords[b_in][-2] += 1
                    else:
                        ords.append([iid, ocode_id, percent, 1, sign])
                else:
                    for ii, o in enumerate(mats):
                        if iid == o[0]:
                            b_in = ii 
                            break
                    if b_in != -1:
                        print('got duplicated mat')
                        mats[b_in][-2] += 1
                    else:
                        mats.append([iid, ocode_id, percent, 1, sign])
    
    test_ = [oi[0] for oi in ords if len(dic_all_inv['ord'][oi[0]]) == 2]
    if test_ and not diags:
        diags = [d_amp[dic_all_inv['ord'][oi]] for oi in test_]
    diags = [di for di in diags if di]
    if not (diags and (ords or meds or mats)):
        #print(u'empty cases....')
        n_empty += 1
        continue

    # create inst first: guess work.
    insttype_id = dic_all['insttype'].get('09')
    is_cont = 0
    is_severe = 0

    cr.execute('''insert into inst (insttype_id, is_cont, is_severe) 
            values (%s, %s, %s) returning id''', (insttype_id, is_cont, is_severe))
    inst_id = cr.fetchone()[0]
    
    newborn, newbornmark, newbornprobe = '', '', '' 
    state_code = '3'
    amend_code = '1'

    # having collected all tk data, now insert into new database.
    # tk
    tk_id = create_tk(inst_id=inst_id, name=name, pid=pid, birthday=birthday, addr_code=addr_code, tel_code=tel_code, card_code=card_code, state_code=state_code, newborn=newborn, newbornmark=newbornmark, newbornprobe=newbornprobe, tktype_code=tktype_code, amend_code=amend_code, dt=dt, serial=serial, sign=sign, sam_code=sam_code, soap=soap, note=note)#staff_pid_doctor='', staff_pid_pharmacist='')

    # tk_fee
    #cr.executemany('''insert into tk_fee (tk_id, fee_id, qty) 
    #                  values (%s, %s, %s)''',
    #              [(tk_id, dic_all['fee'][fi[0]], fi[1]) for fi in fees])
    
    # test over diags to see if all diags can be translated;
    diags_ = []
    for di in diags: # only icd9 64503(645.03) post-term pregnancy can't be detected
        result, c_corr, c_orig = icd_corrected(di)
        if result == 0:
            print('icd that cannot be translated: %s' % di) 

        elif result == 1: #icd9
            diags_.append((tk_id, dic_all['diag'][c_orig])) 

        elif result == 2: #icd10
            diags_.append((tk_id, dic_diag[c_orig]))
     
    l_unique = sorted(list(set(diags_)))
    #if len(diags_) != len(l_unique):
    #    print('original icd9s: ', diags)
    #    print(diags_, l_unique)

    # tk_diag
    if l_unique:
        cr.executemany('insert into tk_diag (tk_id, diag_id) values (%s, %s)', 
                       l_unique)

    # tk_ord
    cr.executemany('''insert into tk_ord 
                      (tk_id, ord_id, ocode_id, percent, qty, sign) 
                      values (%s, %s, %s, %s, %s, %s)''', 
                    [tuple([tk_id,] + oi) for oi in ords])
    
    # tk_med
    cr.executemany('''insert into tk_med 
                    (tk_id, med_id, usage_id, freq_id, ocode_id, days, dosage, sign)
                      values (%s, %s, %s, %s, %s, %s, %s, %s)''', 
                    [tuple([tk_id,] + mi) for mi in meds])

    # tk_mat
    cr.executemany('''insert into tk_mat 
                      (tk_id, mat_id, ocode_id, percent, qty, sign) 
                      values (%s, %s, %s, %s, %s, %s)''', 
                    [tuple([tk_id,] + ma) for ma in mats])

cn.commit()
print('All Completed!! Elapsed: %f seconds.' % (time.time() - start_time,))
print('n_empty: %s, n_sign: %s, n_duplicate: %s, n_missing: %s' % (n_empty, n_sign, n_duplicate, n_missing))

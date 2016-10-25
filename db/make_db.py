# -*- coding: utf-8 -*-

import os, sqlite3, codecs, sys, shutil, time
os.chdir(os.path.dirname(__file__))
cat = os.path.join

print('start creating new mycis db ...')
start_time = time.time()

import psycopg2
import psycopg2.extensions
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

cn = psycopg2.connect(database='mycis', user='mycis', password='mycis') 
cr = cn.cursor()

sqls_ix = []
def create_ix(t, i, b_ex=False):
    sql = 'create index ix_%s_%s on %s(%s)' % (t, i, t, i)
    if b_ex:
        cr.execute(sql)
    else:
        sqls_ix.append(sql)

#  passlib.hash.sha512_crypt 
#  group: 'admin', 'doctor', 'nurse', 'pharmacist';
for t in ['staff',]:
    sql = '''create table %s (id serial primary key, 
                              pid text not null, 
                              name text not null, 
                              pwd text not null,
                              unique(pid, name))''' % t
    cr.execute(sql)

for t in ['patient',]:
    sql = '''create table %s (id serial primary key, 
                              pid text not null, 
                              name text not null, 
                              birthday text not null,
                              custom_code text not null default '',
                              note text not null default '',
                              unique (pid, name, birthday))''' % t
    cr.execute(sql)
    for i in ['pid', 'birthday']:
        create_ix(t, i)

#for t in ['addr',]:
#    sql = '''create table %s(id serial primary key,
#                             zip_id integer not null, 
#                             code text not null,
#                             foreign key (zip_id) references zip (id),
#                             unique (code))''' % t
#    cr.execute(sql)
#    for i in ['zip_id',]:
#        create_ix(t, i) 
#
#for t in ['zip',]:
#    sql = '''create table %s(id serial primary key,
#                             code text not null, 
#                             name text not null,
#                             unique (code, name))''' % t
#    cr.execute(sql)
#    for i in ['code', 'name']:
#        create_ix(t, i) 

for t in ['addr',]:
    sql = '''create table %s(id serial primary key,
                             code text not null,
                             unique (code))''' % t
    cr.execute(sql) 

for t in ['tel',]:
    sql = '''create table %s(id serial primary key, 
                             code text not null,
                             unique (code) )''' % t
    cr.execute(sql)

for t in ['card',]:
    sql = '''create table %s(id serial primary key,
                             code text not null,
                             unique (code))''' % t 
    cr.execute(sql)

for t in ['patient_addr', 'patient_tel', 'patient_card']:
    s1, s2 = t.split('_')
    sql = '''create table %s (%s_id integer not null, 
                              %s_id integer not null,
                              foreign key (%s_id) references %s (id),
                              foreign key (%s_id) references %s (id),
            primary key (%s_id, %s_id))''' % (t, s1, s2, s1, s1, s2, s2, s1, s2)
    cr.execute(sql)
    for i in ['%s_id' % s1, '%s_id' % s2]:
        create_ix(t, i) 

# XXX
#for t in ['csession',]:
#    sql = '''create table %s (id serial primary key, 
#                              staff_id integer not null,
#                              number, 
#                              foreign key (staff_id) references staff (id)
#                              )''' % t
#    cr.execute(sql)
#    for i in ['staff_id', 'dt']:
#        create_ix(t, i)

for t in [# official: needed to put into database
          'amend', 'anormaly', 'insttype', 'tktype', 'state', 'usage',
          # official; redundant: 
          #   'insurertype', 'oprep', 'oprepic', 'otype', 'otypeic', 
          # official; for reference only
          #   'dept', 'healthservice', 'specord', 'donation', 'paytype', 
          # my own def to replace oprep + oprepic + otype + otypeic
          'ocode',  
         ]:
    sql = '''create table %s (id serial primary key,
                              code text not null, 
                              name text not null)''' % t 
    cr.execute(sql)
    for i in ['code',]:
        create_ix(t, i) 

for t in ['sam',]:
    sql = '''create table %s (id serial primary key,
                              code text not null, 
                              unique (code))''' % t 
    cr.execute(sql)
    for i in ['code',]:
        create_ix(t, i) 

for t in ['freq']:
    sql = '''create table %s (id serial primary key,
                              code text not null, 
                              name text not null,
                              freq real not null)''' % t
    cr.execute(sql)
    for i in ['code',]:
        create_ix(t, i) 

for t in ['selfpay', 'fee']:
    sql = '''create table %s (id serial primary key,
                              code text not null, 
                              name text not null,
                              price integer not null)''' % t 
    cr.execute(sql)
    for i in ['code',]:
        create_ix(t, i) 

for t in ['inst',]:
    sql = '''create table %s (id serial primary key, 
                              insttype_id integer not null, 
                              is_cont integer not null default 0, 
                              is_severe integer not null default 0, 
                              foreign key (insttype_id) references insttype (id)
                              )''' % t
    cr.execute(sql)
    for i in ['insttype_id', 'is_cont', 'is_severe']:
        create_ix(t, i)

for t in ['tk',]:
    sql = '''create table %s (id serial primary key,
                              inst_id integer not null,
                              patient_id integer not null, 
                              amend_id integer not null, 
                              insurertype_id integer not null default 0, 
                              tktype_id integer not null, 
                              sam_id integer not null, 
                              state_id integer not null, 
                              card_id integer not null,
                              staff_id_doctor integer not null,
                              staff_id_pharmacist integer not null,
                              newborn text not null default '', 
                              newbornmark text not null default '', 
                              newbornprobe text not null default '', 
                              sign text not null default '', 
                              dt text not null, 
                              serial text not null default '',
                              soap text not null default '',
                              foreign key(inst_id) references inst(id),
                              foreign key(patient_id) references patient(id),
                              foreign key(amend_id) references amend(id),
                              foreign key(tktype_id) references tktype(id),
                              foreign key(sam_id) references sam(id),
                              foreign key(state_id) references state(id),
                              foreign key(card_id) references card(id),
                              foreign key(staff_id_doctor) references staff(id),
                              foreign key(staff_id_pharmacist) references staff(id)
                                   )''' % t

    cr.execute(sql)
    for i in ['inst_id', 
              'patient_id',
              'amend_id', 
              'tktype_id', 
              'sam_id', 
              'state_id',
              'card_id',
              'staff_id_doctor',
              'staff_id_pharmacist',
              'dt', 
              'serial']:
        create_ix(t, i)

for t in ['diag']:
    sql = '''create table %s (id serial primary key,
                              code text not null, 
                              name text not null,
                              name_zh text not null,
                              unique (code))''' % t
    cr.execute(sql)
    for i in ['code',]:
        create_ix(t, i) 

for t in ['effect']:
    sql = '''create table %s (id serial primary key, 
                              effective_date text not null,
                              unique (effective_date))''' % t
    cr.execute(sql)
    for i in ['effective_date',]:
        create_ix(t, i, b_ex=True) 

for t in ['ord']:
    sql = '''create table %s (id serial primary key, 
                              code text not null,
                              name text not null,
                              name_en text not null default '',
                              note text not null default '',
                              unique (code, name))''' % t
    cr.execute(sql)
    #for i in ['code',]:
    #    create_ix(t, i) 

# =======================================================================
#               健保用藥品項查詢檔欄位格式說明  07/01/16
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

for t in ['med']:
    sql = '''create table %s (id serial primary key, 
                              code text not null,
                              name text not null,
                              spec_amount text not null default '',
                              spec_unit text not null default '',
                              content_name text not null default '',
                              content_amount text not null default '',
                              content_unit text not null default '',
                              med_type text not null default '',
                              vendor text not null default '',
                              med_class text not null default '',
                              quality_code text not null default '',
                              name_zh text not null default '',
                              class_group text not null default '',
                              content1 text not null default '',
                              content_amount1 text not null default '',
                              content_unit1 text not null default '',
                              content2 text not null default '',
                              content_amount2 text not null default '',
                              content_unit2 text not null default '',
                              content3 text not null default '',
                              content_amount3 text not null default '',
                              content_unit3 text not null default '',
                              content4 text not null default '',
                              content_amount4 text not null default '',
                              content_unit4 text not null default '',
                              content5 text not null default '',
                              content_amount5 text not null default '',
                              content_unit5 text not null default '',
                              manufacturer text not null default '',
                              atc_code text not null default '',
                              unique (code, name))''' % t
    cr.execute(sql)
    #for i in ['code', 'name']:
    #    create_ix(t, i) 

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

for t in ['mat']:
    sql = '''create table %s(id serial primary key, 
                             code text not null,
                             name text not null, 
                             model text not null, 
                             unit text not null, 
                             applier text not null default '',
                             allowance_code text not null default '',
                             unique(code, name))''' % t
    cr.execute(sql)
    #for i in ['code', 'name']:
    #    create_ix(t, i) 

for t in ['ord_effect']:
    sql = '''create table %s (ord_id integer not null,
                              effect_id integer not null,
                              price real not null,
                              primary key(ord_id, effect_id),
                              foreign key(ord_id) references ord(id),
                              foreign key(effect_id) references effect(id)
                              )''' % t
    cr.execute(sql)
    for i in ['ord_id', 'effect_id']:
        create_ix(t, i) 

for t in ['med_effect']:
    sql = '''create table %s (med_id integer not null,
                              effect_id integer not null,
                              price real not null,
                              primary key (med_id, effect_id),
                              foreign key(med_id) references med(id),
                              foreign key(effect_id) references effect(id)
                              )''' % t
    cr.execute(sql)
    for i in ['med_id', 'effect_id']:
        create_ix(t, i) 

for t in ['mat_effect']:
    sql = '''create table %s (mat_id integer not null,
                              effect_id integer not null,
                              effect_exam_id integer not null,
                              price real not null,
                              exam text not null,
                              payment_code text not null default '',
                              primary key (mat_id, effect_id, effect_exam_id),
                              foreign key(mat_id) references mat(id),
                              foreign key(effect_id) references effect(id),
                              foreign key(effect_exam_id) references effect(id)
                              )''' % t
    cr.execute(sql)
    for i in ['mat_id', 'effect_id', 'effect_exam_id']:
        create_ix(t, i) 

for t in ['tk_diag']:
    sql = '''create table %s (tk_id integer not null,
                              diag_id integer not null,
                              primary key (tk_id, diag_id),
                              foreign key(tk_id) references tk(id),
                              foreign key(diag_id) references diag(id)
                              )''' % t
    cr.execute(sql)
    for i in ['tk_id', 'diag_id']:
        create_ix(t, i) 
    
for t in ['tk_ord']:
    sql = '''create table %s (tk_id integer not null,
                              ord_id integer not null,
                              ocode_id integer not null,
                              percent integer not null, 
                              qty integer not null,
                              sign text not null default '',
                              primary key (tk_id, ord_id),
                              foreign key(tk_id) references tk(id),
                              foreign key(ord_id) references ord(id),
                              foreign key(ocode_id) references ocode(id)
                              )''' % t
    cr.execute(sql)
    for i in ['tk_id', 'ord_id', 'ocode_id']:
        create_ix(t, i) 
    
for t in ['tk_med']:
    sql = '''create table %s (tk_id integer not null,
                              med_id integer not null,
                              usage_id integer not null,
                              freq_id integer not null,
                              ocode_id integer not null,
                              days integer not null, 
                              dosage real not null,
                              sign text not null default '',
                              primary key (tk_id, med_id),
                              foreign key(tk_id) references tk(id),
                              foreign key(med_id) references med(id),
                              foreign key(usage_id) references usage(id),
                              foreign key(freq_id) references freq(id),
                              foreign key(ocode_id) references ocode(id)
                              )''' % t
    cr.execute(sql)
    for i in ['tk_id', 'med_id', 'usage_id', 'freq_id', 'ocode_id']:
        create_ix(t, i) 

for t in ['tk_mat']:
    sql = '''create table %s (tk_id integer not null,
                              mat_id integer not null,
                              ocode_id integer not null,
                              percent integer not null, 
                              qty integer not null,
                              sign text not null default '',
                              primary key (tk_id, mat_id),
                              foreign key(tk_id) references tk(id),
                              foreign key(mat_id) references mat(id),
                              foreign key(ocode_id) references ocode(id)
                              )''' % t
    cr.execute(sql)
    for i in ['tk_id', 'mat_id', 'ocode_id']:
        create_ix(t, i) 

for t in ['tk_fee',]:
    sql = '''create table %s (tk_id integer not null, 
                              fee_id integer not null,
                              qty integer not null default 1,
                              primary key(tk_id, fee_id),
                              foreign key(tk_id) references tk(id),
                              foreign key(fee_id) references fee(id)
                              )''' % t 
    cr.execute(sql)
    for i in ['tk_id', 'fee_id']:
        create_ix(t, i) 
   
for t in ['fav']:
    sql = '''create table %s (id serial primary key, 
                              code text not null,  
                              name text not null default '',
                              staff_id integer not null,
                              unique (code, name, staff_id),
                              foreign key (staff_id) references staff(id)
                              )''' % t
    cr.execute(sql)
    for i in ['code', 'staff_id']:
        create_ix(t, i) 

for t in ['fav_diag']:
    sql = '''create table %s (fav_id integer not null,
                              diag_id integer not null,
                              primary key (fav_id, diag_id),
                              foreign key(fav_id) references fav(id),
                              foreign key(diag_id) references diag(id)
                              )''' % t
    cr.execute(sql)
    for i in ['fav_id', 'diag_id']:
        create_ix(t, i) 
    
for t in ['fav_ord']:
    sql = '''create table %s (fav_id integer not null,
                              ord_id integer not null,
                              ocode_id integer not null,
                              percent integer not null, 
                              qty integer not null,
                              primary key (fav_id, ord_id),
                              foreign key(fav_id) references fav(id),
                              foreign key(ord_id) references ord(id),
                              foreign key(ocode_id) references ocode(id)
                              )''' % t
    cr.execute(sql)
    for i in ['fav_id', 'ord_id', 'ocode_id']:
        create_ix(t, i) 
    
for t in ['fav_med']:
    sql = '''create table %s (fav_id integer not null,
                              med_id integer not null,
                              usage_id integer not null,
                              freq_id integer not null,
                              ocode_id integer not null,
                              days integer not null, 
                              dosage real not null,
                              primary key (fav_id, med_id),
                              foreign key(fav_id) references fav(id),
                              foreign key(med_id) references med(id),
                              foreign key(usage_id) references usage(id),
                              foreign key(freq_id) references freq(id),
                              foreign key(ocode_id) references ocode(id)
                              )''' % t
    cr.execute(sql)
    for i in ['fav_id', 'med_id', 'usage_id', 'freq_id', 'ocode_id']:
        create_ix(t, i) 

for t in ['fav_mat']:
    sql = '''create table %s (fav_id integer not null,
                              mat_id integer not null,
                              ocode_id integer not null,
                              percent integer not null,
                              qty integer not null,
                              primary key (fav_id, mat_id),
                              foreign key(fav_id) references fav(id),
                              foreign key(mat_id) references mat(id),
                              foreign key(ocode_id) references ocode(id)
                              )''' % t
    cr.execute(sql)
    for i in ['fav_id', 'mat_id', 'ocode_id']:
        create_ix(t, i) 

for t in ['app']: # XXX
    sql = '''create table %s (id serial primary key, 
                              ym text not null, 
                              serial text not null,
                              unique (ym, serial))''' % t
    cr.execute(sql)
    for i in ['ym', 'serial',]:
        create_ix(t, i) 

for t in ['inst_app']:
    sql = '''create table %s (inst_id integer not null,
                              app_id integer not null,
                              insttype_id integer not null, 
                              nr integer not null,
                              foreign key (inst_id) references inst(id),
                              foreign key (app_id) references app(id),
                              primary key (inst_id, app_id))''' % t
    cr.execute(sql)
    for i in ['inst_id', 'app_id', 'insttype_id']:
        create_ix(t, i) 
    
for t in ['upload']: # XXX
    sql = '''create table %s (id serial primary key, 
                              datatype text not null default '1', 
                              dataformat text not null default '1', 
                              dt text not null)''' % t
    cr.execute(sql)
    for i in ['dt', 'datatype']:
        create_ix(t, i) 
    
for t in ['tk_upload',]:
    sql = '''create table %s (tk_id integer not null, 
                              upload_id integer not null, 
                              foreign key (tk_id) references tk(id),
                              foreign key (upload_id) references upload(id),
                              primary key (tk_id, upload_id))''' % t 
    cr.execute(sql)
    for i in ['tk_id', 'upload_id']:
        create_ix(t, i) 

# from G8S: ord, med, mat
# reuse functions in ../renew.py
# create tmp
# copy into this folder 

def cls():
    try:
        for i in ['renew.py', 'renew.pyc']:
            os.remove(i)
    except:
        pass
    try:
        shutil.rmtree('tmp') 
        os.rmdir('tmp') 
    except:
        pass

cls() 
os.mkdir('tmp')
shutil.copyfile(os.path.join('..', 'renew.py'), 'renew.py')

# create ord, med, mat from scratch
from renew import create_new
for t in ['ord', 'med', 'mat']:
    create_new(t, cr)

def build_diag():
    data = [[ll.strip().replace('"', '') for ll in l.split('\t')] for l in codecs.open(cat('txt', 'diag.txt'), 'r', 'utf-8')]
    l = sorted(list(set([tuple(d[3:6]) for d in data])))
    #cr.executemany('insert into diag (code, name, name_zh) values (%s, %s, %s)', l)
    codecs.open('diag', 'wb', 'utf-8').write('\n'.join(['\t'.join(ll) for ll in l]))
    start_time0 = time.time()
    print('start copying diag ... (# of data: %s)' % (len(l),))
    cr.copy_from(codecs.open('diag', 'rb', 'utf-8'), 'diag', columns=('code', 'name', 'name_zh'))
    print('completed copying diag. elapsed: %f seconds.' % (time.time() - start_time0,))

def build_freq():
    l = []
    for i in codecs.open(cat('txt', 'freq.txt'), 'r', 'utf-8'):
        s = [ii.strip() for ii in i.split(' ', 2)]
        s[2] = float(s[2])
        l.append(tuple(s))

    cr.executemany('insert into freq (code, name, freq) values (%s, %s, %s)', l)

def build_selfpay():
    l = []
    for i in codecs.open(cat('txt', 'selfpay.txt'), 'r', 'utf-8'):
        s = [ii.strip() for ii in i.split(' ', 2)]
        s[1] = int(s[1])
        l.append(tuple(s))
    cr.executemany('insert into selfpay (code, price, name) values (%s, %s, %s)', l)

def build_from_txt():
    build_diag()
    build_freq()
    build_selfpay()
    for t in ('amend', 'anormaly', 'insttype', 'tktype', 'state', 'usage'):
        l = []
        for i in codecs.open(cat('txt', '%s.txt' % t), 'r', 'utf-8'):
            l.append(tuple([ii.strip() for ii in i.split(' ', 1)]))
        sql = 'insert into %s (code, name) values (?, ?)' % (t,)
        sql = sql.replace('?', '%s')
        cr.executemany(sql, l)

build_from_txt()

# my own def: fee, ocode, fav 
cr.executemany('insert into fee (code, name, price) values (%s, %s, %s)', 
    ((u'n/a', u'無', 0),
     (u'tk_fee_em', u'急診掛號費', 100),
     (u'tk_fee_gen', u'一般掛號費', 50),
     (u'loan', u'欠卡押金', 500)))

# oprep, otype, oprepic, otypeic
cr.executemany('insert into ocode (code, name) values (%s, %s)', 
    ((u'["", "2", "", "3"]',    u'一般處置'),
     (u'["", "3", "", "4"]',    u'特殊材料'),
     (u'["0", "1", "01", "1"]', u'院所自調之藥品'),
     (u'["0", "1", "05", "2"]', u'院所自調之連續處方籤'),
     (u'["1", "4", "02", "1"]', u'處方釋出之藥品或檢驗'),
     (u'["1", "4", "06", "2"]', u'處方釋出之連續處方籤'),
     (u'["2", "2", "02", "1"]', u'病理'),
     (u'["self", "", "", ""]',  u'自費'),
     (u'["free", "", "", ""]',  u'贈送'),
    ))

start_time0 = time.time()
print(u'now creating indices ...')
for i in sqls_ix:
    cr.execute(i)
print(u'completed indices. elapsed: %f seconds.' % (time.time() - start_time0,))
print(u'\nAll Completed!! Elapsed: %f seconds.\n' % (time.time() - start_time,))

cn.commit()
cls()

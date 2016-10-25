# -*- coding: utf-8 -*-

import os, sqlite3, time, cPickle, codecs
try:
    import simplejson as json
except:
    import json
from collections import defaultdict
from bisect import bisect

os.chdir(os.path.dirname(__file__))
cat = os.path.join

cn = sqlite3.connect(cat('..', 'mycis.db'))
cr = cn.cursor()

b_create_dic = True 
if b_create_dic:
    dic_price = {}
    for typ in ('ord', 'med', 'mat'):
        dic_price[typ] = defaultdict(dict)
        codes = [r[0] for r in cr.execute('select distinct code from %s order by code' % typ).fetchall()]
        for code in codes:
            r = cr.execute('''
                select effect.effective_date, %s_effect.price from %s 
                join %s_effect on %s.id = %s_effect.%s_id
                join effect on %s_effect.effect_id = effect.id
                where %s.code = ? 
                order by effect.effective_date''' % tuple([typ] * 8), 
                (code,)).fetchall()
            dic_price[typ][code]['effective_date'] = tuple([rr[0] for rr in r])
            dic_price[typ][code]['price'] = tuple([0.0] + [rr[1] for rr in r])
    #cPickle.dump(dic_price, open(cat('..', 'cache', 'dic_price.pkl'), 'wb'))
    open(cat('..', 'cache', 'dic_price.json'), 'wb').write(json.dumps(dic_price))
    
    # custom 
    list_icd = [[ll.strip().replace('"', '') for ll in l.split('\t')] for l in codecs.open(cat('..', 'db', 'txt', 'diag.txt'), 'r', 'utf-8')]
    #cPickle.dump(list_icd, open(cat('..', 'cache', 'list_icd.pkl'), 'wb'))
    open(cat('..', 'cache', 'list_icd.json'), 'wb').write(json.dumps(list_icd))
    
    dic_all = defaultdict(dict)
    dic_all_inv = defaultdict(dict)
    for t in ('sam', 'amend', 'tktype', 'insttype', 'selfpay', 'ocode', 'fee', 
              'state', 'usage', 'freq', 'diag', 'ord', 'med', 'mat', 'anormaly'):
        for r in cr.execute('select * from %s' % t).fetchall():
            dic_all[t][r[1]] = r[0]
            dic_all_inv[t][r[0]] = r[1:]

    ##cPickle.dump(dic_all, open(cat('..', 'cache', 'dic_all.pkl'), 'wb'))
    #open(cat('..', 'cache', 'dic_all.json'), 'wb').write(json.dumps(dic_all))
    #cPickle.dump(dic_all_inv, open(cat('..', 'cache', 'dic_all_inv.pkl'), 'wb'))
    ##open(cat('..', 'cache', 'dic_all_inv.json'), 'wb').write(json.dumps(dic_all_inv))

    dic_custom_code_name = {}
    r = cr.execute('select id, code, name from fav where staff_id = ?', (1,)).fetchall()
    for fav_id, fav_code, fav_name in r:
        d = {}
        for t in ['diag', 'ord', 'med', 'mat']:
            d[t] = cr.execute('select %s_id from fav_%s where fav_id = ?' % (t, t),
                       (fav_id,)).fetchall()
        if sum([len(d[t]) for t in ['diag', 'ord', 'med', 'mat']]) != 1:
            continue
        iid, typ = [(d[t][0][0], t) for t in ['diag', 'ord', 'med', 'mat'] if d[t]][0]
        code, name = dic_all_inv[typ][iid][:2]
        dic_custom_code_name[code] = (fav_code, fav_name)
    open(cat('..', 'cache', 'dic_custom_code_name.json'), 'wb').write(json.dumps(dic_custom_code_name)) 

else:
    dic_price = cPickle.load(open(cat('..', 'cache', 'dic_price.pkl'), 'rb'))
    
def get_price(typ, code, dt):
    d = dic_price[typ][code]
    return d['price'][bisect(d['effective_date'], '1051001' if typ == 'ord' else dt)] 

dt = '1051001'
for typ in ('ord', 'med', 'mat'):
    codes = [r[0] for r in cr.execute('select distinct code from %s order by code' %typ).fetchall()]
    start_time = time.time()
    for code in codes:
        r = cr.execute('''
                select %s_effect.price from %s 
                join %s_effect on %s.id = %s_effect.%s_id
                join effect on %s_effect.effect_id = effect.id
                where %s.code = ? 
                and effect.effective_date <= ?
                order by effect.effective_date desc''' % tuple([typ] * 8), 
                (code, dt)).fetchone()
        price_db = r[0] if r else 0 
        price_bisect = get_price(typ, code, dt)
        assert price_db == price_bisect
    print('iterating %s to get prices: %f secs' % (typ, time.time() - start_time))

    start_time = time.time()
    for code in codes:
        r = get_price(typ, code, dt)
    print('iterating get_price to get %s prices: %f secs' % (typ, time.time() - start_time))

start_time = time.time()
for r in cr.execute('''
    select med.code, z.price from med
    join 
    (select x.med_id, x.price
    from med_effect x 
    join effect on x.effect_id = effect.id
    join
    (select med_effect.med_id, max(effect.effective_date) as maxd 
    from med_effect 
    join effect on med_effect.effect_id = effect.id
    where effect.effective_date <= ? group by med_effect.med_id) y 
    on  effect.effective_date = y.maxd 
    and x.med_id = y.med_id) z
    on z.med_id = med.id
    ''', (dt,)).fetchall():
    code, price = r
    price_bisect = get_price('med', code, dt)
    assert price == price_bisect
print('complicated sql to get %s prices: %f secs' % ('med', time.time() - start_time))

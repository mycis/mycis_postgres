# -*- coding: utf-8 -*-

# Important: Don't use non alpha-numeric characters (esp. '_', '(', ')', ...)
#            in gmail messages!!  27/10/09 02:49:07

import os, sys, shutil, tempfile, subprocess, hashlib, sqlite3

os.chdir(os.path.dirname(__file__))
cat = os.path.join

base = os.getcwd()
cid = '001_cwtu'
admin = 'ADMIN'
repo = cat(base, 'res', 'db')
BIN = cat(base, 'bin')
xdelta = cat(BIN, 'xdelta.exe') if os.name == 'nt' else 'xdelta3'
rsync = cat(BIN, 'rsync', 'rsync.exe') if os.name == 'nt' else 'rsync'
z = cat(BIN, '7z.exe') if os.name == 'nt' else '7z'
tmp = cat(base, 'tmp')
db = 'mycis.db'
sd = 'e'  # external hd: e drive

sys.path.insert(0, BIN)
from utl import channel, message, msg_time, time_stamp, cls, log  

def backup_remote_inc_ver():
    td = tempfile.mkdtemp(dir=tmp)
    
    log('Starting to do incremental backup !')
    log('Generating version string ...')
    ver = cat(repo, 'version')
    if not os.path.isfile(ver):        
        log('Initialize the version string: starting from 0.')
        open(ver, 'w').write('0')
    ed = int(open(ver, 'r').read())
    ed_old = str(ed).zfill(8)
    ed_new = str(ed + 1).zfill(8)
    
    log('Get database of previous version ...')
    old = cat(repo, db)
    if not os.path.isfile(old):
        log('This is the first time doing delta. Copy to repo.')
        shutil.copyfile(db, old) 
    old_coded = cat(repo, 'mycis_coded.db')
     
    new_ = cat(base, db)
    new = cat(td, db)
    # Use a copy to generate delta
    log('Use a copy to generate delta, otherwise there will be errors ...')
    shutil.copyfile(new_, new)
    
    delta_fn = 'delta-%s-%s' % (ed_old, ed_new)
    delta = cat(td, delta_fn)    
    
    log('Computing md5 ...')
    md5_old = hashlib.md5(open(old, 'rb').read()).hexdigest()
    md5_new = hashlib.md5(open(new, 'rb').read()).hexdigest()

    if md5_old == md5_new:
        log('No new delta is needed: Stop.')
        return
    
    log('Now generating delta, please wait ...')
    subprocess.call([xdelta, '-e', '-f', '-s', old, new, delta])
    
    # msg delta ex.:
    # From: cwtu_001, To: admin 
    # Subject: delta-00000001-00000002
    # Text:
    # 00000001=(md5 of mycis.db ed.00000001)
    # 00000002=(md5 of mycis.db ed.00000002)
    # Attachment: delta-00000001-00000002
    
    log('Authoring the delta msg ...')
    msg = message(cid, (admin,), delta_fn, '%s=%s\n%s=%s' % (ed_old, md5_old, ed_new, md5_new), [delta])
    
    log('Uploading delta, please wait ...')
    try:
        ch = channel()
        ch.append(cid, '', msg_time(), str(msg))
        # Render old <- new.
        subprocess.call([xdelta, '-d', '-f', '-s', old, delta, old_coded])
               
        md5_ = hashlib.md5(open(old_coded, 'rb').read()).hexdigest()
        if md5_ == md5_new:
            shutil.move(old_coded, old)
        
        else: # Should be very rare ...
            log('')
            os.remove(old_coded)
            return
        
        ed += 1
        open(ver, 'w').write(str(ed))
        log('Upload delta successfully !')

    except:
        log('Upload delta / Manage File unsuccessfully. Please check all settings & report to cytu !')

    finally:    
        try:
            ch.close()
        except:
            pass
        try:
            ch.logout()
        except:
            pass
        cls(td)

def backup_local():
    ''' rsync '''

    log(u'開始本機備份：將 mycis 系統映射至 %s 磁碟機上...' % sd)
    try:
        r = subprocess.check_call([rsync, '-rltz', '--delete', '--progress', '--modify-window=1', '/cygdrive/d/mycis/', '/cygdrive/%s/mycis/' % sd])
        log(u'本機備份完成！')       
    except:
        log(u'無法將 mycis 系統映射至 %s 磁碟機上，本機備份失敗...' % sd)

def backup_remote_inc():
    log(u'開始遠端備份 ...')
    
    td = tempfile.mkdtemp(dir=tmp)

    old = cat(repo, db)
    if not os.path.isfile(old):
        log(u'This is the first time doing backup. Copy to repo.')
        shutil.copyfile(db, old) 
     
    new_ = cat(base, db)
    new = cat(td, db)
    # Use a copy to generate delta
    #log('Use a copy to generate delta, otherwise there will be errors ...')
    shutil.copyfile(new_, new)
    
    delta_fn = 'delta' 
    delta = cat(td, delta_fn)    
    
    md5_old = hashlib.md5(open(old, 'rb').read()).hexdigest()
    md5_new = hashlib.md5(open(new, 'rb').read()).hexdigest()

    if md5_old == md5_new:
        log(u'新舊資料庫版本相同，無需遠端備份！')
        cls(td)
        return
    
    log(u'製作資料庫差異檔中，請稍候...')
    subprocess.check_call([xdelta, '-e', '-f', '-s', old, new, delta])
    
    # msg delta ex.:
    # From: cwtu_001, To: admin 
    # Subject: delta 2009-10-11 06:00:00
    # Text:
    # (md5 of old db)
    # (md5 of new db)
    # Attachment: delta
     
    tm = time_stamp()    
    msg = message(cid, (admin,), delta_fn + ' ' + tm, '%s\n%s' % (md5_old, md5_new), [delta])
    log(u'上傳資料庫差異檔中，請稍候...')
    try:
        ch = channel()
        ch.append(cid, '', msg_time(), str(msg))
              
        log(u'遠端備份成功！')

    except:
        log(u'遠端備份失敗...')

    finally:    
        try:
            ch.close()
            ch.logout()
        except:
            pass
        cls(td)

def backup_remote_all(dbc=''):
        
    td = tempfile.mkdtemp(dir=tmp)
    ud_s = cat(td, '%s.7z' % db)

    new_ = dbc if dbc else cat(base, db)
    new = cat(td, db)
    
    try:
        log(u'開始上傳完整資料庫。製作完整資料庫壓縮檔...')
        shutil.copyfile(new_, new)
        r = subprocess.check_call([z, 'a', '-t7z',  ud_s, new])
    
    except:
        log(u'完整資料庫壓縮檔無法製作，上傳失敗...')
        return False
    
    md5 = hashlib.md5(open(new, 'rb').read()).hexdigest()
    
    # msg backup ex.:
    # From: cwtu_001 
    # To: admin 
    # Subject: backup 2009-10-11 06:00:00
    # Text:
    # (md5 of db)
    # Attachment: mycis.db.7z

    msg = message(cid, (admin,), 'backup ' + time_stamp(), md5, [ud_s])
    
    try:
        log(u'完整資料庫上傳需要幾分鐘；請勿關閉視窗，耐心等候！')
        ch = channel()
        ch.append(cid, '', msg_time(), str(msg))

        # Delete all previous delta, if any.
        try:
            ch.select('[Google Mail]/All Mail')
            r, [ids] = ch.search(None, '(FROM "%s" TEXT "delta")' % cid)
            if ids.split():
                ch.copy(','.join(ids.split()), '[Google Mail]/Trash')  

        except:
            log(u'（請手動清除備份紀錄）')

        log(u'完整資料庫上傳成功！')
        ans = True

    except:
        log(u'完整資料庫上傳失敗...')
        ans = False

    finally:    
        try:
            ch.close()
        except:
            pass
        try:
            ch.logout()
        except:
            pass

        cls(td)
        return ans

if __name__ == '__main__':
    args = len(sys.argv)
    if args == 2:
        if sys.argv[1] == 'all':
            backup_remote_all()

    elif args == 1:
        backup_local()
        backup_remote_inc()
        raw_input('\nPress ENTER to leave ...')

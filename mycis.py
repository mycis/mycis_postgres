# -*- coding: utf-8 -*-

__version__ = '0.5'
release_date = 'October 01, 2016'

import time
start_time0 = time.time()

import os, sys
cat = os.path.join
os.chdir(os.path.dirname(__file__))

# ==============================================================================
#  singleton 
# ==============================================================================

if os.name == 'nt':
    from win32event import CreateMutex
    from win32api import CloseHandle, GetLastError
    from winerror import ERROR_ALREADY_EXISTS

    class singleton:
        ''' Limits application to single instance ''' 

        def __init__(self):
            self.mutexname = 'mycis_singleton_XXX'
            self.mutex = CreateMutex(None, False, self.mutexname)
            self.lasterror = GetLastError()
        
        def exists(self):
            return (self.lasterror == ERROR_ALREADY_EXISTS)
            
        def __del__(self):
            if self.mutex:
                CloseHandle(self.mutex)

    myapp = singleton()
    if myapp.exists():
        print('Another instance of %s is already running.' % __file__)
        sys.exit(0) 

from PyQt4.QtCore import *
from PyQt4.QtGui import *

app = QApplication(sys.argv)
app.setApplicationName('mycis')
app.setOverrideCursor(QCursor(Qt.WaitCursor))
app.setFont(QFont('Microsoft JhengHei'))
spl = QSplashScreen(QPixmap('res/img/health_care_shield.png'))
spl.show()
app.processEvents()

def show_msg(msg, align=Qt.AlignBottom|Qt.AlignHCenter):
    spl.showMessage(msg, align)

show_msg(u'載入 python 標準模組 ...')
import codecs, platform, tempfile, shutil, zipfile, datetime, atexit, calendar, math, sqlite3, logging, cgi

try:
    import simplejson as json
except:
    import json
from subprocess import call, Popen
from functools import partial
from collections import namedtuple, defaultdict
from operator import itemgetter
from bisect import bisect
from copy import deepcopy
from ctypes import *

print('load python standard library and PyQt4 : %f seconds.' % (time.time() - start_time0,))

logging.basicConfig(filename='log.txt', 
                    format='%(asctime)s %(levelname)s: %(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S', 
                    level=logging.INFO)
logger = logging.getLogger('cwtu')

#b_debug = False 
#cwd = os.getcwd()
#shutil.copyfile(cat(cwd, 'db', 'mycis_.db' if b_debug else 'mycis.db'), cat(cwd, 'mycis.db'))

#sys.stderr = codecs.open('errors.txt', 'a', 'utf-8')
    
show_msg(u'定義常用參數 ...')

DIAG_CODE, DIAG_NAME = range(2)
ORD_CODE, ORD_NAME, ORD_PRICE, ORD_PERCENT, ORD_QTY, ORD_AMOUNT, ORD_OCODE = range(7)
ORD_CODE_FAV, ORD_NAME_FAV, ORD_PERCENT_FAV, ORD_QTY_FAV, ORD_OCODE_FAV = range(5)
MED_CODE, MED_NAME, MED_DOSAGE, MED_FREQ, MED_DAYS, MED_QTY, MED_USAGE, MED_PRICE, MED_AMOUNT, MED_OCODE = range(10)
MED_CODE_FAV, MED_NAME_FAV, MED_DOSAGE_FAV, MED_FREQ_FAV, MED_DAYS_FAV, MED_USAGE_FAV, MED_OCODE_FAV = range(7)
MAT_CODE, MAT_NAME, MAT_PRICE, MAT_PERCENT, MAT_QTY, MAT_AMOUNT, MAT_OCODE = range(7)
MAT_CODE_FAV, MAT_NAME_FAV, MAT_PERCENT_FAV, MAT_QTY_FAV, MAT_OCODE_FAV = range(5)
FAV_ID, FAV_CODE, FAV_NAME = range(3)

CLINIC_NAME = u'杜外科診所'                 #
CLINIC_CODE = '3521011033'                  #
CLINIC_TAX_NR = '69564144'                  # 
CLINIC_ZIP = '701'                          #
CLINIC_ADDRESS = u'台南市東門路二段六十三號'#
CLINIC_TEL = '(06)2378927'                  #
DEPT_CODE= '03'                             #
DOCTOR_PID = 'E101919343'                   #
DOCTOR_NAME = u'杜進旺'                     #
PHARMACIST_PID = u''                        #
PHARMACIST_NAME = u''                       #
OPREP_CODE = '1'                            #

INSTTYPE = ['01', '03', '04', '08', '09', 'B6']
TKTYPE_WITH_PROBE = set(['01', '02', '03', '04', '05', '06', '07', '08'])

TMP = 'tmp'
DB = 'mycis.db'

show_msg(u'載入 ui 檔案 ...')
start_time0 = time.time()

from ui.dlg_tk_ini import Ui_dlg_tk_ini
from ui.dlg_tk_abn import Ui_dlg_tk_abn
from ui.dlg_ent_inst import Ui_dlg_ent_inst
from ui.dlg_fee import Ui_dlg_fee
from ui.dlg_print import Ui_dlg_print
from ui.dlg_pwd import Ui_dlg_pwd
from ui.dlg_login import Ui_dlg_login
from ui.dlg_fav import Ui_dlg_fav
from ui.win_app import Ui_win_app
from ui.win_inst import Ui_win_inst
from ui.win_stat import Ui_win_stat
from ui.win_probe import Ui_win_probe
from ui.win_fav import Ui_win_fav
from ui.win_main import Ui_win_main
from ui.win_ic import Ui_win_ic
from ui.wdg_probe import Ui_wdg_probe
from ui.wdg_fav import Ui_wdg_fav
print('load ui files : %f seconds.' % (time.time() - start_time0,))

start_time0 = time.time()
dic_icd10_enc = json.loads(open(cat('cache', 'dic_icd10_enc.json'), 'rb').read())
def icd10_encode(icd10_code):
    s = icd10_code.replace('.', '')
    if len(s) > 5 or s[0] in 'EV':
        s = dic_icd10_enc[s] 
    return s
print('load dic_icd10_enc : %f seconds.' % (time.time() - start_time0,))

start_time0 = time.time()
dic_price = json.loads(open(cat('cache', 'dic_price.json'), 'rb').read())
def get_price(typ, code, dt): 
    d = dic_price[typ][code]
    # XXX ord has no complete pricing history!
    return d['price'][bisect(d['effective_date'],'1051001' if typ == 'ord' else dt)]
print('load dic_price : %f seconds.' % (time.time() - start_time0,))

start_time0 = time.time()
list_icd = json.loads(open(cat('cache', 'list_icd.json'), 'rb').read())
list_zip = json.loads(open(cat('cache', 'list_zip.json'), 'rb').read())
dic_custom_code_name = json.loads(open(cat('cache', 'dic_custom_code_name.json'), 'rb').read())
print('load list_icd, list_zip, dic_custom_code_name : %f seconds.' % (time.time() - start_time0,))

def update_dic_custom_code_name(cr, staff_id=1):
    TK = ['diag', 'ord', 'med', 'mat']
    dd = {}
    r = cr.execute('select id, code, name from fav where staff_id = ?', 
                   (staff_id,)).fetchall()
    for fav_id, fav_code, fav_name in r:
        d = {}
        for t in ['diag', 'ord', 'med', 'mat']:
            d[t] = cr.execute('select %s_id from fav_%s where fav_id = ?' % (t, t),
                       (fav_id,)).fetchall()
        if sum([len(d[t]) for t in ['diag', 'ord', 'med', 'mat']]) != 1:
            continue
        iid, typ = [(d[t][0][0], t) for t in ['diag', 'ord', 'med', 'mat'] if d[t]][0]
        code, name = dic_all_inv[typ][iid][:2]
        dd[code] = (fav_code, fav_name)
    return dd

# Pathway for xdelta
#old = cat('res', 'db', DB)
#if not os.path.isfile(old):
#    shutil.copyfile(DB, old) 

# XXX
def valid_ord_code(s):
    if s[-1].lower() in 'abk' or s.upper() < '06001C' or (len(s) <= 6 and s[0].lower().isalpha()):
        return False
    return True    

cn = sqlite3.connect(DB)
cn.create_function('valid_ord_code', 1, valid_ord_code)
cr = cn.cursor()

start_time0 = time.time()
dic_all = defaultdict(dict)
dic_all_inv = defaultdict(dict)
for t in ('sam', 'amend', 'tktype', 'insttype', 'selfpay', 'ocode', 'fee', 
          'state', 'usage', 'freq', 'diag', 'ord', 'med', 'mat', 'anormaly'):
    for r in cr.execute('select * from %s' % t).fetchall():
        dic_all[t][r[1]] = r[0]
        dic_all_inv[t][r[0]] = r[1:]
print('generate dic_all, dic_all_inv : %f seconds.' % (time.time() - start_time0,))

is_dll_ok = False
try:
    cs = windll.LoadLibrary('CsHis.dll')
    eii = windll.LoadLibrary('nhi_eiiapi.dll')
    is_dll_ok = True

except:
    show_msg(u'dll檔未安裝，無法使用ic卡作業與申報！')

sts = QSettings(cat('res', 'mycis.ini'), QSettings.IniFormat)

# search for acrobat exe
def acrobat_exe():
    for repo in [r'C:\Program Files (x86)\Adobe', r'C:\Program Files\Adobe']:
        for root, dirs, files in os.walk(repo):
            for f in files:
                if f == 'AcroRd32.exe':
                    return cat(root, f)
    return ''

if os.name == 'nt':
    acrobat = acrobat_exe()

# ==============================================================================
#  utilities
# ==============================================================================

def fl(s, n, b_null_term=False):
    '''
    >>>fl(12345, 7) 
    '12345  '
    
    >>>fl('abcdefghij', 4)
    'abcd'

    '''
    ss = str(s).ljust(n)
    return (ss[:n-1] + '\0') if b_null_term else ss[:n]

def valid_pid(pid):
    A = {'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 
         'H': 17, 'I': 34, 'J': 18, 'K': 19, 'L': 20, 'M': 21, 'N': 22, 
         'O': 35, 'P': 23, 'Q': 24, 'R': 25, 'S': 26, 'T': 27, 'U': 28, 
         'V': 29, 'W': 32, 'X': 30, 'Y': 31, 'Z': 33}
    try:
        t2 = int(pid[1]) * 8 % 10 if pid[1].isdigit() else (A[pid[1]] % 10) * 8 % 10
        
        s = (int(str(A[pid[0]])[0]) * 1 % 10 + int(str(A[pid[0]])[1]) * 9 % 10 + t2 + int(pid[2]) * 7 % 10 + int(pid[3]) * 6 % 10 +  int(pid[4]) * 5 % 10 + int(pid[5]) * 4 % 10 + int(pid[6]) * 3 % 10 + int(pid[7]) * 2 % 10 + int(pid[8]) * 1 % 10) % 10 
        return s == ((10 - int(pid[9])) if s else int(pid[9]))
   
    except:
        return False

def error_ic(cr, r=0, is_dsc=True):
    d = {
    4000: u'讀卡機 timeout',
    4012: u'未置入安全模組卡',
    4013: u'未置入健保 IC 卡',
    4014: u'未置入醫事人員卡',
    4029: u'IC 卡權限不足',
    4032: u'所插入非安全模組卡',
    4033: u'所置入非健保 IC 卡',
    4034: u'所置入非醫事人員卡',
    4042: u'醫事人員卡 PIN 尚未認證成功',
    4043: u'健保卡讀取 / 寫入作業異常',
    4050: u'安全模組尚未與 IDC 認證',
    4051: u'安全模組與 IDC 認證失敗',
    4061: u'VPN 網路不通',
    4071: u'健保 IC 卡與 IDC 認證失敗',
    5001: u'就醫可用次數不足',
    5002: u'卡片已註銷',
    5003: u'卡片已過有限期限',
    5004: u'新生兒依附就醫已逾六十日',
    5005: u'讀卡機的日期時間讀取失敗',
    5006: u'讀取安全模組內的「醫療院所代碼」失敗',
    5007: u'寫入一組新的「就醫資料登錄」失敗',
    5008: u'安全模組簽章失敗',
    5009: u'無寫入就醫相關紀錄之權限',
    5010: u'同一天看診兩科（含）以上',
    5012: u'此人未在保',
    5015: u'「門診處方箋」讀取失敗',
    5016: u'「長期處方箋」讀取失敗',
    5017: u'「重要醫令」讀取失敗',
    5020: u'要寫入的資料和健保 IC 卡不是屬於同一人',
    5022: u'找不到「就醫資料登錄」中的該組資料',
    5023: u'「就醫資料登錄」寫入失敗',
    5028: u'HC 卡「就醫費用紀錄」寫入失敗',
    5033: u'「門診處方箋」寫入失敗',
    5051: u'新生兒註記寫入失敗',
    5052: u'有新生兒出生日期，但無新生兒胞胎註記資料',
    5056: u'讀取醫事人員 ID 失敗',
    5057: u'過敏藥物寫入失敗',
    5061: u'同意器官捐贈及安寧緩和醫療註記寫入失敗',
    5062: u'放棄同意器官捐贈及安寧緩和醫療註記輸入',
    5067: u'安全模組卡「醫療院所代碼」讀取失敗',
    5068: u'預防保健資料寫入失敗',
    5071: u'緊急聯絡電話寫入失敗',
    5078: u'產前檢查資料寫入失敗',
    5079: u'性別不符，健保 IC 卡記載為男性',
    5081: u'最近二十四小時內同院所未曾就醫，故不可取消就醫（就醫類別輸入 ZA/ZB 時檢查）',
    5082: u'最近二十四小時內同院所未曾執行產檢服務紀錄，故不可取消產檢（輸入 XA 時檢查）',
    5083: u'最近六次就醫不含就醫類別 AC，不可單獨寫入預防保健或產檢紀錄',
    5084: u'最近二十四小時內同院所未曾執行保健服務項目紀錄，故不可取消保健服務（輸入 YA~YF 時檢查）',
    5087: u'刪除「孕婦產前檢查」（限女性）全部十一組資料失敗',
    5093: u'預防接種資料寫入失敗',
    5102: u'使用者所輸入之 PIN 值，與卡上之 PIN 值不合',
    5105: u'原 PIN 碼尚未通過認證',
    5107: u'使用者輸入兩次新 PIN 值，兩次 PIN 值不合',
    5108: u'密碼變更失敗',
    5109: u'密碼輸入過程按「取消」鍵',
    5110: u'變更健保 IC 卡密碼時，請移除醫事人員卡',
    5111: u'停用失敗，且健保 IC 卡之 PIN 碼輸入功能仍啟用',
    5122: u'被鎖住的醫事人員卡仍未解開',
    5130: u'更新健保 IC 卡內容失敗',
    5141: u'未置入醫事人員卡，僅能讀取重大傷病有效起訖日期',
    5150: u'卡片中無此筆就醫記錄',
    5151: u'就醫類別為數值才可退掛',
    5152: u'醫療院所不同，不可退掛',
    5153: u'本筆就醫記錄已經退掛過，不可重覆退掛',
    5154: u'退掛日期不符合規定',
    5160: u'就醫可用次數不合理',
    5161: u'最近一次就醫年不合理',
    5162: u'最近一次就醫序號不合理',
    5163: u'住診費用總累計不合理',
    5164: u'門診費用總累計不合理',
    5165: u'就醫累計資料年不合理',
    5166: u'門住診就醫累計次數不合理',
    5167: u'門診部分負擔費用累計不合理',
    5168: u'住診急性三十天、慢性一百八十日以下部分負擔費用累計不合理',
    5169: u'住診急性三十天、慢性一百八十一日以上部分負擔費用累計不合理',
    5170: u'門診加住診部分負擔費用累計不合理',
    5171: u'門診加住診（急性三十日、慢性一百八十日以下）部分負擔費用累計不合理',
    5172: u'門診醫療費用累計不合理',
    5173: u'住診醫療費用累計不合理',
    6005: u'安全模組卡的外部認證失敗',
    6006: u'IDC 的外部認證失敗',
    6007: u'安全模組卡的內部認證失敗',
    6008: u'寫入讀卡機日期時間失敗',
    6014: u'IDC 驗證簽章失敗',
    6015: u'檔案大小不合或檔案傳輸失敗',
    6016: u'記憶體空間不足',
    6017: u'權限不足無法開啟檔案或找不到檔案',
    6018: u'參數錯誤',
    9001: u'送至 IDC Message Header 檢核不符',
    9002: u'送至 IDC 語法不符',
    9003: u'與 IDC 作業逾時',
    9004: u'IDC 異常無法 Service',
    9010: u'IDC 無法驗證該卡片',
    9011: u'IDC 驗證健保 IC 卡失敗',
    9012: u'IDC 無該卡片資料',
    9013: u'無效的安全模組卡',
    9014: u'IDC 對安全模組卡認證失敗',
    9015: u'安全模組卡對 IDC 認證失敗',
    9020: u'IDC 驗章錯誤',
    9030: u'無法執行卡片管理系統的認證',
    9040: u'無法執行健保 IC 卡 Applet Perso 認證',
    9041: u'健保 IC 卡 Applet Perso 認證失敗',
    9050: u'無法執行安全模組卡世代碼更新認證',
    9051: u'安全模組卡世代碼更新認證失敗',
    9060: u'安全模組卡遭停約處罰',
    9061: u'安全模組卡不在有效期內',
    9062: u'安全模組卡合約逾期或尚未生效',
    9070: u'上傳資料大小不符無法接收檔案',
    9071: u'上傳日期與 Data Center 不一致',
    9081: u'卡片可用次數大於三次，未達可更新標準',
    9082: u'此卡已被註銷，無法進行卡片更新作業',
    9083: u'不在保',
    9084: u'停保中',
    9085: u'已退保',
    9086: u'個人欠費',
    9087: u'負責人欠費',
    9088: u'投保單位欠費',
    9089: u'個人及單位均欠費',
    9090: u'欠費且未在保',
    9091: u'聲明不實',
    9092: u'其他',
    9100: u'藥師，藥劑生，特約藥局或藥局專用卡無權限',
    9101: u'保留項目',
    9102: u'保留項目',
    9103: u'保留項目',
    9104: u'保留項目',
    9105: u'保留項目',
    9106: u'保留項目',
    9107: u'保留項目',
    9108: u'保留項目',
    9109: u'保留項目',
    9110: u'保留項目',
    9111: u'保留項目',
    9112: u'保留項目',
    9113: u'保留項目',
    9114: u'保留項目',
    9115: u'保留項目',
    9116: u'保留項目',
    9117: u'保留項目',
    9118: u'保留項目',
    9119: u'保留項目',
    9120: u'保留項目',
    9121: u'保留項目',
    9122: u'保留項目',
    9123: u'保留項目',
    9124: u'保留項目',
    9125: u'保留項目',
    9126: u'保留項目',
    9127: u'找不到對應編碼內容或參數傳遞方法錯誤',
    9128: u'保留項目',
    9129: u'持卡人於非所限制的醫療院所就診',
    9130: u'醫事人員卡已註銷或停用',
    9140: u'醫事人員卡已逾有效期限',
    }
    return (u'\n（%s [%s] %s）' % 
            (u'錯誤原因：' if is_dsc else u'', r, d[r])) if r else ''

def error_eii(r):
    d = {
    5000: u'網路環境載入異常',
    5001: u'檔案大小異常',
    5002: u'找不到 Reader.dll',
    5003: u'檔名錯誤',
    5004: u'作業申請異常',
    5005: u'產生簽章錯誤',
    5006: u'記憶體不足',
    5007: u'下載路徑不存在',
    5008: u'取得醫療院所代碼錯誤',
    5009: u'檔名有誤',
    5010: u'認證錯誤',
    9999: u'不明異常',
    5020: u'連線總數量已超過，請稍後再試',
    5021: u'網路作業錯誤，訊息不完整',
    5022: u'等待醫療系統處理中',
    5023: u'等待 EIIAPI 處理中或交易不存在',
    5024: u'無法建立檔案',
    5025: u'寫入磁碟異常',
    5026: u'解密錯誤',
    5027: u'網路作業錯誤但已完成',
    5028: u'連線錯誤',
    }
    return d[r]

def show_error(par, code=0, title=u'IC卡錯誤訊息提示', msg=u''):
    QMessageBox.warning(par, title, u'%s%s' % (msg, error_ic(cr, code)))

def qna(par=None, title=u'', msg=u'', flags=(QMessageBox.Yes|QMessageBox.No)):
    return QMessageBox.question(par, title, msg, flags)

def info(par=None, title=u'', msg=u''):
    QMessageBox.information(par, title, msg)

def validate_pid(led):
    class error(Exception): 
        pass
    
    pid = unicode(led.text())
    try:
        if len(pid) != 10:
            raise error, u'身份證號碼應為十個字元，請檢查！'
        elif not valid_pid(pid):
            raise error, u'身份證號碼格式錯誤，請檢查！'
        return 1

    except error, e:
        QMessageBox.warning(led.parent(), u'身份證號碼輸入錯誤', unicode(e))
        led.setFocus()
        led.selectAll()
        return 0

def validate_code_name(led_code, led_name):
    class error(Exception): 
        pass
    
    code = unicode(led_code.text()).strip()
    name = unicode(led_name.text()).strip()
    try:
        if not code:
            raise error, u'「輸入代碼」不可空白！'
        if not name:
            raise error, u'「識別名稱」不可空白！'

        r = cr.execute('select * from fav where code = ? and name = ?', 
                       (code, name)).fetchone()
        if r:
            raise error, u'此組「輸入代碼」/「識別名稱」重複存在。\n請重新修改後再嘗試存檔！'
        return 1

    except error, e:
        QMessageBox.warning(led_code.parent(), u'輸入代碼錯誤', unicode(e))
        led_code.setFocus()
        led_code.selectAll()
        return 0

def rnd(n):
    return int(round(n))

# XXX
def serial_s(serial, insttype_code, sign, amend_code, tktype_code):
    s = serial.strip()
    if s:
        if insttype_code == 'B6':
            h = u'職災：' 
        elif amend_code == '2':
            h = u'補卡：' 
        elif s in dic_all_inv['anormaly'].keys():
            h = u'異常：'
        elif s in ('IC11', 'IC12', 'IC13', 'IC15', 'IC16', 'IC17', 'IC19', 'IC71', 'IC72', 'IC73', 'IC75', 'IC76', 'IC77', 'IC79'):
            h = u'兒健：'
        elif s in ['IC%s' % i for i in range(41, 61)]:
            h = u'產檢：'
        elif s in ['IC31', 'IC35', 'IC37']:
            h = u'抹片：'
        elif s in ['IC91', 'IC93']:
            h = u'乳攝：'
        elif s in ['IC85']:
            h = u'潛血：'
        elif s in ['IC95', 'IC97']:
            h = u'黏膜：'
        elif s in ['IC21', 'IC22', 'IC23', 'IC24']:
            h = u'成健：'
        else:
            h = u''
    else:
        if sign.strip():
            if tktype_code == 'AA' and amend_code == '2':
                h = u'補卡同療'
            elif tktype_code == 'AA' and amend_code == '1': 
                h = u'同一療程'
            else:
                h = u''
        else:
            if tktype_code == 'AA':
                h = u'欠卡同療'
            else:
                h = u'欠卡'
    return h + s

def dt_s(dt, date_only=False):
    try:
        s = '%s.%s.%s' % (int(dt[:3]), dt[3:5], dt[5:7])
        return s if date_only else '%s %s:%s:%s' % (s, dt[7:9], dt[9:11], dt[11:13])
    except:
        return ''

def dt_now():
    return datetime.datetime.now()

def dt_tw(dt, date_only=False):
    s = str(dt.year - 1911).zfill(3) + dt.strftime('%m%d%H%M%S')
    return s[:7] if date_only else s

def now():
    return dt_tw(dt_now())

def dt_before(dt_i, days=5):
    dt = dt_i
    dt -= datetime.timedelta(days=days)
    # XXX in this month; never on sunday; never greater than today
    while dt.month != dt_i.month:
        dt += datetime.timedelta(days=1)
    if dt.date().weekday() == 6:
        dt += datetime.timedelta(days=1)
    if dt > dt_i:
        dt = dt_now()
    return dt

def dt_add_1hr(dt):
    return dt_tw(datetime.datetime(int(dt[:3]) + 1911, int(dt[3:5]), int(dt[5:7]), int(dt[7:9]), int(dt[9:11])) + datetime.timedelta(minutes=60))[:11]
           
def str2date(s):
    return datetime.datetime(*time.strptime(s.split('.')[0], '%Y%m%d')[:6])

def t_n(dl):
    return dl - datetime.timedelta(microseconds=dl.microseconds)

def spaced_s(orig_s, s=u' '):
    return s.join(orig_s)

def ellipsis(s, n=0):
    return s if len(s) <= n else s[:n] + ' ...'

def gender(pid, is_en=True):
    return ('male' if is_en else u'男') if pid[1] in '1ACY' else ('female' if is_en else u'女')

def zh(typ):
    d = {'prscr':  u'處方籤', 
         'chk':    u'檢驗單', 
         'rcpt':   u'明細收據', 
         'rcptn':  u'費用收據', 
         'dtl':    u'總表', 
         'apply':  u'申報', 
         'upload': u'上傳',
         'query':  u'申報結果查詢'}
    return d.get(typ, '') 

# ref: http://www.robvanderwoude.com/commandlineswitches.php
def pdf_print(f):
    if os.name == 'nt':
        l = [acrobat, '/N', '/T', f]

    elif os.name == 'posix': # XXX
        l = ['evince', f]
    
    Popen(l)

def kill_adobe():
    if os.name == 'nt':
        Popen(['taskkill', '/F', '/FI', 'WINDOWTITLE eq Adobe*'])

def rm_tmp():
    shutil.rmtree(TMP)
    os.mkdir(TMP)

def atexit_f(fn, restart=True):
    rm_tmp()  
    call(['python', './%s.py' % fn])
    if restart:
        Popen(['python', './mycis.py'])

def attrs_from_dict(d):
    self = d.pop('self')
    for n, v in d.iteritems():
        setattr(self, n, v)

# ============================================================================
#  database functions
# ============================================================================

# XXX        
def is_duplicate_tk(tk_id, cr):
    r = cr.execute('''
    select 1 from tk where tk.patient_id = (select patient_id from tk where id = ?)
    and tk.dt > (select dt from tk where id = ?)
    and substr(tk.dt, 1, 7) = (select substr(dt, 1, 7) from tk where id = ?) 
 and (exists (select 1 from tk_ord where tk_ord.tk_id = tk.id and tk_ord.sign = "") 
 or exists (select 1 from tk_med where tk_med.tk_id = tk.id and tk_med.sign = ""))''', (tk_id, tk_id, tk_id)).fetchone()

    return r is not None

def model_collect_zip(): 
    model = QStandardItemModel(0, 4)
    for l in sorted([(d[0], ' '.join(d[1:4]), d[4], 'zip_%s' % i) for i, d in enumerate(list_zip)], key=itemgetter(0, 1)):
        model.appendRow([QStandardItem(ll) for ll in l])
    return model

# dt is in dt_tw; must manually sort the model.
def model_collect(dt): 
    model = QStandardItemModel(0, 3)
    ll_model = []
    
    # fixed
    for d in list_icd:
        ll_model.append((d[0].replace('.', ''), d[5], 'diag' + '_' + str(dic_all['diag'].get(d[3]))))

    # fixed
    d = dic_all_inv['diag']
    for k in d.keys():
        code, name, name_zh = d[k]
        col1 = code.replace('.', '') 
        ll_model.append((col1, name_zh, 'diag' + '_' + str(k)))

    d = dic_all_inv['ord']
    for k in d.keys():
        code, name = d[k][:2]
        price = get_price('ord', code, dt)
        if price > 0.0:
            ll_model.append((code, name, 'ord' + '_' + str(k)))
    
    d = dic_all_inv['med']
    for k in d.keys():
        code, name = d[k][:2]
        price = get_price('med', code, dt)
        if price > 0.0:
            ll_model.append((name, code, 'med' + '_' + str(k)))
    
    d = dic_all_inv['mat']
    for k in d.keys():
        code, name = d[k][:2]
        price = get_price('mat', code, dt)
        if price > 0.0:
            ll_model.append((code, name, 'mat' + '_' + str(k)))

    for l in sorted(ll_model, key=itemgetter(0, 1, 2)):
        model.appendRow([QStandardItem(ll) for ll in l])
    
    return model

def ids(l):
    return [tuple(ll[:2]) for ll in l]

def ids_(l):
    return [ll['fav_id'] for ll in l]

def list_in_ids(l, _ids):
    return [tuple(ll) for ll in l if tuple(ll[:2]) in _ids]

def list_in_ids_(l, _ids):
    return [ll for ll in l if ll['fav_id'] in _ids]

def diff(l_i, l_f, b_debug=False):
    if b_debug:
        print('l_i: ', l_i)
        print('l_f: ', l_f)

    k_i = set(ids(l_i))
    k_f = set(ids(l_f))

    if b_debug:
        print('k_i: ', k_i, ' k_f: ', k_f)

    l_i_in = list_in_ids(l_i, k_i & k_f) 
    l_f_in = list_in_ids(l_f, k_i & k_f)

    assert sorted(ids(l_i_in)) == sorted(ids(l_f_in))

    l_delete = list_in_ids(l_i, k_i - k_f)
    l_insert = list_in_ids(l_f, k_f - k_i)
    l_update = list(set(l_f_in) - set(l_i_in)) 

    d = {'l_delete': l_delete, 'l_insert': l_insert, 'l_update': l_update}
    if b_debug:
        print(d)
    return d

def diff_favs(favs_i, favs_f):
    k_i = set(ids_(favs_i))
    k_f = set(ids_(favs_f))

    l_i_in = list_in_ids_(favs_i, k_i & k_f) 
    l_f_in = list_in_ids_(favs_f, k_i & k_f)

    assert sorted(ids_(l_i_in)) == sorted(ids_(l_f_in))

    l_delete = list_in_ids_(favs_i, k_i - k_f)
    l_insert = list_in_ids_(favs_f, k_f - k_i)

    d = {'l_delete': l_delete, 'l_insert': l_insert, 
         'l_update_i': l_i_in, 'l_update_f': l_f_in}
    return d

def columns(t): 
    return [str(i[1]) for i in cr.execute('pragma table_info (%s)' % t).fetchall()]

def import_tk(tk_id, cr):
    d = {}        
    d['tk_id'] = tk_id
    r = cr.execute('''select patient.name, 
                             patient.pid, 
                             patient.birthday,
                             patient.note,
                             inst.insttype_id, 
                             inst.is_cont, 
                             inst.is_severe,
                             inst.id,
                             tk.dt,
                             tk.soap
                             from tk 
                             join patient on tk.patient_id = patient.id
                             join inst on tk.inst_id = inst.id
                             where tk.id = ?''', (tk_id,)).fetchone()
    d['name'], d['pid'], d['birthday'], d['note'], d['insttype_id'], d['is_cont'], d['is_severe'], d['inst_id'], d['dt'], d['soap'] = r

    for t in ['diag', 'ord', 'med', 'mat']:
        d[t] = []
        for i in cr.execute('select * from tk_%s where tk_id = ?' % t, 
                            (tk_id,)).fetchall():
            d[t].append(list(i))
    return d

def import_fav(fav_id, staff_id, cr):
    r = cr.execute('select code, name from fav where id = ? and staff_id = ?', (fav_id, staff_id,)).fetchone()
    if r is None:
        return {}

    d = {} 
    d['fav_id'] = fav_id
    d['code'], d['name'] = r

    for t in ['diag', 'ord', 'med', 'mat']:
        # list() is important for further editing
        d[t] = [list(l) for l in cr.execute('select * from fav_%s where fav_id = ?' % t, (fav_id,)).fetchall()]

    return d 

def import_favs(staff_id, cr):
    l_favs = []
    rr = cr.execute('select id from fav where staff_id = ? order by code', (staff_id,)).fetchall()
    for r in rr:
        l_favs.append(import_fav(r[0], staff_id, cr))
    return l_favs 

# ==============================================================================
#  database related 
# ==============================================================================

def ocode_def(code, typ='', is_cont=False, b_ph=False):
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

def tk_save(name='', pid='', birthday='', card_code='', insurertype_code='', state_code='3', newborn='', newbornmark='', newbornprobe='', tktype_code='01', amend_code='1', dt='', serial='', sign='', sam_code='', insttype_code='09', staff_id_doctor=1, staff_id_pharmacist=2, inst_id=0):    

    if not (name.strip() and pid.strip() and birthday.strip()):
        return {}
    try:
        s = sam_code
        r = dic_all['sam'].get(s, 0)
        if r:
            sam_id = r
        else:
            cr.execute('insert into sam (code) values (?)', (s,))
            sam_id = cr.execute('select last_insert_rowid()').fetchone()[0]
        
        amend_id = dic_all['amend'].get(amend_code, 1) 
        tktype_id = dic_all['tktype'].get(tktype_code, 1) 
        state_id = dic_all['state'].get(state_code, 3)
        insttype_id =  dic_all['insttype'].get(insttype_code, 1)
             
        r = cr.execute('select id from patient where pid = ?', (pid,)).fetchone()
        if r:
            patient_id = r[0]
            ## possible update of patient name and birthday, as seen in dlg_tk_abn
            ## XXX Should I update here? The only authoritive source is IC ...
            #cr.execute('update patient set name = ?, birthday = ? where id = ?', 
            #           (name, birthday, patient_id))

        else:
            cr.execute('''insert into patient (pid, name, birthday) 
                           values (?, ?, ?)''', (pid, name, birthday))
            patient_id = cr.execute('select last_insert_rowid()').fetchone()[0]

        if not inst_id:
            cr.execute('''insert into inst (insttype_id) values (?)''', 
                                             (insttype_id,)) 
            
            inst_id = cr.execute('select last_insert_rowid()').fetchone()[0] 
        
        r = cr.execute('select id from card where code = ?', 
                       (card_code,)).fetchone()
        if r:
            card_id = r[0]
        else:
            cr.execute('insert into card (code) values (?)', (card_code,))
            card_id = cr.execute('select last_insert_rowid()').fetchone()[0] 
            cr.execute('''insert into patient_card (patient_id, card_id) 
                                 values (?, ?)''', (patient_id, card_id))
        
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
                                      serial)
                        values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                     (inst_id,
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
                                      serial))

        tk_id = cr.execute('select last_insert_rowid()').fetchone()[0]
        
        l = [] 
        s = serial
        if s:
            if not amend_code == '2':
            # 非補卡：掛號費; 補卡：免掛號費
                l = [(tk_id, 3, 1)]        
        else:
            if sign.strip():
                if tktype_code == 'AA' and amend_code == '1':
                # 同一療程：掛號費
                    l = [(tk_id, 3, 1)]
            else:
                # 欠卡：掛號費 + 押金        
                l = [(tk_id, 3, 1), (tk_id, 4, 1)]     
        if l: 
            cr.executemany('''insert into tk_fee (tk_id, fee_id, qty) 
                              values (?, ?, ?)''', l)
        cn.commit()
        return vars()

    except:
        cn.rollback()
        return {}

def tag(tn='', c='', b=True):
    s = '<%s>%s</%s>' % (tn, str(c).strip(), tn) 
    return (s if (c and tn) else '') if b else s 

def attrs(cr, tk_id=0, inst_id=0, ym='', nr=0, is_app=False, is_xml=False, is_ic=False):
    apptype='1' 
    specord_code = '' 
    trans_code = 'N' 
    is_trans = 'N' 
    surgery_code_main = '' 
    surgery_code_sub = ''
    pharmacy_code = ''
    clinic_code = CLINIC_CODE     
    dept = DEPT_CODE 
    doctor_pid = DOCTOR_PID           # XXX
    doctor_name = DOCTOR_NAME         # XXX
    pharmacist_pid = PHARMACIST_PID   # XXX
    pharmacist_name = PHARMACIST_NAME # XXX
    
    # XXX   
    r = cr.execute('''select patient.name, 
                             patient.pid, 
                             patient.birthday,
                             inst.is_cont, 
                             inst.is_severe, 
                             insttype.code
                             from tk 
                             join patient on tk.patient_id = patient.id
                             join inst on tk.inst_id = inst.id
                             join insttype on inst.insttype_id = insttype.id 
                             where tk.id %s''' % 
        (''' in (select id from tk where inst_id = ?)''' if inst_id else ' = ?',),
                             (inst_id,) if inst_id else (tk_id,)).fetchone()
    
    name, pid, birthday, is_cont, is_severe, insttype_code = r 
    paytype_code = '1' if insttype_code == 'B6' else '4'

    r_tk = cr.execute('''select tk.serial, 
                                tk.dt, 
                                tk.newbornmark,
                                state.code, 
                                amend.code, 
                                tktype.code
                                from tk
                                join amend on tk.amend_id = amend.id
                                join state on tk.state_id = state.id
                                join tktype on tk.tktype_id = tktype.id
                                where tk.id %s order by tk.dt''' % 
        (''' in (select id from tk where inst_id = ?)''' if inst_id else ' = ?',), 
                      (inst_id,) if inst_id else (tk_id,)).fetchall()
    
    # XXX
    newbornmark, state_code = '', '3'
    for g in r_tk:
        if g[0].isdigit():
            newbornmark, state_code  = g[2:4]
            break
    # XXX
    dt, dt_end = '', ''
    l_dt = [g[1] for g in r_tk]
    dt = l_dt[0] 
    dt_end = l_dt[-1]
    # XXX 欠卡 -- 補卡是否適用？
    dt_end = '' if dt_end == dt else dt_end 
    dt_pr = dt_s(dt, True) + ((' ' + dt_s(dt_end, True)) if dt_end else '') 
    
    #if not inst_id:
    #  r_dt = cr.execute('select dt, sign, serial from tk where inst_id = (select inst_id from tk where id = ?) order by dt', (tk_id,)).fetchall()

    # for pdf  
    s_pdf = (pid, dt)

    selfpay_code = 'D10'
    q = cr.execute('select price from selfpay where code = ?', 
                    (selfpay_code,)).fetchone()        
    selfpay_bas = q[0] if q else 50

    if state_code == '1':
        selfpay_code = '003'
    elif state_code == '2':
        selfpay_code = '004'
    # XXX 
    elif state_code == '3':
        if newbornmark.strip():
            selfpay_code = '903'
        elif insttype_code == 'B6':
            selfpay_code = '006'            
        elif is_severe:
            selfpay_code = '001'

    q = dic_all_inv['selfpay'].get(dic_all['selfpay'].get(selfpay_code))[-1]
    serial, amount_tk, amount_selfpay, amount_agency = '', 0, 0, 0
    for g in r_tk:
        s = g[0].strip()
        if s: # 卡序掛號：計價 
            serial = s  # XXX
            serial_s = (u'補卡：' + s) if (g[4] == '2' and g[5] == '01') else s# XXX
            if selfpay_code in ('003', '004', '005', '006', 
                                '901', '902', '903', '904'):
                amount_agency += selfpay_bas
            else:
                amount_selfpay += (q if q else selfpay_bas)            
        
        q = cr.execute('''select fee.price * tk_fee.qty from tk_fee 
                          join fee on tk_fee.fee_id = fee.id 
                          where tk_fee.tk_id = ? 
                          and fee.code like ?''', 
                          (tk_id, 'tk_fee' + '%')).fetchone()
        amount_tk += q[0] if q else 0 

    # diag
    r = cr.execute('''select distinct diag.code, diag.name from diag 
                      join tk_diag on diag.id = tk_diag.diag_id 
                      where tk_diag.tk_id %s order by diag.code''' % 
        (''' in (select id from tk where inst_id = ?)''' if inst_id else ' = ?',), 
                      (inst_id,) if inst_id else (tk_id,)).fetchall()
    
    l, l1, l2, l3, l4 = [], [], [], [], []
    for i, d in enumerate(r):
        icd10_code, icd10_name = d

        if i < 3:
            l2.append(icd10_code)
            l3.append(icd10_name)

        if is_ic and i < 6:
            l4.append(fl(icd10_encode(icd10_code), 5))    
        
        if is_xml and i < 6:
            l.append('<A%s>%s</A%s>' % (25 + i, icd10_code.replace('.', ''),
                                        25 + i))
        if is_app and i < 5:
            l1.append('<d%s>%s</d%s>' % (19 + i, icd10_code.replace('.', ''),
                                         19 + i))
    xml_diag = ''.join(l)
    icds_dbody = ''.join(l1) 
    icds_code = '  '.join(l2)    
    icds_name = '  '.join(l3)[:50]
    icds_ic = ''.join(l4)

    l_ic, l_ord, l_ic_id = [], [], []
    l, l_chk, l_charged = [], [], []
    l_pdata = []

    # ord XXX 04/30/14 add tk.dt  
    record_ord = namedtuple('record_ord', 'code name percent qty ocode_code sign dt tk_id ord_id')
    r = cr.execute('''select ord.code, 
                             ord.name, 
                             tk_ord.percent, 
                             tk_ord.qty, 
                             ocode.code,
                             tk_ord.sign,
                             tk.dt,
                             tk_ord.tk_id,
                             tk_ord.ord_id
                             from tk_ord
                             join ord on tk_ord.ord_id = ord.id
                             join ocode on tk_ord.ocode_id = ocode.id
                             join tk on tk_ord.tk_id = tk.id
                             where tk_ord.tk_id %s order by ord.code''' % 
        (''' in (select id from tk where inst_id = ?)''' if inst_id else ' = ?',), 
                            (inst_id,) if inst_id else (tk_id,)).fetchall()

    amount_ord = 0 
    n_p13 = 0

    for oo in r:
        o = record_ord._make(oo)
        n_p13 += 1
        o_price = get_price('ord', o.code, dt)
        # XXX inexact float
        o_amount = rnd(o.percent * o.qty * o_price / 100.)
        oprep_code, otype_code, oprepic_code, otypeic_code =json.loads(o.ocode_code)
        if oprep_code != '1':
            amount_ord += o_amount
        else:
            l_chk.append((o.code + '  ' + ellipsis(o.name, 47), o.qty))
        
        l_ord.append((oprep_code, 
                      otype_code, 
                      o.code, 
                      o.name[:9], 
                      '', 
                      o.percent, 
                      '', 
                      o.qty, 
                      o_price, 
                      o_amount))

        if otype_code != '4':
            l_charged.append((o.name, o.qty, o_amount))
        
        if is_app:  
            l_pdata.append(''.join([
                                            #p1  藥品給藥日份
                tag('p2', oprep_code),      #p2  醫令調劑方式
                tag('p3', otype_code),      #p3  醫令類別
                tag('p4', o.code),          #p4  藥品(項目)代號
                                            #p5  藥品用量
                                            #p6  診療之部位
                                            #p7  藥品使用頻率
                tag('p8', o.percent),       #p8  支付成數
                                            #p9  給藥途徑/作用部位
                tag('p10', o.qty),     #p10 總量
                tag('p11', o_price),   #p11 單價
                tag('p12', o_amount),  #p12 點數
                tag('p13', n_p13),     #p13 醫令序
                tag('p14', o.dt[:11]), #p14 執行時間-起 XXX 04/30/14
                tag('p15', dt_add_1hr(o.dt)), #p15 執行時間-迄 XXX 04/30/14
                                            #p16 執行醫事人員代號
                                       #p17 慢性病連續處方箋、同一療程及排檢案件註記
                                            #p18 影像來源
                                            #p19 事前審查受理編號
                                            #p20 就醫科別
            ]))

        if is_ic:
            l_ic.append(''.join([fl(dt, 13), 
                                 fl(otypeic_code, 1), 
                                 fl(o.code, 12), 
                                 fl('', 6), 
                                 fl(o.percent, 18), 
                                 fl('', 2), 
                                 fl(o.qty, 7), 
                                 fl(oprepic_code, 2)]))
            l_ic_id.append(['ord', o.tk_id, o.ord_id])

        if is_xml:
            # XXX 04/10/16 22:04:09 A77 changed from o.qty to o.qty / 100. 
            l.append('<MB2><A72>%s</A72><A73>%s</A73><A75>%s</A75><A77>%s</A77><A78>%s</A78>%s</MB2>' % (otypeic_code, o.code, o.percent, '%.2f' % (o.qty / 100.,), oprepic_code, tag('A79', o.sign)))
    
    xml_ord = ''.join(l)
    has_chk = len(l_chk) > 0
    
    # med 
    record_med = namedtuple('record_med', 'code name usage freq_code freq days dosage ocode_code sign tk_id med_id')
    r = cr.execute('''select med.code, 
                             med.name, 
                             usage.code, 
                             freq.code, 
                             freq.freq, 
                             tk_med.days, 
                             tk_med.dosage, 
                             ocode.code,
                             tk_med.sign,
                             tk_med.tk_id,
                             tk_med.med_id
                             from tk_med 
                             join med on tk_med.med_id = med.id 
                             join usage on tk_med.usage_id = usage.id 
                             join freq on tk_med.freq_id = freq.id 
                             join ocode on tk_med.ocode_id = ocode.id 
                             where tk_med.tk_id %s order by med.code''' % 
        (''' in (select id from tk where inst_id = ?)''' if inst_id else ' = ?',), 
                             (inst_id,) if inst_id else (tk_id,)).fetchall()

    days, amount_med = 0, 0   
    l, l_med = [], []
    
    for m0 in r:
        m = record_med._make(m0)
        n_p13 += 1
        m_qty = m.freq * m.days * m.dosage
        m_price = get_price('med', m.code, dt)
        m_amount = rnd(m_qty * m_price)

        oprep_code, otype_code, oprepic_code, otypeic_code =json.loads(m.ocode_code)
        if oprep_code == '1':
            l_med.append((m.code + '  ' + ellipsis(m.name, 90), 
                    m.usage + '  ' + m.freq_code + ' x ' + str(m.dosage), m_qty))
        
        if oprep_code in ('0', '4', '5', '6', 'A', 'B'):
            amount_med += m_amount

        if otype_code == '4':
            if m.days >= days:
                days = m.days
        else:
            l_charged.append((m.name, m_qty, m_amount))
        
        l_ord.append((oprep_code, 
                      otype_code, 
                      m.code, 
                      m.name[:15], 
                      m.dosage, 
                      m.freq_code, 
                      m.usage, 
                      m_qty, 
                      m_price, 
                      m_amount))
        
        if is_app:
            l_pdata.append(''.join([
                tag('p1', m.days if oprep_code != '0' else ''),
                                            #p1  藥品給藥日份
                tag('p2', oprep_code),      #p2  醫令調劑方式
                tag('p3', otype_code),      #p3  醫令類別
                tag('p4', m.code),          #p4  藥品(項目)代號
                tag('p5', m.dosage),        #p5  藥品用量
                                            #p6  診療之部位
                tag('p7', cgi.escape(m.freq_code)),  #p7  藥品使用頻率
                                            #p8  支付成數
                tag('p9',  m.usage),        #p9  給藥途徑/作用部位
                tag('p10', m_qty),          #p10 總量
                tag('p11', m_price),        #p11 單價
                tag('p12', m_amount),       #p12 點數
                tag('p13', n_p13),          #p13 醫令序
                                            #p14 執行時間-起
                                            #p15 執行時間-迄
                                            #p16 執行醫事人員代號
                                       #p17 慢性病連續處方箋、同一療程及排檢案件註記
                                            #p18 影像來源
                                            #p19 事前審查受理編號
                                            #p20 就醫科別
            ]))
        if is_ic:
            l_ic.append(''.join([fl(dt, 13), 
                                 fl(otypeic_code, 1), 
                                 fl(m.code, 12), 
                                 fl('', 6),
                                 # XXX 07/23/15 22:53:57 test no writing
                                 #fl('%s %s' % (m[3], m[4]), 18), 
                                 fl(str(m.freq_code), 18), 
                                 fl(m.days, 2),
                                 # XXX 07/23/15 22:53:57 test updated format
                                 #fl(m_qty, 7), 
                                 ('%5.2f' % (m_qty,)).replace('.', '').rjust(7),
                                 fl(oprepic_code, 2)]))
            
            l_ic_id.append(['med', m.tk_id, m.med_id])

        if is_xml:
            l.append('<MB2><A72>%s</A72><A73>%s</A73><A75>%s %s</A75><A76>%s</A76><A77>%s</A77><A78>%s</A78>%s</MB2>' % (otypeic_code, m.code, m.usage, cgi.escape(m.freq_code), m.days, m_qty, oprepic_code, tag('A79', m.sign)))         
    xml_med = ''.join(l)
    
    has_prscr = len(l_med) > 0
    
    # XXX
    b = len(l_med) > 0 or len(l_ord) > 0
    has_dtl = b 
    has_rcpt = b 
    has_rcptn = b 

    days = 1 if days == 0 else (days if len(r) else 0)
    days_cont = days if is_cont else 0
    
    # XXX only valid in clinic
    if list(set([g[5] for g in r_tk]) & TKTYPE_WITH_PROBE): 
        if days == 0:
            probe_code = '00110C'
        elif is_cont: 
            probe_code = '00158C'
        else:
            probe_code = '00109C'
        
        amount_probe = get_price('ord', probe_code, dt)
        
        # XXX 12/20/12 21:26:53 101.09 起外科專科醫師診療費加成 9%
        if dt[:5] >= '10109':
            amount_probe = int(round(amount_probe * 1.09))
    else:
        probe_code = ''
        amount_probe = 0
       
    amount_pharmacy = 0 # XXX get_price('ord', pharmacy_code, dt)
    amount_charged = amount_tk + amount_selfpay
    amount_all = amount_ord + amount_med + amount_probe + amount_pharmacy  
    amount_app = amount_all - amount_selfpay
   
    if is_app:
        if probe_code: # XXX 08/31/11 15:04:29 
                       # B6 case which has no probe_code will add an empty line
            n_p13 += 1
            l_pdata.append(''.join([
                tag('p2', '1'),             #p2  醫令調劑方式
                tag('p3', '0'),             #p3  醫令類別
                tag('p4', probe_code),      #p4  藥品(項目)代號
                tag('p8',  100),            #p8  支付成數
                tag('p10', 1),              #p10 總量
                tag('p11', amount_probe),   #p11 單價
                tag('p12', amount_probe),   #p12 點數
                tag('p13', n_p13),          #p13 醫令序
            ]))

        pdata = ''.join(['<pdata>%s</pdata>' % pd for pd in l_pdata])

        dhead = ''.join([
            tag('d1', insttype_code),       #d1  案件分類
            tag('d2', nr),                  #d2  流水編號
        ])

        # XXX dbody
        dbody = ''.join([
            tag('d3', pid),                 #d3  身分證統一編號
            tag('d4', specord_code),        #d4  特定治療項目代號(一)
                                            #d5  特定治療項目代號(二)
                                            #d6  特定治療項目代號(三)
                                            #d7  特定治療項目代號(四)
            tag('d8', dept),                #d8  就醫科別
            tag('d9', dt[:7]),              #d9  就醫日期
            tag('d10', dt_end[:7]),         #d10 治療結束日期
            tag('d11', birthday),           #d11 出生年月日
                                            #d12 補報原因註記
                                            #d13 整合式照護計畫註記
            tag('d14', paytype_code),       #d14 給付類別
            tag('d15', selfpay_code),       #d15 部分負擔代號
                                        #d16 轉入或原處方或轉檢或代檢之註記
            tag('d17', trans_code),     #d17 轉入或原處方或轉檢或代檢之服務機構代號
            tag('d18', is_trans),           #d18 病患是否轉出
            icds_dbody,                     #d19 國際疾病分類號(一)
                                            #d20 國際疾病分類號(二)
                                            #d21 國際疾病分類號(三)
                                            #d22 國際疾病分類號(四)
                                            #d23 國際疾病分類號(五)
            tag('d24', surgery_code_main),  #d24 主手術代碼
            tag('d25', surgery_code_sub),   #d25 次手術代碼
                                            #d26 次手術代碼(二)
            tag('d27', days),               #d27 給藥日份
            tag('d28', OPREP_CODE),         #d28 處方調劑方式
            tag('d29', serial),             #d29 健保卡就醫序號
            tag('d30', doctor_pid),         #d30 診治醫師代號
            tag('d31', pharmacist_pid),     #d31 藥師代號
            tag('d32', amount_med),         #d32 用藥明細點數小計
            tag('d33', amount_ord),         #d33 診療明細點數小計
                                            #d34 特殊材料明細點數小計
            tag('d35', probe_code),         #d35 診察費項目代號
            tag('d36', amount_probe),       #d36 診察費點數
            tag('d37', pharmacy_code),      #d37 藥事服務費項目代號
            tag('d38', amount_pharmacy),    #d38 藥事服務費點數
            tag('d39', amount_all),         #d39 合計點數
            tag('d40', amount_selfpay, False), #d40 部分負擔點數
            tag('d41', amount_app),         #d41 申請點數
                                            #d42 論病例計酬代碼
            tag('d43', amount_agency),      #d43 行政協助費用點數
            tag('d44', days_cont),          #d44 慢性病連續處方箋有效期間總處方日份
                                            #d45 依附就醫新生兒出生日期
                                            #d46 急診治療起始時間
                                            #d47 急診治療結束時間
                                            #d48 醫療服務計畫代碼
            tag('d49', name),               #d49 姓名
        ])
        ddata = '<ddata><dhead>%s</dhead><dbody>%s%s</dbody></ddata>' % (dhead, dbody, pdata)

    return vars()

def xml_upload(cr, tk_id, datatype='1', dataformat='1'):
    x = '''<REC>
  <MSH>
    <A00>%(datatype)s</A00>
    <A01>%(dataformat)s</A01>
    <A02>1.0</A02>
  </MSH>
  <MB>
    <MB1>
      %(card_code)s
      <A12>%(pid)s</A12>
      <A13>%(birthday)s</A13>
      <A14>%(clinic_code)s</A14>
      <A15>%(doctor_pid)s</A15>
      %(sam_code)s
      <A17>%(dt)s</A17>
      %(serial)s
      <A19>%(amend_code)s</A19>
      %(newborn)s
      %(newbornmark)s
      %(sign)s
      <A23>%(tktype_code)s</A23>
      %(newbornprobe)s
      %(xml_diag)s
      <A31>%(amount_all)s</A31>
      <A32>%(amount_selfpay)s</A32>
    </MB1>
    %(xml_ord)s
    %(xml_med)s
  </MB>
</REC>'''
    
    record_upload = namedtuple('record_upload', 'card pid birthday sam dt serial amend newborn newbornmark sign tktype newbornprobe')
    rr = cr.execute('''select tk.card_code, 
                             patient.pid, 
                             patient.birthday, 
                             sam.code, 
                             tk.dt, 
                             tk.serial, 
                             amend.code, 
                             tk.newborn, 
                             tk.newbornmark, 
                             tk.sign,
                             tktype.code, 
                             tk.newbornprobe 
                             from tk 
                             join patient on tk.patient_id = patient.id 
                             join sam on tk.sam_id = sam.id 
                             join amend on tk.amend_id = amend.id 
                             join tktype on tk.tktype_id = tktype.id
                             where tk.id = ?''', (tk_id,)).fetchone()
    r = record_upload._make(rr) 
    card_code =  tag('A11', r.card)
    pid = r.pid
    birthday = r.birthday
    clinic_code = CLINIC_CODE
    doctor_pid = DOCTOR_PID
    sam_code = tag('A16', r.sam)
    dt = r.dt
    serial =  tag('A18', r.serial)
    amend_code = r.amend
    newborn = tag('A20', r.newborn)
    newbornmark = tag('A21', r.newbornmark)
    sign = tag('A22', r.sign)
    tktype_code = r.tktype
    newbornprobe = tag('A24', r.newbornprobe)
    d = attrs(cr, tk_id=tk_id, is_xml=True)
    amount_all = d['amount_all']
    amount_selfpay = d['amount_selfpay']
    xml_diag = d['xml_diag']
    xml_ord = d['xml_ord']
    xml_med = d['xml_med']

    return x % vars()

# ==============================================================================
#  threading foundation 
# ==============================================================================

class thread(QThread):

    def __init__(self, par=None):
        super(thread, self).__init__(par)
        self.stopped = False
        self.mtx = QMutex()
     
    def send(self, **d):
        self.emit(SIGNAL('msg_%s' % self.__class__.__name__), d)
    
    def go(self, **kw):
        self.end()
        d = locals()
        self = d.pop('self')
        for n, v in d['kw'].iteritems():
            setattr(self, n, v)
        self.start()

    def end(self):
        if self.isRunning():
            self.stop()
            self.wait()

    def stop(self):
        try:
            self.mtx.lock()
            self.stopped = True
            self.emit(SIGNAL('stopped'))
        finally:
            self.mtx.unlock()

    def is_stopped(self):
        try:
            self.mtx.lock()
            return self.stopped
        finally:
            self.mtx.unlock()

    def run(self):
        self.stopped = False
        self.process()
        self.stop()

    def log(self, s):
        self.emit(SIGNAL('status'), s)

    def process(self):
        pass

def mid(buf, i, n):
    return str(buf.raw)[i - 1 : i - 1 + n]

class dll(thread):

    def __init__(self, par=None):
        super(dll, self).__init__(par)

    def reset(self):
        for i in ['f', 'kw', 'f_next', 'kw_next', 'var']:
            try:
                delattr(self, i)
            except:
                pass

    def process(self):
        f = getattr(self, self.f)
        kw = getattr(self, 'kw', {})
        f_next = getattr(self, 'f_next', '')
        kw_next = getattr(self, 'kw_next', {})
        var = getattr(self, 'var', {})

        try:        
            result = f(**kw) 
        
        except:
            result = None

        finally:
            logger.info('self.send(f=%s, kw=%s, result=%s, f_next=%s, kw_next=%s, var=%s)\n' % (self.f, kw, result, f_next, kw_next, var))
            self.send(f=self.f, kw=kw, result=result, f_next=f_next, kw_next=kw_next, var=var)
            self.reset()

    def init_com(self, port=0):
        global is_dll_ok, is_com_ok
        r = cs.csOpenCom(port)
        if r == 4000:
            is_com_ok = False
        return r

    def init_sam(self):
        global is_dll_ok, is_com_ok
        r = cs.csVerifySAMDC()
        if r == 4000:
            is_com_ok = False
        return r

    def update_hc(self): 
        global is_dll_ok, is_com_ok
        r = cs.csUpdateHCContents()
        if r == 4000:
            is_com_ok = False 
        return r

    def get_basic(self):
        t = []
        global is_dll_ok, is_com_ok
        if not is_dll_ok or not is_com_ok:
            return 4000, {}, t

        buf = create_string_buffer(78)
        r = cs.hisGetRegisterBasic(buf, byref(c_int(sizeof(buf))))
        if r == 0:
            l = [mid(buf, 1, 12), 
                 mid(buf, 13, 20).decode('big5'), 
                 mid(buf, 33, 10), 
                 mid(buf, 43, 7), 
                 mid(buf, 50, 1), 
                 mid(buf, 51, 7), 
                 mid(buf, 58, 1), 
                 mid(buf, 59, 2), 
                 mid(buf, 61, 1), 
                 mid(buf, 62, 7), 
                 mid(buf, 69, 2), 
                 mid(buf, 71, 7), 
                 mid(buf, 78, 1)] 
            card_code, name, pid, birthday, gender, issue, valid, insurertype_code, state_code, expiry, avail, newborn, newbornmark = l 
            
            t.append(l)
            
            return r, {'card_code': card_code, 'name': name, 'pid': pid, 'birthday': birthday, 'insurertype_code': insurertype_code, 'state_code': state_code, 'newborn': newborn, 'newbornmark': newbornmark}, t 
       
        elif r == 4000:
            is_com_ok = False

        return r, {}, t

    def get_seq(self, amend_code='1', tktype_code='01', d=None):
        global is_dll_ok, is_com_ok
        if not is_dll_ok or not is_com_ok or d is None:
            return 4000, {}
        
        buf = create_string_buffer(296)
        r = cs.hisGetSeqNumber256(c_char_p(fl(tktype_code, 3)), 
                                  c_char_p(fl(d.get('newbornmark', ''), 2)), 
                                  c_char_p(fl(amend_code, 1)), 
                                  buf, byref(c_int(sizeof(buf))))
        if r == 0:
            d['tktype_code'] = tktype_code
            d['amend_code'] = amend_code
            d['dt'] = mid(buf, 1, 13)
            d['serial'] = mid(buf, 14, 4)
            d['sign'] = mid(buf, 28, 256)
            d['sam_code'] = mid(buf, 284, 12)

        elif r == 4000:
            is_com_ok = False

        return r, d

    def unget_seq(self, dt=''):
        global is_com_ok
        r = cs.csUnGetSeqNumber(c_char_p(dt))
        if r == 4000:
            is_com_ok = False
        return r

    def write(self, tk_id=0, amend_code='1'):
        global is_dll_ok, is_com_ok
        t = []
        if not is_dll_ok or not is_com_ok:
            return 4000, t

        cn = sqlite3.connect(DB)
        cr = cn.cursor()
        d = attrs(cr, tk_id=tk_id, is_ic=True)
        
        # XXX modified: \0 terminated strings
        r = cs.hisWriteTreatmentData(c_char_p(fl(d['dt'], 14, True)), 
                                     c_char_p(fl(d['pid'], 11, True)), 
                                     c_char_p(fl(d['birthday'], 8, True)), 
                                     c_char_p(''.join([fl(amend_code, 1), 
                                                       fl(d['icds_ic'], 30),
                                                       fl(d['amount_all'], 8),
                                                       fl(d['amount_selfpay'], 8),
                                                       fl(0, 8),
                                                       fl(0, 7),
                                                       fl(0, 7),])),
                                     c_char_p(fl(DOCTOR_PID, 11, True)))
        if r == 0:
            n = len(d['l_ic'])
            # XXX check item number 
            if 0 < n <= 60:
                buf = create_string_buffer(40 * n)
                r = cs.hisWriteMultiPrescriptSign(c_char_p(fl(d['dt'], 14, True)), 
                                                  c_char_p(fl(d['pid'], 11, True)), 
                                              c_char_p(fl(d['birthday'], 8, True)), 
                                                  c_char_p(''.join(d['l_ic'])), 
                                                  byref(c_int(n)),
                                                  buf,                         
                                                  byref(c_int(40 * n)))
                if r == 0:
                    s = mid(buf, 1, 40 * n)
                    signs = [s[40 * i: 40 * (i + 1)] for i in range(n)]    
                    for j, l in enumerate(d['l_ic_id']):
                        tbl, i1, i2 = l
                        t.append((tbl, signs[j], i1, i2)) 
                
                elif r == 4000:
                    is_com_ok = False
        
        elif r == 4000:
            is_com_ok = False
        
        return r, t

# =============================================================================
#  pdf printing 
# =============================================================================

try:
    import reportlab.rl_config
    reportlab.rl_config.warnOnMissingFontGlyphs = 0
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import mm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    pdfmetrics.registerFont(TTFont('wtm', 'WT021.TTF'))
    pdfmetrics.registerFont(TTFont('msjh', 'MSJH.ttf'))
    pdfmetrics.registerFont(TTFont('ming', 'mingliu.ttc'))
    A4_w, A4_h = 210, 297
except:
    # XXX 02/16/15 17:35:22 should do something...
    pass

# XXX better calling convention?
def print_proxy(arg):   

    def line(l, cv):
        cv.line(*tuple([l[0]*mm, (A4_h - l[1])*mm, l[2]*mm, (A4_h - l[3])*mm]))

    def text(s, cv, size=9, font='wtm', centered=False):
        cv.setFont(font, size)
        f = cv.drawCentredString if centered else cv.drawString        
        f(*(s[0]*mm, (A4_h - s[1])*mm, unicode(s[2])))

    def rect(s, cv, fill=0):
        cv.rect(s[0]*mm, (A4_h - s[1])*mm, 3*mm, 3*mm, fill=fill)

    def dtl_form(cv):
        cv.setLineWidth(0.1*mm)

        lines = [
            (8,   22,  26,  22),    
            (8,   40,  26,  40),
            (8,   22,  8,   40),
            (26,  22,  26,  40),    
            (31,  22,  201, 22),
            (31,  31,  201, 31),
            (31,  40,  201, 40),
            (31,  22,  31,  40),
            (39,  31,  39,  40),
            (60,  22,  60,  40),
            (117, 22,  117, 40),
            (143, 22,  143, 40),
            (179, 22,  179, 40),
            (201, 22,  201, 40), 
            (8,   47,  201, 47),
            (8,   276, 201, 276),
            (8,   47,  8,   276),
            (201, 47,  201, 276),
            (8,   56,  201, 56),
            (8,   65,  201, 65),
            (8,   74,  201, 74),
            (8,   83,  201, 83),
            (8,   92,  201, 92),
            (8,   101, 201, 101),
            (8,   110, 201, 110),
            (8,   125, 201, 125),
            (8,   132, 201, 132),
            (8,   139, 201, 139),
            (8,   146, 201, 146),
            (8,   153, 201, 153),
            (8,   160, 201, 160),
            (8,   167, 201, 167),
            (8,   174, 201, 174),
            (8,   181, 201, 181),
            (8,   188, 201, 188),
            (8,   195, 201, 195),
            (8,   204, 201, 204),
            (8,   213, 201, 213),
            (97,  222, 201, 222),
            (97,  231, 201, 231),
            (97,  240, 201, 240),
            (97,  249, 201, 249),
            (97,  258, 201, 258),
            (97,  267, 201, 267),
            (17,  47,  17,  195),
            (26,  110, 26,  195),
            (50,  110, 50,  195),
            (63,  65,  63,  83),
            (63,  92,  63,  101),
            (72,  65,  72,  74),
            (72,  92,  72,  101),
            (81,  110, 81,  195),
            (97,  47,  97,  74),
            (97,  101, 97,  195),
            (97,  213, 97,  276),
            (106, 47,  106, 83),
            (106, 101, 106, 110),
            (113, 213, 113, 249),
            (121, 110, 121, 195),
            (137, 110, 137, 195),
            (149, 47,  149, 74),
            (153, 110, 153, 195),
            (158, 47,  158, 74),
            (169, 110, 169, 276),
            (185, 110, 185, 276),       
        ]
        for s in lines:
            line(s, cv)

        s9 = [
            (14,   27.5,   u'流水號'),
            (39,   27.5,   u'資 料 格 式'),
            (69,   27.5,   u'特約醫事服務機構或調劑機構'),
            (123,  27.5,   u'費 用 年 月'),
            (150,  27.5,   u'申   報   類   別'),
            (153,  36.5,   u'送核'),
            (167,  36.5,   u'補送'),
            (182,  27.5,   u'案 件 分 類'),
            (19,   52.5,   u'特定治療項目代號：'),
            (108,  52.5,   u'姓名：'),
            (160,  52.5,   u'就醫科別：'),
            (19,   61.5,   u'就醫日期：'),
            (108,  61.5,   u'生日：'),
            (160,  61.5,   u'身份證號：'),
            (19,   70.5,   u'健保卡就醫序號：'),
            (74,   70.5,   u'給付類別：'),
            (108,  70.5,   u'部分負擔代碼：'),
            (160,  70.5,   u'轉入之院所代碼：'),
            (19,   79.5,   u'病患是否轉出：'),
            (47,   79.5,   u'是'),
            (57,   79.5,   u'否'),
            (77,   79.5,   u'國際疾病分類號碼'),
            (19,   88.5,   u'主手術代號（一）：'),
            (74,   88.5,   u'傷病名稱及主要症候：'),
            (19,   97.5,   u'給藥日份：'),
            (74,   97.5,   u'處方：'),
            #(91,  97.5,   u'自行調劑'),
            #(111, 97.5,   u'交付調劑'),
            #(131, 97.5,   u'未開處方'),
            (91,   97.5,   u'交付調劑'),  
            (19,   106.5,  u'次手術代號（二）：'),
            (108,  106.5,  u'慢性病連續處方籤有效期間總處方日份：'),
            (8.5,  118.5,  u'調 劑'),
            (8.5,  122.5,  u'方 式'),
            (17.5, 118.5,  u'醫 令'),
            (17.5, 122.5,  u'類 別'),
            (30,   118.5,  u'藥 品 代 號'),
            (30,   122.5,  u'項 目 代 號'),
            (54.5, 114.5,  u'診  療  項  目'),
            (52.5, 118.5,  u'或 藥 品 、 材 料'),
            (54.5, 122.5,  u'名  稱  規  格'),
            (83,   118.5,  u'藥品用量'),
            (83,   122.5,  u'診療部位'),
            (100,  118.5,  u'藥品使用頻率'),
            (100,  122.5,  u'診療支付成數'),
            (123,  118.5,  u'給藥途徑'),
            (123,  122.5,  u'作用部位'),
            (145,  118.5,  u'總量'),
            (161,  118.5,  u'單價'),
            (177,  118.5,  u'金額'),
            (187,  118.5,  u'審 查 欄'),
            (19,   200.5,  u'藥  費  小  計'),
            (19,   209.5,  u'診  療  及  材  料  金  額  小  計'),
            (19,   231.5,  u'診治醫師'),
            (19,   235.5,  u'代號：'),
            (19,   255.5,  u'診治醫師'),
            (19,   259.5,  u'簽章：'),
            (59,   231.5,  u'調劑藥師（藥劑生）'),
            (59,   235.5,  u'代號：'),
            (59,   255.5,  u'調劑藥師（藥劑生）'),
            (59,   259.5,  u'簽章：'),
            (99,   218.5,  u'項目代號'),
            (120,  218.5,  u'項     目     名     稱'),
            (170.5,218.5,  u'金    額'),
            (187,  218.5,  u'審 查 欄'),
            (131,  227.5,  u'診察費'),
            (131,  236.5,  u'藥事服務費'),
            (131,  245.5,  u'代辦費'),
            (112,  254.5,  u'合  計  金  額'),
            (112,  263.5,  u'部  分  負  擔  金  額'),
            (112,  272.5,  u'申  請  金  額')
        ]
        for s in s9:
            text(s, cv)

        s_n = [
            (10,   27.5,   u'6'),
            (33,   27.5,   u'1'),
            (62,   27.5,   u'2'),
            (119,  27.5,   u'3'),
            (145,  27.5,   u'4'),
            (180,  27.5,   u'5'),
            (11,   52.5,   u'7'),
            (100,  52.5,   u'8'),
            (152,  52.5,   u'9'),
            (10,   61.5,   u'10'),
            (99,   61.5,   u'11'),
            (151,  61.5,   u'12'),
            (10,   70.5,   u'13'),
            (65,   70.5,   u'14'),
            (99,   70.5,   u'15'),
            (151,  70.5,   u'16'),
            (10,   79.5,   u'17'),
            (65,   79.5,   u'18～20'),
            (10,   88.5,   u'21'),
            (10,   97.5,   u'22'),
            (65,   97.5,   u'23'),
            (10,   106.5,  u'24'),
            (99,   106.5,  u'25'),
            (8.5,  114.5,  u'A8'),
            (17.5, 114.5,  u'A9'),
            (30,   114.5,  u'A10'),
            (83,   114.5,  u'A11a,b'),
            (100,  114.5,  u'A11a,b'),
            (123,  114.5,  u'A11a,b'),
            (138.5,118.5,  u'A12'),
            (154.5,118.5,  u'A13'),
            (170.5,118.5,  u'A14'),
            (10,   200.5,  u'28'),
            (10,   209.5,  u'29'),
            (10,   231.5,  u'25'),
            (50,   231.5,  u'26'),
            (99,   227.5,  u'29-1'),
            (99,   236.5,  u'30-1'),
            (99,   245.5,  u'34-1'),
            (100,  254.5,  u'31'),
            (100,  263.5,  u'32'),
            (100,  272.5,  u'33')
        ]
        for s in s_n:
            text(s, cv, font='msjh')

        text((105, 19, u'中 央 健 康 保 險 局 特 約 醫 事 服 務 機 構 門 診 醫 療 服 務 點 數 及 醫 令 清 單'), cv, size=13, centered=True)

    def dtl(d, cv):
        dtl_form(cv)

        s9 = [
            (33,   36.5,  u'11'), 
            (40,   36.5,  u'門診費用明細'),        # 資料格式
            (68,   36.5,  d['clinic_code']), 
            (91,   36.5,  CLINIC_NAME),            # 特約醫事服務機構
            (14,   36.5,  d['nr']),                # 流水號
            (123,  36.5,  d['ym']),                # 費用年月
            (188,  36.5,  d['insttype_code']),     # 申報類別
            (49,   52.5,  d['specord_code']),      # 特定治療項目代號 
            (118,  52.5,  d['name']),              # 姓名
            (177,  52.5,  d['dept']),              # 就醫科別
            (36,   61.5,  d['dt_pr']),             # 就醫日期
            (118,  61.5,  dt_s(d['birthday'], True)),# 生日
            (177,  61.5,  d['pid']),               # 身份證號
            (45,   70.5,  d['serial']),            # 健保卡就醫序號
            (90,   70.5,  d['paytype_code']),      # 給付類別
            (131,  70.5,  d['selfpay_code']),      # 部分負擔代碼
            (185,  70.5,  d['trans_code']),        # 轉入之院所代碼    
            (108,  79.5,  d['icds_code']),         # 國際疾病分類號碼
            (49,   88.5,  d['surgery_code_main']), # 主手術代號（一）
            (106,  88.5,  d['icds_name']),         # 傷病名稱及主要症候
            (36,   97.5,  d['days']),              # 給藥日份
            (48,   106.5, d['surgery_code_sub']),  # 次手術代號（二）
            (166,  106.5, d['days_cont']),         # 慢性病連續處方籤有效期間總處方日份
            (170.5,200.5, d['amount_med']),        # 藥費小計
            (170.5,209.5, d['amount_ord']),        # 診療及材料金額小計
            (29,   235.5, d['doctor_pid']),        # 診治醫師代號
            (29,   259.5, d['doctor_name']),       # 診治醫師簽章
            (59,   235.5, d['pharmacist_pid']),    # 調劑藥師（藥劑生）代號
            (59,   259.5, d['pharmacist_name']),   # 調劑藥師（藥劑生）簽章
            (170.5,227.5, d['amount_probe']),      # 診察費
            (170.5,236.5, d['amount_pharmacy']),   # 藥事服務費
            (170.5,245.5, d['amount_agency']),     # 代辦費
            (170.5,254.5, d['amount_all']),        # 合計金額
            (170.5,263.5, d['amount_selfpay']),    # 部分負擔金額
            (170.5,272.5, d['amount_app']),        # 申請金額
        ]
        
        rect((42, 80), cv)
        rect((52, 80), cv, fill=1)
        
        rect((86, 98), cv, fill=1)
        
        #rect((106, 98), cv)
        #rect((126, 98), cv)

        rect((148, 37), cv, fill=1)
        rect((162, 37), cv)

        for i_, r in enumerate(d['l_ord']):
            i = i_ % 10
            if i == 0 and i_:
                for s in s9:
                    text(s, cv, font='msjh')
                s9 = []
                cv.showPage()
                text((184, 14, u'（續  頁）'), cv, size=11)
                dtl_form(cv)
            
            s9.extend([(j, 129.5 + i * 7, r[n]) for n, j in enumerate([10, 20, 28.5, 51, 83, 100, 123, 138.5, 154.5, 170.5])])
        for s in s9:
            text(s, cv, font='msjh')
        
    def chk_form(cv, scale=(1, 1), translation=(0, 0)):
        cv.setLineWidth(0.1*mm)
        cv.translate(*(t*mm for t in translation))
        cv.scale(*scale)

        h_lines = [
            (5, 16, 205, 16),
            (5, 92, 205, 92),
            (5, 20, 205, 20),
            (5, 24, 205, 24),
            (5, 28, 205, 28),
            (5, 32, 205, 32),
            (5, 80, 205, 80),        
        ]
        v_lines = [
            (5,   16, 5,   24),
            (5,   16, 5,   92),
            (71,  16, 71,  24),
            (138, 16, 138, 28),
            (175, 28, 175, 80),
            (190, 28, 190, 80),
            (205, 16, 205, 92),
        ]
        for s in (h_lines, v_lines):
            for i in s:
                line(i, cv)
        s9 = [
            (6,   19,  u'患者姓名：'),
            (72,  19,  u'身份證號：'), 
            (139, 19,  u'出生日期：'), 
            (6,   23,  u'就醫序號：'),
            (72,  23,  u'就醫日期：'),
            (139, 23,  u'案件分類：'),
            (6,   27,  u'主要症候：'),
            (139, 27,  u'疾病分類：'),      
            (176, 31,  u'總 數 量'),
            (191, 31,  u'備    註'),
            (6,   83,  u'醫 院 診 所 核 章'),
        ]
        for s in s9:
            text(s, cv)
              
        text((105, 9, u'全  民  健  康  保  險  門  診  交  付  檢  驗  項  目  明  細'), cv, size=14, centered=True)
        text((90, 31, u'檢           驗           代           碼           與           項           目           名           稱'), cv, size=9, centered=True)
        
    def chk(d, cv):
        chk_form(cv, translation=(0, 5))

        s9 = [
            (22,  19, d['name']),                   # 患者姓名
            (88,  19, d['pid']),                    # 身份證號 
            (155, 19, dt_s(d['birthday'], True)),   # 出生日期 
            (22,  23, d['serial_s']),               # 就醫序號
            (88,  23, d['dt_pr']),                  # 就醫日期
            (155, 23, d['insttype_code']),          # 案件分類
            (23,  27, d['icds_name']),              # 主要症候
            (155, 27, d['icds_code']),              # 疾病分類  
        ]
        for s in s9:
            text(s, cv, font='msjh')

        s_i = [
            (138, 87, spaced_s(CLINIC_NAME, ' '*2)), 
            (148, 91, spaced_s(CLINIC_ADDRESS)),
        ]
        for s in s_i:
            text(s, cv)

        s_n = [
            (177, 87, spaced_s(CLINIC_TEL)), 
            (138, 91, spaced_s(CLINIC_ZIP))
        ]
        for i_, t in enumerate(d['l_chk']):
            i = i_ % 12
            if i == 0 and i_:
                for s in s_n:
                    text(s, cv, font='msjh')
                s_n = []
                cv.showPage()
                text((184, 14, u'（續  頁）'), cv, size=11)
                chk_form(cv)
            
            s_n.extend([(j, 35 + i*4, t[n]) for n, j in enumerate([6, 176])])
        for s in s_n:
            text(s, cv, font='msjh')
        
        s14 = [(60, 14, spaced_s(CLINIC_NAME, ' '*2))]
        s14_ = [(115, 14, CLINIC_CODE)]
        for s in s14:
            text(s, cv, size=14)
        for s in s14_:
            text(s, cv, size=14, font='msjh')

    def prscr_form(cv, scale=(1, 1), translation=(0, 0)):
        cv.setLineWidth(0.1*mm)
        cv.translate(*(t*mm for t in translation))
        cv.scale(*scale)

        h_lines = [
            (5, 16, 205, 16),
            (5, 20, 205, 20),
            (5, 24, 205, 24),
            (5, 28, 205, 28),
            (5, 32, 205, 32),
            (5, 72, 205, 72),        
            (5, 92, 205, 92),
        ]
        v_lines = [
            (5,   16, 5,   92),
            (71,  16, 71,  24),
            (138, 16, 138, 72),
            (175, 28, 175, 72),
            (190, 28, 190, 72),
            (34,  72, 34,  92),
            (63,  72, 63,  92),
            (92,  72, 92,  92),
            (121, 72, 121, 92),
            (149, 72, 149, 92),
            (177, 72, 177, 92),
            (205, 16, 205, 92),
        ]
        for s in (h_lines, v_lines):
            for i in s:
                line(i, cv)
        
        s9 = [
            (10,  9,   u'一般處方籤'),
            (10,  14,  u'連續處方籤'),
            (6,   19,  u'患者姓名：'),
            (72,  19,  u'身份證號：'), 
            (139, 19,  u'出生日期：'), 
            (6,   23,  u'就醫序號：'),
            (72,  23,  u'就醫日期：'),
            (139, 23,  u'給藥日份：'),
            (6,   27,  u'主要症候：'),
            (139, 27,  u'疾病分類：'),      
            (139, 31,  u'用   量   及   用   法'),
            (176, 31,  u'總 數 量'),
            (191, 31,  u'備    註'),
            (6,   75,  u'診治醫師代號簽章'),
            (36,  75,  u'處方醫院診所核章'),
            (65,  75,  u'調劑藥師代號簽章'),
            (65,  91,  u'調劑日期：'),
        ]
        for s in s9:
            text(s, cv)

        s11 = [
            (106, 84, '1'),
            (136, 84, '2'),
            (163, 84, '3'),
            (191, 84, '4')
        ]
        for s in s11:
            text(s, cv, size=11, centered=True, font='msjh')
        
        text((105, 9, u'全  民  健  康  保  險  門  診  交  付  調  劑  處  方  籤'), cv, size=14, centered=True)
        text((73, 31, u'藥      品      名      稱      及      規      格  （ 劑    型   、   劑    量 ）'), cv, size=9, centered=True) 

    def prscr(d, cv):
        prscr_form(cv, translation=(0, 5))

        s9 = [
            (22,  19, d['name']),                   # 患者姓名
            (88,  19, d['pid']),                    # 身份證號 
            (155, 19, dt_s(d['birthday'], True)),   # 出生日期 
            (22,  23, d['serial_s']),               # 就醫序號
            (88,  23, d['dt_pr']),                  # 就醫日期
            (155, 23, d['days']),                   # 給藥日份
            (22,  27, d['icds_name']),              # 主要症候
            (155, 27, d['icds_code']),              # 疾病分類
        ]
        for s in s9:
            text(s, cv, font='msjh')

        s_n = []
        for i_, m in enumerate(d['l_med']):
            i = i_ % 10
            if i == 0 and i_:
                for s in s_n:
                    text(s, cv, font='msjh')
                s_n = []
                cv.showPage()
                text((184, 14, u'（續  頁）'), cv, size=11)
                prscr_form(cv)

            s_n.extend([(j, 35 + 4 * i, m[n]) for n, j in enumerate([6, 139, 176])])
        for s in s_n:
            text(s, cv, font='msjh')

        fill_2 = d['is_cont']
        fill_1 = 0 if fill_2 else 1
        rect((5, 9.5), cv, fill=fill_1)
        rect((5, 14.5), cv, fill=fill_2)

        s14 = [(60, 14, spaced_s(CLINIC_NAME, '  '))]
        s14_ = [(115, 14, CLINIC_CODE)]
        for s in s14:
            text(s, cv, size=14)
        for s in s14_:
            text(s, cv, size=14, font='msjh')

    def rcpt_form(cv, scale=(1, 1), translation=(0, 0)):
        cv.setLineWidth(0.1*mm)
        cv.translate(*(t*mm for t in translation))
        cv.scale(*scale)
        
        h_lines = [
            (5,   16, 205, 16),
            (5,   92, 205, 92),
            (5,   16, 5,   92),
            (205, 16, 205, 92),
            (5,   20, 205, 20),
            (5,   24, 205, 24),
            (5,   72, 205, 72),
            (5,   76, 205, 76),
            (5,   80, 205, 80),
        ]
        v_lines = [
            (45,  16, 45,  20),
            (85,  16, 85,  20),
            (115, 16, 115, 20),
            (145, 16, 145, 20),
            (175, 20, 175, 72),
            (190, 20, 190, 76),
            (71,  76, 71,  80),
            (138, 76, 138, 80),
        ]
        for s in (h_lines, v_lines):
            for i in s:
                line(i, cv)

        s9 = [
            (6,   19, u'姓名：'),
            (46,  19, u'身份證號：'), 
            (86,  19, u'生日：'), 
            (116, 19, u'就醫序號：'),
            (146, 19, u'就醫日期：'),
            (176, 23, u'數    量'),
            (191, 23, u'金    額'),
            (6,   79, u'療程掛號費用總計：'),
            (72,  79, u'部分負擔費用總計：'),
            (139, 79, u'療程實收費用總計：'),
            (6,   91, u'列  印  日  期  ：  中  華  民  國       年     月     日'),
            (138, 91, u'統    一    編    號')
        ]
        for s in s9:
            text(s, cv)

        text((105, 9, u'全  民  健  康  保  險  門  診  治  療  明  細  及  收  據'), cv, size=14, centered=True)
        text((6, 23, u'處        置        項        目        及        計        價        藥        品        名        稱'), cv, size=9)
        text((6, 75, u'處       置       項       目       及       計       價       藥       品       費       用       總       計'), cv, size=9)
        
    def rcpt(d, cv):
        rcpt_form(cv, translation=(0, 5))
        
        s9 = [
            (16,  19, d['name']),                 # 姓名
            (62,  19, d['pid']),                  # 身份證號 
            (96,  19, dt_s(d['birthday'], True)), # 生日 
            (132, 19, d['serial_s']),             # 就醫序號     
            (162, 19, d['dt_pr']),                # 就醫日期
            (35,  79, d['amount_tk']),            # 療程掛號費用總計 
            (101, 79, d['amount_selfpay']),       # 部分負擔費用總計 
            (168, 79, d['amount_charged']),       # 療程實收費用總計 
            (63,  91, dt_now().year - 1911),      # 列印年
            (77,  91, dt_now().month),            # 列印月
            (87.5,91, dt_now().day),              # 列印日
        ]
        for s in s9:
            text(s, cv, font='msjh')

        s_n = [
            (177, 83, spaced_s(CLINIC_TEL)), 
            (138, 87, spaced_s(CLINIC_ZIP)),
            (183, 91, spaced_s(CLINIC_TAX_NR)),
        ]   
        total = 0
        for i_, r in enumerate(d['l_charged']):
            i = i_ % 12
            if i == 0 and i_:
                for s in s_n:
                    text(s, cv, font='msjh')
                s_n = []
                cv.showPage()
                text((184, 14, u'（續  頁）'), cv, size=11)
                rcpt_form(cv)
        
            s_n.extend([(j, 27 + 4*i, r[n]) for n, j in enumerate([6, 176, 191])])
            total += r[2]

        s_n.extend([(191, 75, total)]) # 處置項目及計價藥品費用總計
        
        for s in s_n:
            text(s, cv, font='msjh')
        
        s_i = [(138, 83, spaced_s(CLINIC_NAME, ' '*2)),
               (148, 87, spaced_s(CLINIC_ADDRESS)),]    
        for s in s_i:
            text(s, cv)
        
        s14 = [(60, 14, spaced_s(CLINIC_NAME, ' '*2))]
        s14_ = [(115, 14, CLINIC_CODE)]
        for s in s14:
            text(s, cv, size=14)
        for s in s14_:
            text(s, cv, size=14, font='msjh')

    def rcptn_form(cv, scale=(1, 1), translation=(0, 0)):
        cv.setLineWidth(0.1*mm)
        cv.translate(*(t*mm for t in translation))
        cv.scale(*scale)

        h_lines = [
            (5, 16, 205, 16),
            (5, 20, 205, 20),
            (5, 24, 205, 24),
            (5, 28, 205, 28),
            (5, 32, 205, 32),
            (5, 36, 205, 36),
            (5, 40, 205, 40),
            (5, 44, 205, 44),
            (5, 48, 205, 48),
            (5, 52, 205, 52),
            (5, 56, 205, 56),
            (5, 60, 205, 60),
            (5, 64, 205, 64),
            (5, 68, 205, 68),
            (5, 72, 205, 72),
            (5, 76, 205, 76),
            (5, 80, 205, 80),
            (5, 92, 205, 92),
        ]
        v_lines = [
            (5,   16, 5,   92),
            (71,  16, 71,  32),
            (138, 16, 138, 32),
            (55,  32, 55,  80),
            (105, 32, 105, 80),
            (155, 32, 155, 80),
            (205, 16, 205, 92),
        ]
     
        for s in (h_lines, v_lines):
            for i in s:
                line(i, cv)

        s9 = [
            (6,   19, u'病患姓名：'),
            (72,  19, u'身份證號：'), 
            (139, 19, u'出生日期：'),
            (6,   23, u'性別：'),
            (72,  23, u'就診日期：'),
            (139, 23, u'就醫身份別：'),
            (6,   27, u'健保卡就醫序號：'),
            (72,  27, u'部份負擔代號：'),
            (139, 27, u'就醫科別：'),
            (6,   31, u'診別：'),
            (72,  31, u'醫師姓名：'),
            (139, 31, u'病歷號碼：'),
            (6,   35, u'健保申報項目'),
            (56,  35, u'點數'),
            (106, 35, u'自付費用項目'),
            (156, 35, u'金額'),
            (6,   39, u'診察費'),
            (106, 39, u'掛號費'),
            (6,   43, u'藥費'),
            (106, 43, u'部份負擔'),
            (6,   47, u'藥事服務費'),
            (106, 47, u'基本部份負擔'),
            (6,   51, u'注射費'),
            (106, 51, u'藥品部份負擔'),
            (6,   55, u'檢驗費'),
            (106, 55, u'復健部份負擔'),
            (6,   59, u'檢查費'),
            (106, 59, u'檢驗檢查'),
            (6,   63, u'處置手術費'),
            (106, 63, u'藥品'),
            (6,   67, u'材料費'),
            (106, 67, u'衛材'),
            (6,   71, u'健保申報點數'),
            (106, 71, u'部份負擔金額'),
            (106, 75, u'其他自費金額'),
            (6,   79, u'應繳金額'),
            (106, 79, u'收款人'),
            (6,   87, spaced_s(u'醫療機構代碼', ' '*2)),
            ]
        for s in s9:
            text(s, cv)

        text((105, 13, spaced_s(u'%s門診醫療費用收據' % CLINIC_NAME)), cv, 
             size=14, centered=True)
        
    def rcptn(d, cv):
        rcptn_form(cv, translation=(0, 8))

        s9 = [
            (22,  19, d['name']),                 # 病患姓名 
            (88,  19, d['pid']),                  # 身份證號 
            (155, 19, dt_s(d['birthday'], True)), # 出生日期 
            (16,  23, gender(d['pid'], False)),   # 性別
            (88,  23, d['dt_pr']),                # 就診日期
            (158, 23, d['state_code']),           # 就醫身份別
            (32,  27, d['serial_s']),             # 健保卡就醫序號
            (94,  27, d['selfpay_code']),         # 部份負擔代號 
            (155, 27, d['dept']),                 # 就醫科別
            (16,  31, ''),                        # 診別         XXX
            (88,  31, d['doctor_name']),          # 醫師姓名
            (155, 31, ''),                        # 病歷號碼     XXX
            (56,  39, d['amount_probe']),         # 診察費
            (156, 39, d['amount_tk']),            # 掛號費
            (56,  43, d['amount_med']),           # 藥費
            (56,  47, ''),                        # 藥事服務費   XXX
            (156, 47, d['amount_selfpay']),       # 基本部份負擔
            (56,  51, ''),                        # 注射費       XXX
            (156, 51, ''),                        # 藥品部份負擔 XXX
            (56,  55, ''),                        # 檢驗費       XXX
            (156, 55, ''),                        # 復健部份負擔 XXX
            (56,  59, ''),                        # 檢查費       XXX
            (156, 59, ''),                        # 檢驗檢查     XXX
            (56,  63, d['amount_ord']),           # 處置手術費   XXX
            (156, 63, ''),                        # 藥品         XXX
            (56,  67, ''),                        # 材料費       XXX
            (156, 67, ''),                        # 衛材         XXX
            (56,  71, d['amount_app']),           # 健保申報點數
            (156, 71, d['amount_selfpay']),       # 部份負擔金額 
            (156, 75, ''),                        # 其他自費金額 XXX
            (56,  79, d['amount_charged']),       # 應繳金額
        ]
        for s in s9:
            text(s, cv, font='msjh')

        s_n = [
            (45, 83, spaced_s(CLINIC_TEL)), 
            (46, 87, spaced_s(CLINIC_CODE)),
            (6,  91, spaced_s(CLINIC_ZIP)),
        ]   
        
        for s in s_n:
            text(s, cv, font='msjh')
        
        s_i = [(6,  83, spaced_s(CLINIC_NAME, ' '*2)),
               (16, 91, spaced_s(CLINIC_ADDRESS)),]    
        for s in s_i:
            text(s, cv)

    def final(fi, fo):
        cv = canvas.Canvas(fo)
        o = cv.beginText()
        o.setTextOrigin(0*mm, A4_h*mm)
        o.setFont('ming', 10)
        for l in codecs.open(fi, 'r', 'big5'):
            o.textLine(l.replace('\n', ''))
        cv.drawText(o)
        cv.save()
    
    # XXX better calling schemes?
    if len(arg) == 2:
        vars()['final'](*arg)

    else:
        typ, d, b = arg
        if d['has_%s' % typ]:
            f = cat(TMP, typ + '_%s_%s.pdf' % d['s_pdf'])
            cv = canvas.Canvas(f)
            vars()[typ](d, cv)
            cv.save()
            if b:
                pdf_print(f)

def printf(typ, tk_id, par):
    inst_id = 0
    if typ in ('rcptn', 'dtl'):
        if qna(par, u'選擇%s列印模式' % zh(typ), u'%s列印：列印整個案件，或是僅列印此次掛號內容？\n\n選擇 [Yes] 列印整個案件，[No] 僅列印此次掛號內容！' % zh(typ)) == QMessageBox.Yes:
            r = cr.execute('select inst_id from tk where id = ?', 
                           (tk_id,)).fetchone()
            if r:
                inst_id = r[0]                

    d = attrs(cr, tk_id=tk_id, inst_id=inst_id)
    print_proxy((typ, d, True))

# ==============================================================================
#  threading classes
# ==============================================================================

class refresher(thread):
    
    def __init__(self, par=None):
        super(refresher, self).__init__(par)
    
    def process(self):
        cn = sqlite3.connect(DB)
        cr = cn.cursor()
        log = self.log
        
        #tic = dt_now() 
        #log(u'開始 %s 掛號紀錄整理！現在時刻： %s' % (self.dt, dt_s(now())))
        r = cr.execute('''select tk.id, 
                                 patient.name, 
                                 patient.pid, 
                                 patient.birthday, 
                                 tk.dt, 
                                 tk.serial, 
                                 insttype.code, 
                                 tk.sign, 
                                 amend.code, 
                                 tktype.code, 
                                 tk.inst_id,
            (exists (select 1 from tk_diag where tk_diag.tk_id = tk.id) and 
             (exists (select 1 from tk_ord where tk_ord.tk_id = tk.id) or 
              exists (select 1 from tk_med where tk_med.tk_id = tk.id))),
(not exists (select 1 from tk_ord where tk_ord.tk_id = tk.id and tk_ord.sign = "") 
and not exists (select 1 from tk_med where tk_med.tk_id = tk.id and tk_med.sign = ""))
                                 from tk 
                                 join inst on tk.inst_id = inst.id 
                                 join patient on tk.patient_id = patient.id 
                                 join amend on tk.amend_id = amend.id 
                                 join tktype on tk.tktype_id = tktype.id 
                                 join insttype on inst.insttype_id = insttype.id 
                                 where tk.dt like ? 
                                 order by tk.dt''', (self.dt + '%',)).fetchall()
                    
        #toc = dt_now()
        #log(u'掛號紀錄整理結束！歷時： %s' % t_n(toc - tic))
            
        self.emit(SIGNAL('done'), r)

class applier(thread):
    
    def __init__(self, par=None):
        super(applier, self).__init__(par)
         
    def process(self):        
        cn = sqlite3.connect(DB)
        cr = cn.cursor()
        td = tempfile.mkdtemp(dir=TMP)
        log = self.log
        reader_dll = cat(os.getcwd(), 'Reader.dll')

        def cls():
            shutil.rmtree(td)            
     
        def abort():
            log(u'終止申報作業！')
            cls()
        
        #def del_app_db(serial):
        #    try:
        #        r = cr.execute('select id from app where serial= ?', 
        #                       (serial,)).fetchone()
        #        if r:
        #            app_id = r[0]
        #            cr.execute('delete from inst_app where app_id = ?', (app_id,))
        #            cr.execute('delete from app where id = ?', (app_id,))
        #            cn.commit()
        #        return True
        #
        #    except:
        #        cn.rollback()
        #        return False
        
        hosp_data_type = '11'  # 醫事類別：西醫門診
        appl_type = '1'        # 申報類別：送核
        month_mark = '3'       # 月份註記：全月
        chi_type = 'B'         # 中文碼：XML-> B

        typ = getattr(self, 'typ', 'apply')
        if typ == 'apply':
            tic = dt_now()
            n_inst, n_selfpay, amount_app_all, amount_selfpay_all = 0, 0, 0, 0
            l_ddata, l_app = [], []
             
            for ct in INSTTYPE:
                if self.is_stopped():
                    abort()
                    return     
                
                # XXX [app criteria]
                #     serial != '' or sign != '' (but not both empty !!)
                #     diag > 0 and (#ord > 0 or #med > 0)
                r = cr.execute('''select inst.id, inst.insttype_id 
                                  from inst 
                                  join insttype on inst.insttype_id = insttype.id 
                                  where exists (
                   select 1 from tk where tk.inst_id = inst.id
                   and tk.dt like ?
                   and (tk.serial != "" or tk.sign != "") 
                   and not (tk.serial = "" and tk.sign = "")
                   and exists (select 1 from tk_diag where tk_diag.tk_id = tk.id)
                   and (exists (select 1 from tk_ord where tk_ord.tk_id = tk.id) or 
                        exists (select 1 from tk_med where tk_med.tk_id = tk.id)))
                                  and insttype.code = ?''', 
                                  (self.ym + '%', ct)).fetchall()
                n_typ = len(r)
                log(u'可申報之 %s 案件共 %s 件 ...' % (ct, n_typ))
                if not n_typ:
                    continue

                l1 = []
                for i, c in enumerate(r):
                    if self.is_stopped(): 
                        abort()
                        return
                    
                    g = attrs(cr, inst_id=c[0], ym=self.ym, nr=i+1, is_app=True)

                    l_app.append((c[0], c[1], i + 1))
                    n_inst += 1
                    amount_app_all += g['amount_app']
                    a_selfpay = g['amount_selfpay']
                    if a_selfpay:
                        amount_selfpay_all += a_selfpay 
                        n_selfpay += 1
                    # XXX 
                    l1.append(g['ddata'])
                l_ddata.append('\n'.join(l1))
             
            # XXX 
            tdata = ''.join([ 
                tag('t1', '10'),                #t1  資料格式
                tag('t2', CLINIC_CODE),         #t2  服務機構代號
                tag('t3', self.ym),             #t3  費用年月
                tag('t4', '2'),                 #t4  申報方式
                tag('t5', '1'),                 #t5  申報類別
                tag('t6', fl(now(), 7)),        #t6  申報日期
                                                #t7  西醫一般案件申請件數
                                                #t8  西醫一般案件申請點數
                tag('t9', n_inst),              #t9  西醫專案案件申請件數
                tag('t10', amount_app_all),     #t10 西醫專案案件申請點數
                                                #t11 洗腎案件申請件數
                                                #t12 洗腎案件申請點數
                                                #t13 精神疾病社區復健申請件數
                                                #t14 精神疾病社區復健申請點數
                                                #t15 結核病申請件數
                                                #t16 結核病申請點數
                tag('t17', n_inst),             #t17 西醫件數申請小計
                tag('t18', amount_app_all),     #t18 西醫申請點數小計
                                                #t19 牙醫一般案件申請件數
                                                #t20 牙醫一般案件申請點數
                                                #t21 牙醫專案案件申請件數
                                                #t22 牙醫專案案件申請點數
                                                #t23 牙醫申請件數小計
                                                #t24 牙醫申請點數小計
                                                #t25 中醫一般案件申請件數
                                                #t26 中醫一般案件申請點數
                                                #t27 中醫專案案件申請件數
                                                #t28 中醫專案案件申請點數
                                                #t29 中醫申請件數小計
                                                #t30 中醫申請點數小計
                                                #t31 預防保健申請件數
                                                #t32 預防保健申請點數
                                                #t33 慢性病連續處方調劑申請件數
                                                #t34 慢性病連續處方調劑申請點數
                                                #t35 居家照護申請件數
                                                #t36 居家照護申請點數
                tag('t37', n_inst),             #t37 申請件數總計
                tag('t38', amount_app_all),     #t38 申請點數總計
                tag('t39', n_selfpay, False),   #t39 部分負擔件數總計
                tag('t40', amount_selfpay_all, False), #t40 部分負擔點數總計
                                                #t41 本次連線申報起日期
                                                #t42 本次連線申報迄日期
                ])
            
            xml_app = u'''<?xml version="1.0" encoding="Big5"?>
<outpatient><tdata>%s</tdata>%s</outpatient>''' % (tdata, ''.join(l_ddata))

            log(u'製作申報檔案 ...')
            
            zip_ = cat(td, '%s.zip' % (CLINIC_CODE + hosp_data_type + self.ym + appl_type + month_mark + chi_type))
            zf = zipfile.ZipFile(zip_, mode='w', compression=zipfile.ZIP_DEFLATED)
            zf.writestr('TOTFA.xml', xml_app.encode('big5'))
            zf.close()

            if self.is_stopped():
                abort()
                return
             
            log(u'申報檔案製作完畢。上傳申報檔案中，請稍候 ...')
            
            buf_lid = create_string_buffer(12)
            buf_nid = create_string_buffer(12)
            r = eii.NHI_SendB(c_int(com_port), c_char_p(reader_dll), 
                              c_char_p(zip_), c_char_p('05'), buf_lid, buf_nid)
            if r != 0:
                log(u'無法上傳申報檔案！ [ %s %s ] ' % (r, error_eii(r)))
                cls()
                return
            
            lid = mid(buf_lid, 1, 13)
            nid = mid(buf_nid, 1, 13)
            toc = dt_now()

            log(u'申報檔案上傳成功！[ 序號：%s, %s ] 歷時： %s' % (lid, nid, t_n(toc - tic))) 
            log(u'儲存申報資料中，請稍候....') 
            cr.execute('insert into app (ym, serial) values (?, ?)', 
                       (self.ym, now()))
            app_id = cr.execute('select last_insert_rowid()').fetchone()[0]
            cr.executemany('''insert into inst_app 
                              (inst_id, app_id, insttype_id, nr) 
                              values (?, ?, ?, ?)''', 
                               ((i[0], app_id, i[1], i[2]) for i in l_app))
            cn.commit()                                 

        elif typ == 'query':

            qry = cat(td, 'qry')
            open(qry, 'w').write('\n'.join(['FEE_YM=%s' % self.ym, 
                                            'APPL_TYPE=%s' % appl_type, 
                                            'HOSP_DATA_TYPE=%s' % hosp_data_type, 
                                            'APPL_DATE=']))
            
            buf_lid = create_string_buffer(12)
            buf_nid = create_string_buffer(12)
            r = eii.NHI_DownloadB(c_int(com_port), c_char_p(reader_dll), 
                                  c_char_p(qry), c_char_p('03'), buf_lid, buf_nid)
            if r != 0:
                log(u'檢核結果無法查詢！[ %s %s ]' % (r, error_eii(r)))   
                cls()
                return

            log(u'檢核結果接收中，請稍候 ...')
            r = eii.NHI_GetB(c_int(com_port), c_char_p(reader_dll), buf_lid, buf_nid, c_char_p(tp))
            if r != 0:
                log(u'檢核結果接收失敗！[ %s %s ] ' % (r, error_eii(r)))
                cls()
                return

            log(u'檢核結果接收完畢，判斷申報是否成功中 ...')
            ## XXX Do something if it's wrong....
            #    f = fli[-1]
            #    fi = cat(td, 'final')
            #    fo = cat(TMP, 'final_%s.pdf' % self.ym)
            #    print_proxy((fi, fo))
            #    self.emit(SIGNAL('printf'), fo)
            #cls()

class uploader(thread):

    def __init__(self, par=None):
        super(uploader, self).__init__(par)
    
    def process(self):
        cn = sqlite3.connect(DB)
        cr = cn.cursor()
        td = tempfile.mkdtemp(dir=TMP)
        log = self.log
        
        def cls():
            shutil.rmtree(td)
        
        tic = dt_now()
        log(u'開始上傳作業！現在時刻： %s' % dt_s(now()))
        
        # XXX [upload criteria]
        #     unuploaded
        #     sign != '' (leave out abnormal ones) 
        #     #diag > 0 and (#ord > 0 or #med > 0 (with sign?))  
        r_tk = cr.execute('''select tk.id from tk 
            where tk.id not in (select tk_id from tk_upload)
            and exists (select 1 from tk_diag where tk_diag.tk_id = tk.id)
            and (exists (select 1 from tk_ord where tk_ord.tk_id = tk.id) or
                 exists (select 1 from tk_med where tk_med.tk_id = tk.id))
                             and tk.sign != "" 
                             order by tk.dt''',).fetchall()
        n_all = len(r_tk)
        
        if not n_all:
            log(u'無需上傳之掛號看診紀錄！')
            cls()
            return

        log(u'需上傳之掛號看診紀錄共 %s 件，開始製作上傳檔案 ...' % n_all)
        fi = cat(td, 'upload.xml')
         
        codecs.open(fi, 'w', 'big5').write('<?xml version="1.0" encoding="Big5"?><RECS>%s</RECS>' % '\n'.join([xml_upload(cr, i[0]) for i in r_tk]))

        n, n_trial = 0, 3
        while n < n_trial:
            buf = create_string_buffer(50)        
            r = cs.csUploadData(c_char_p(fi), 
                                c_char_p(str(os.stat(fi).st_size)), 
                                c_char_p(str(n_all)), 
                                buf, byref(c_int(100)))
            if r == 0: 
                dt = mid(buf, 37, 14)    
                log(u'上傳成功！IDC接收上傳資料時間： %s，上傳資訊存檔中 ...' % dt)
                try:
                    # note that dt is like 1000207172015 (dt_tw) 
                    cr.execute('insert into upload (dt) values (?)', 
                               (str(int(dt[:4]) - 1911).zfill(3) + dt[4:],))
                    
                    uid = cr.execute('select last_insert_rowid()').fetchone()[0]
                    
                    cr.executemany('''insert into tk_upload (tk_id, upload_id) 
                                      values (?, ?)''', 
                                   ((i[0], uid) for i in r_tk))
                    cn.commit()
                
                except:
                    cn.rollback()
                    # XXX Do something?
                    log(u'上傳至健保局成功，但寫入資料庫時失敗 ...')
                
                finally:
                    break

            else:
                if n == n_trial - 1:
                    break
                log(u'上傳失敗，重試中... ' + error_ic(cr, r))
                n += 1
                if r == 4050:
                    time.sleep(2)
                    r = cs.csVerifySAMDC()
                    log(u'安全模組認證中...')
                time.sleep(2)
        cls()

class patient_inst_selector(thread):
    
    def __init__(self, par=None):
        super(patient_inst_selector, self).__init__(par)
    
    def process(self):
        cn = sqlite3.connect(DB)
        cr = cn.cursor()        
        log = self.log

        def abort():
            log(u'終止患者案件整理！')
 
        m = QStandardItemModel(0, 0)
        r = cr.execute('''select distinct tk.inst_id, patient.name from tk 
                          join patient on tk.patient_id = patient.id 
                          where patient.pid = ? 
                          order by tk.dt desc''', (self.pid,)).fetchall()
        n_all = len(r)   
        tic = dt_now()
        if n_all:
            name = r[0][1]
            
            si = QStandardItem(u'%s  %s' % (self.pid, name))
            si.setData(QVariant('patient_%s' % self.pid))
            si.setCheckable(True)
            
            for ii, i in enumerate(r):
                log(u'整理患者 %s %s 案件中： %s/%s （%s%%）' % 
                    (self.pid, name, ii + 1, n_all, int((ii + 1) * 100. / n_all))) 
                
                if self.is_stopped():
                    abort()
                    return 

                qi = QStandardItem(u'案件號碼：%s' % i[0])
                qi.setData(QVariant('inst_%s' % i[0]))
                
                r1 = cr.execute('''select id, dt from tk 
                                   where inst_id = ? 
                                   order by dt''', (i[0],)).fetchall()
                for i1 in r1:
                
                    if self.is_stopped():
                        abort()
                        return 
                    
                    qi1 = QStandardItem(dt_s(i1[1]))
                    qi1.setData(QVariant('tk_%s' % i1[0]))
                    qi.appendRow(qi1)
                                        
                qi.setCheckable(True)
                si.appendRow(qi) 
        
            m.setItem(0, si)       
                
        toc = dt_now()
        log(u'案件整理結束！歷時： %s' % t_n((toc - tic)))
            
        self.emit(SIGNAL('done'), m)

class inst_selector(thread):
    
    views = (
        (u'案件分類-申報號碼', 
         '''select inst_app.inst_id, patient.name, inst_app.nr from inst_app 
            join tk on inst_app.inst_id = tk.inst_id
            join insttype on inst_app.insttype_id = insttype.id 
            join app on inst_app.app_id = app.id 
            join patient on tk.patient_id = patient.id 
            where insttype.code = ? and app.ym = ? 
            order by inst_app.nr'''), 
        
        (u'案件分類-案件號碼', 
         '''select distinct inst.id, patient.name from inst 
            join tk on inst.id = tk.inst_id 
            join patient on tk.patient_id = patient.id 
            join insttype on inst.insttype_id = insttype.id 
            where insttype.code = ? and substr(tk.dt, 1, 5) = ? 
            order by tk.dt'''),
    )
    def __init__(self, par=None):
        super(inst_selector, self).__init__(par)
    
    def process(self):
        cn = sqlite3.connect(DB)
        cr = cn.cursor()
        log = self.log
        
        def abort():
            log(u'終止案件整理！')

        tic = dt_now() 
        log(u'開始費用年月 %s 之案件整理！現在時刻： %s' % (self.ym, dt_s(now())))
        m = QStandardItemModel(len(INSTTYPE), 1)
        for k, ct in enumerate(INSTTYPE):          
            
            log(u'整理 %s 案件，請稍候 ...' % ct) 
            if self.is_stopped():
                abort()
                return      
        
            r = cr.execute(self.sql, (ct, self.ym)).fetchall()
            si = QStandardItem(ct)
            si.setData(QVariant('insttype_%s'% ct))
            n_all = len(r)
            if n_all:                    
                si.setCheckable(True)
                for ii, i in enumerate(r):

                    log(u'整理 %s 案件中： %s/%s （%s%%）' % 
                        (ct, ii + 1, n_all, int((ii + 1) * 100. / n_all))) 
                    if self.is_stopped():
                        abort()
                        return 
                    
                    try:
                        nr_s = str(i[2]).zfill(3) + ' ' * 3 
                    except:
                        nr_s = ''                        
                    
                    qi = QStandardItem(nr_s + i[1])
                    qi.setData(QVariant('inst_%s' % i[0]))
                    r1 = cr.execute('''select id, dt from tk 
                                       where inst_id = ? 
                                       order by dt''', (i[0],)).fetchall()
                    for i1 in r1:
                        qi1 = QStandardItem(dt_s(i1[1]))
                        qi1.setData(QVariant('tk_%s' % i1[0]))
                        qi.appendRow(qi1)
                                            
                    qi.setCheckable(True)
                    si.appendRow(qi) 
            
            m.setItem(k, si) 
                
        toc = dt_now()
        log(u'案件整理結束！歷時： %s' % t_n((toc - tic)))
        self.emit(SIGNAL('done'), m)

# recursively set the icons (to prevent 'not safe using QPixmap outside the GUI')
def set_icons(m):
    def _set(it):
        t = unicode(it.data().toString()).split('_')[0]
        if t == 'inst':
            it.setIcon(QIcon(':/res/img/patient.png'))
        elif t == 'patient':
            it.setIcon(QIcon(':/res/img/patient.png'))
        elif t == 'tk':
            it.setIcon(QIcon(':/res/img/calendar.png'))
        elif t == 'insttype':
            it.setIcon(QIcon(':/res/img/document-open.png'))

        if it.hasChildren():
            for ii in range(it.rowCount()):
                for jj in range(it.columnCount()):
                    itc = it.child(ii, jj)
                    _set(itc)

    for i in range(m.rowCount()):
        for j in range(m.columnCount()):
            it = m.item(i, j)
            _set(it)
    
    return m

class stats(thread):

    def __init__(self, par=None):
        super(stats, self).__init__(par)

    def process(self):
        cn = sqlite3.connect(DB)
        cr = cn.cursor()
        log = self.log

        try:
            d1 = str(int(self.ym[:3]) + 1911) + '.' + self.ym[3:5] 
        except:
            d1 = ''
        
        ym = self.ym
        yr = ym[:3]
        mon = ym[3:]
        tic = dt_now()
        log(u'開始 %s 年 %s 月費用圖形製作！開始時刻： %s' % (yr, mon, dt_s(now())))
        
        n_all = calendar.monthrange(int(yr) + 1911, int(mon))[1]
        
        ind = [[] for i in range(7)]
        for i in range(1, n_all + 1):
            w = str2date(str(int(yr) + 1911) + mon + str(i).zfill(2)).weekday()
            ind[w].append(i)
            if i == 1:
                ww = w

        r = cr.execute('''select tk.id, tk.dt 
                          from tk 
                          join inst on tk.inst_id = inst.id
                          join insttype on inst.insttype_id = insttype.id
                          where tk.dt like ?
                          and (trim(tk.serial) != "" or tk.sign != "")
               and exists (select 1 from tk_diag where tk_diag.tk_id = tk.id)
               and (exists (select 1 from tk_ord where tk_ord.tk_id = tk.id) or 
                    exists (select 1 from tk_med where tk_med.tk_id = tk.id))
                          order by tk.dt''', 
                          (self.ym + '%',)).fetchall()
        
        l = [[0] * len(i) for i in ind]
        cum = 0
        for ii, i in enumerate(r):
            tk_id, dt = i
            ix = int(dt[5:7])
            toc = dt_now()
            log(u'完成 %s %%，歷時 %s' % (int(ii * 100. / len(r)), t_n(toc - tic)))
            w = str2date(str(int(dt[:3]) + 1911) + dt[3:7]).weekday()
            a = attrs(cr, tk_id=tk_id)['amount_app']
            # XXX not intuitive ... 
            l[w][ind[w].index(ix)] += a
            cum += a
        
        r = cr.execute('''select insttype.code, count(distinct tk.inst_id) 
                              from tk 
                              join inst on tk.inst_id = inst.id
                              join insttype on inst.insttype_id = insttype.id
                              where tk.dt like ? 
                              and (trim(tk.serial) != "" or tk.sign != "")
                   and exists (select 1 from tk_diag where tk_diag.tk_id = tk.id)
                   and (exists (select 1 from tk_ord where tk_ord.tk_id = tk.id) or 
                        exists (select 1 from tk_med where tk_med.tk_id = tk.id))
                              group by insttype.code''', 
                              (self.ym + '%', )).fetchall()
        
        toc = dt_now()
        log(u'圖形製作完成！歷時： %s' % t_n(toc - tic))
            
        wd = ['{label: "%s"}' % i for i in ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')]
        self.emit(SIGNAL('done'), 
                (json.dumps({'title': u'%s 每日點數一覽圖（ 案件分佈：%s / 累積總點數：%s ）' % (d1, ' '.join([u'[%s] %s' % i for i in r]), cum), 
             'l': l[ww:] + l[0:ww],}), 
             ','.join(wd[ww:] + wd[0:ww]))) 

class printer(thread):

    def __init__(self, par=None):
        super(printer, self).__init__(par)

    def process(self):
        cn = sqlite3.connect(DB)
        cr = cn.cursor()
        log = self.log
        # XXX
        r = cr.execute('''select distinct tk.inst_id, 
            (exists (select 1 from tk_diag where tk_diag.tk_id = tk.id) and 
             (exists (select 1 from tk_ord where tk_ord.tk_id = tk.id) or 
              exists (select 1 from tk_med where tk_med.tk_id = tk.id)))  
                          from tk
                          where tk.inst_id in (%s) 
                          order by tk.inst_id
                       ''' % (','.join([c for c in self.l_print]),)).fetchall()
        n_all = len(r)
        tic = dt_now()
        
        for i, c in enumerate(r):
            log(u'列印中 ... %s/%s （%s%%）' % (i + 1, n_all, int((i + 1) * 100. / n_all)))
            
            if not c[1]:
                # XXX log(u'案件 %s 未看診完畢，無法列印！' % (i + 1))
                continue

            r = cr.execute('''select app.ym, inst_app.nr from inst_app 
                              join app on inst_app.app_id = app.id 
                              where inst_app.inst_id = ? 
                              order by app.ym desc''', (c[0],)).fetchone()
            d = attrs(cr, inst_id=c[0], ym=r[0], nr=r[1]) if r else attrs(cr, inst_id=c[0])
            for typ in ['dtl', 'rcpt', 'rcptn', 'prscr', 'chk']:
                if typ in self.l_print[unicode(c[0])]:
                    print_proxy((typ, d, True))
        
class fav_refresher(thread):
    
    def __init__(self, par=None):
        super(fav_refresher, self).__init__(par)
        self.dirty = False

    def process(self):
        cn = sqlite3.connect(DB)
        cn.create_function('valid_ord_code', 1, valid_ord_code)
        cr = cn.cursor()        
        log = self.log
        self.emit(SIGNAL('begin'))
        staff_id = self.staff_id 
        model = QStandardItemModel(0, 3)
        for l in sorted([(d[0], d[1], 'fav' + '_' + str(d[2])) for d in cr.execute('select code, name, id from fav where staff_id = ?', (staff_id,)).fetchall()], key=itemgetter(0, 1, 2)):
            model.appendRow([QStandardItem(ll) for ll in l])
        if self.dirty:
            d = update_dic_custom_code_name(cr, staff_id)
        else:
            self.dirty = True
            d = dic_custom_code_name

        self.emit(SIGNAL('done'), (model, d))

# ==============================================================================
#  redo-undo classes
# ==============================================================================

class cmd_tk(QUndoCommand):
    
    def __init__(self, w, tk_i, tk_f, msg):
        super(cmd_tk, self).__init__(msg)
        attrs_from_dict(locals())

    def redo(self):
        self.w.set_tk(self.tk_f) 

    def undo(self):
        self.w.set_tk(self.tk_i)

class cmd_fav(QUndoCommand):
    
    def __init__(self, w, favs_i, favs_f, msg):
        super(cmd_fav, self).__init__(msg)
        attrs_from_dict(locals())

    def redo(self):
        self.w.set_fav(self.favs_f) 

    def undo(self):
        self.w.set_fav(self.favs_i)

# ==============================================================================
#  display model classes
# ==============================================================================

class model(QAbstractTableModel):
    
    def __init__(self, ls=None, meta=None, dt=None):
        super(model, self).__init__()
        self.ls = [] if ls is None else ls
        self.meta = {} if meta is None else meta
        self.dt = '' if dt is None else dt 

    def flags(self, ix):
        if not ix.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemFlags(QAbstractTableModel.flags(self, ix) | Qt.ItemIsEditable)
    
    def columnCount(self, index=QModelIndex()):
        return len(self.meta['header']) 

    def rowCount(self, index=QModelIndex()):
        return len(self.ls)

    def insertRows(self, pos, rows=1, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), pos, pos + rows - 1)
        self.endInsertRows()
        return True

    def removeRows(self, pos, rows=1, index=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), pos, pos + rows - 1)
        del self.ls[pos: pos + rows]
        self.endRemoveRows()
        return True
    
    def headerData(self, sec, ori, role=Qt.DisplayRole):
        if role == Qt.TextAlignmentRole:
            if ori == Qt.Horizontal:
                return QVariant(int(Qt.AlignLeft | Qt.AlignVCenter))
            return QVariant(int(Qt.AlignRight | Qt.AlignVCenter))
        
        if role != Qt.DisplayRole:
            return QVariant()
       
        if ori == Qt.Horizontal:
            return QVariant(self.meta['header'][sec])
        
        elif ori == Qt.Vertical:
            return QVariant(sec + 1)

        return QVariant()
    
class model_diag(model):

    def __init__(self, ls, meta):
        super(model_diag, self).__init__(ls, meta)

    def data(self, ix, role=Qt.DisplayRole):
        if not ix.isValid() or not (0 <= ix.row() < len(self.ls)):
            return QVariant()
        
        row = ix.row()
        col = ix.column()
        l = self.ls[row]

        if role == Qt.DisplayRole:
            code, name, name_zh = dic_all_inv['diag'].get(l[1])

            if col == DIAG_CODE:
                return QVariant(code)

            elif col == DIAG_NAME:
                return QVariant(name_zh)

        elif role == Qt.BackgroundRole:
            return QVariant(QBrush(QColor('lavender' if row % 2 else 'lightsteelblue')))
        return QVariant()

class model_ord(model):

    def __init__(self, ls, meta, dt):
        super(model_ord, self).__init__(ls, meta, dt)

    def data(self, ix, role=Qt.DisplayRole):
        if not ix.isValid() or not (0 <= ix.row() < len(self.ls)):
            return QVariant()
        
        row = ix.row()
        col = ix.column()
        l = self.ls[row]
        dt = self.dt
        
        if role == Qt.DisplayRole:

            code, name = dic_all_inv['ord'].get(l[1])[:2]
            price = get_price('ord', code, dt)
            code, name = dic_custom_code_name.get(code, (code, name))

            ocode_name = dic_all_inv['ocode'].get(l[2])[1]

            if col == ORD_CODE:
                return QVariant(code)
            
            elif col == ORD_NAME:
                return QVariant(name)

            elif col == ORD_PRICE:
                return QVariant(price)

            elif col == ORD_PERCENT:
                return QVariant(l[3])
            
            elif col == ORD_QTY:
                return QVariant(l[4])            

            elif col == ORD_AMOUNT:
                return QVariant(rnd(l[3] * l[4] * price / 100.))

            elif col == ORD_OCODE:
                return QVariant(ocode_name)

        elif role == Qt.BackgroundRole:
            return QVariant(QBrush(QColor('lavender' if row % 2 else 'lightsteelblue')))
        return QVariant()

    def setData(self, ix, v, role=Qt.EditRole):
        if ix.isValid() and 0 <= ix.row() < len(self.ls):
            l = self.ls[ix.row()]
            col = ix.column()
            v, ok = v.toInt()
            if ok:
                # displayed and internal data storage 
                if col == ORD_OCODE:
                    i = 2
                elif col == ORD_PERCENT:
                    i = 3
                elif col == ORD_QTY:
                    i = 4
                if v != l[i]:                
                    l[i] = v 
                 
            self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), ix, ix)
            return True
        return False

class delg_ord(QStyledItemDelegate):

    def __init__(self, par=None):
        super(delg_ord, self).__init__(par)

    def createEditor(self, par, opt, ix):
        col = ix.column()
        
        if col == ORD_PERCENT:
            sp = QSpinBox(par)
            sp.setRange(1, 300)
            sp.setSingleStep(1)
            return sp

        elif col == ORD_QTY:
            sp = QSpinBox(par)
            sp.setRange(1, 100)
            sp.setSingleStep(1)
            sp.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
            return sp

        elif col == ORD_OCODE:
            cbo = QComboBox(par)
            dd = dic_all_inv['ocode']
            for k in sorted(dd.keys()):
                cbo.addItem(dd[k][1], QVariant(k))
            return cbo

    def setEditorData(self, ed, ix):
        txt = ix.model().data(ix, Qt.DisplayRole).toString()
        col = ix.column()
        
        if col in (ORD_PERCENT, ORD_QTY):
            ed.setValue(int(txt))
        
        elif col in (ORD_OCODE,):
            i = ed.findText(txt)
            if i == -1:
                i = 0
            ed.setCurrentIndex(i)

    def setModelData(self, ed, md, ix):
        col = ix.column()
        
        if col in (ORD_PERCENT, ORD_QTY):
            md.setData(ix, QVariant(ed.value()))

        elif col in (ORD_OCODE,):
            md.setData(ix, ed.itemData(ed.currentIndex()))

class model_med(model):

    def __init__(self, ls, meta, dt):
        super(model_med, self).__init__(ls, meta, dt)

    def data(self, ix, role=Qt.DisplayRole):
        if not ix.isValid() or not 0 <= ix.row() < len(self.ls):
            return QVariant()
        
        row = ix.row() 
        col = ix.column()
        l = self.ls[row]
        dt = self.dt

        if role == Qt.DisplayRole:
            code, name = dic_all_inv['med'].get(l[1])[:2]
            price = get_price('med', code, dt)
            code, name = dic_custom_code_name.get(code, (code, name))

            usage_code = dic_all_inv['usage'].get(l[2])[0]
            freq_code, _, freq_freq = dic_all_inv['freq'].get(l[3])
            ocode_name = dic_all_inv['ocode'].get(l[4])[1]

            if col == MED_CODE:
                return QVariant(code)
            
            elif col == MED_NAME:
                return QVariant(name)
            
            elif col == MED_USAGE:
                return QVariant(usage_code)
            
            elif col == MED_FREQ:
                return QVariant(freq_code)
            
            elif col == MED_DAYS:
                return QVariant(l[5])

            elif col == MED_DOSAGE:
                return QVariant(l[6])

            elif col == MED_QTY:
                return QVariant(round(freq_freq * l[5] * l[6], 2))

            elif col == MED_PRICE:
                return QVariant(price)

            elif col == MED_AMOUNT:
                return QVariant(rnd(round(freq_freq * l[5] * l[6], 2) * price))
            
            elif col == MED_OCODE:
                return QVariant(ocode_name)
            
        elif role == Qt.BackgroundRole:
            return QVariant(QBrush(QColor('lavender' if row % 2 else 'lightsteelblue')))
        return QVariant()

    def setData(self, ix, v, role=Qt.EditRole):
        if ix.isValid() and 0 <= ix.row() < len(self.ls):
            l = self.ls[ix.row()]
            col = ix.column()
            v, ok = v.toDouble() if col == MED_DOSAGE else v.toInt() 
            if ok:
                # displayed and internal data storage column 
                if col == MED_USAGE:
                    i = 2
                elif col == MED_FREQ:
                    i = 3
                elif col == MED_OCODE:
                    i = 4
                elif col == MED_DAYS:
                    i = 5
                elif col == MED_DOSAGE:
                    i = 6
                if v != l[i]:                
                    l[i] = v 

            self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), ix, ix)
            return True
        return False

class delg_med(QStyledItemDelegate):

    def __init__(self, par=None):
        super(delg_med, self).__init__(par)

    def createEditor(self, par, opt, ix):
        col = ix.column()
        if col == MED_USAGE:
            cbo = QComboBox(par)
            dd = dic_all_inv['usage']
            for k in sorted(dd.keys()):
                cbo.addItem(dd[k][0], QVariant(k))
            return cbo
        
        elif col == MED_FREQ:
            cbo = QComboBox(par)
            dd = dic_all_inv['freq']
            for k in sorted(dd.keys()):
                cbo.addItem(dd[k][0], QVariant(k))
            return cbo
        
        elif col == MED_OCODE:
            cbo = QComboBox(par)
            dd = dic_all_inv['ocode']
            for k in sorted(dd.keys()):
                cbo.addItem(dd[k][1], QVariant(k))
            return cbo

        elif col == MED_DAYS:
            sp = QSpinBox(par)
            sp.setRange(1, 180)
            sp.setSingleStep(1)
            sp.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
            return sp

        elif col == MED_DOSAGE:
            dsp = QDoubleSpinBox(par)
            dsp.setSingleStep(0.01)            
            return dsp

        #else:
        #    return QStyledItemDelegate.createEditor(self, par, opt, ix)

    def setEditorData(self, ed, ix):
        txt = ix.model().data(ix, Qt.DisplayRole).toString()
        col = ix.column()
        
        if col == MED_DAYS:
            ed.setValue(int(txt))
       
        elif col == MED_DOSAGE:
            ed.setValue(float(txt))

        elif col in (MED_USAGE, MED_FREQ, MED_OCODE):
            i = ed.findText(txt)
            if i == -1:
                i = 0
            ed.setCurrentIndex(i)
        
        #else:
        #    QStyledItemDelegate.setEditorData(self, ed, ix)

    def setModelData(self, ed, md, ix):
        col = ix.column()
        if col in (MED_DAYS, MED_DOSAGE):
            md.setData(ix, QVariant(ed.value()))
        
        elif col in (MED_FREQ, MED_USAGE, MED_OCODE):
            md.setData(ix, ed.itemData(ed.currentIndex()))
        
        #else:
        #    QStyledItemDelegate.setModelData(self, ed, md, ix)

class model_mat(model):

    def __init__(self, ls, meta, dt):
        super(model_mat, self).__init__(ls, meta, dt)

    def data(self, ix, role=Qt.DisplayRole):
        if not ix.isValid() or not (0 <= ix.row() < len(self.ls)):
            return QVariant()
        
        row = ix.row()
        col = ix.column()
        l = self.ls[row]
        dt = self.dt
        
        if role == Qt.DisplayRole:
            code, name = dic_all_inv['mat'].get(l[1])[:2]
            price = get_price('mat', code, dt)
            code, name = dic_custom_code_name.get(code, (code, name))

            ocode_name = dic_all_inv['ocode'].get(l[2])[1]

            if col == MAT_CODE:
                return QVariant(code)
            
            elif col == MAT_NAME:
                return QVariant(name)

            elif col == MAT_PRICE:
                return QVariant(price)

            elif col == MAT_PERCENT:
                return QVariant(l[3])
            
            elif col == MAT_QTY:
                return QVariant(l[4])            

            elif col == MAT_AMOUNT:
                return QVariant(rnd(l[3] * l[4] * price / 100.))

            elif col == MAT_OCODE:
                return QVariant(ocode_name)

        elif role == Qt.BackgroundRole:
            return QVariant(QBrush(QColor('lavender' if row % 2 else 'lightsteelblue')))
        return QVariant()

    def setData(self, ix, v, role=Qt.EditRole):
        if ix.isValid() and 0 <= ix.row() < len(self.ls):
            l = self.ls[ix.row()]
            col = ix.column()
            v, ok = v.toInt()
            if ok:
                # displayed and internal data storage 
                if col == MAT_OCODE:
                    i = 2
                elif col == MAT_PERCENT:
                    i = 3
                elif col == MAT_QTY:
                    i = 4
                if v != l[i]:                
                    l[i] = v 
                 
            self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), ix, ix)
            return True
        return False

class delg_mat(QStyledItemDelegate):

    def __init__(self, par=None):
        super(delg_mat, self).__init__(par)

    def createEditor(self, par, opt, ix):
        col = ix.column()
        
        if col == MAT_QTY:
            sp = QSpinBox(par)
            sp.setRange(1, 100)
            sp.setSingleStep(1)
            sp.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
            return sp

        elif col == MAT_PERCENT:
            sp = QSpinBox(par)
            sp.setRange(1, 300)
            sp.setSingleStep(1)
            return sp

        elif col == MAT_OCODE:
            cbo = QComboBox(par)
            dd = dic_all_inv['ocode']
            for k in sorted(dd.keys()):
                cbo.addItem(dd[k][1], QVariant(k))
            return cbo

    def setEditorData(self, ed, ix):
        txt = ix.model().data(ix, Qt.DisplayRole).toString()
        col = ix.column()
        
        if col in (MAT_PERCENT, MAT_QTY):
            ed.setValue(int(txt))
        
        elif col in (MAT_OCODE,):
            i = ed.findText(txt)
            if i == -1:
                i = 0
            ed.setCurrentIndex(i)

    def setModelData(self, ed, md, ix):
        col = ix.column()
        
        if col in (MAT_PERCENT, MAT_QTY):
            md.setData(ix, QVariant(ed.value()))

        elif col in (MAT_OCODE,):
            md.setData(ix, ed.itemData(ed.currentIndex()))

class model_ord_fav(model):

    def __init__(self, ls, meta, dt):
        super(model_ord_fav, self).__init__(ls, meta, dt)

    def data(self, ix, role=Qt.DisplayRole):
        if not ix.isValid() or not (0 <= ix.row() < len(self.ls)):
            return QVariant()
        
        row = ix.row()
        col = ix.column()
        l = self.ls[row]
        dt = self.dt
        
        if role == Qt.DisplayRole:
            code, name = dic_all_inv['ord'].get(l[1])[:2]
            price = get_price('ord', code, dt)
            ocode_name = dic_all_inv['ocode'].get(l[2])[1]

            if col == ORD_CODE_FAV:
                return QVariant(code)
            
            elif col == ORD_NAME_FAV:
                return QVariant(name)

            elif col == ORD_PERCENT_FAV:
                return QVariant(l[3])
            
            elif col == ORD_QTY_FAV:
                return QVariant(l[4])            

            elif col == ORD_OCODE_FAV:
                return QVariant(ocode_name)

        elif role == Qt.BackgroundRole:
            return QVariant(QBrush(QColor('lavender' if row % 2 else 'lightsteelblue')))
        return QVariant()

    def setData(self, ix, v, role=Qt.EditRole):
        if ix.isValid() and 0 <= ix.row() < len(self.ls):
            l = self.ls[ix.row()]
            col = ix.column()
            v, ok = v.toInt()
            if ok:
                # displayed and internal data storage 
                if col == ORD_OCODE_FAV:
                    i = 2
                elif col == ORD_PERCENT_FAV:
                    i = 3
                elif col == ORD_QTY_FAV:
                    i = 4
                if v != l[i]:                
                    l[i] = v 
                 
            self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), ix, ix)
            return True
        return False

class delg_ord_fav(QStyledItemDelegate):

    def __init__(self, par=None):
        super(delg_ord_fav, self).__init__(par)

    def createEditor(self, par, opt, ix):
        col = ix.column()
        
        if col == ORD_PERCENT_FAV:
            sp = QSpinBox(par)
            sp.setRange(1, 300)
            sp.setSingleStep(1)
            return sp

        elif col == ORD_QTY_FAV:
            sp = QSpinBox(par)
            sp.setRange(1, 100)
            sp.setSingleStep(1)
            sp.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
            return sp

        elif col == ORD_OCODE_FAV:
            cbo = QComboBox(par)
            dd = dic_all_inv['ocode']
            for k in sorted(dd.keys()):
                cbo.addItem(dd[k][1], QVariant(k))
            return cbo

    def setEditorData(self, ed, ix):
        txt = ix.model().data(ix, Qt.DisplayRole).toString()
        col = ix.column()
        
        if col in (ORD_PERCENT_FAV, ORD_QTY_FAV):
            ed.setValue(int(txt))
        
        elif col in (ORD_OCODE_FAV,):
            i = ed.findText(txt)
            if i == -1:
                i = 0
            ed.setCurrentIndex(i)

    def setModelData(self, ed, md, ix):
        col = ix.column()
        
        if col in (ORD_PERCENT_FAV, ORD_QTY_FAV):
            md.setData(ix, QVariant(ed.value()))

        elif col in (ORD_OCODE_FAV,):
            md.setData(ix, ed.itemData(ed.currentIndex()))

class model_med_fav(model):

    def __init__(self, ls, meta, dt):
        super(model_med_fav, self).__init__(ls, meta, dt)

    def data(self, ix, role=Qt.DisplayRole):
        if not ix.isValid() or not 0 <= ix.row() < len(self.ls):
            return QVariant()
        
        row = ix.row() 
        col = ix.column()
        l = self.ls[row]
        dt = self.dt

        if role == Qt.DisplayRole:
            code, name = dic_all_inv['med'].get(l[1])[:2]
            price = get_price('med', code, dt)
            usage_code = dic_all_inv['usage'].get(l[2])[0]
            freq_code, _, freq_freq = dic_all_inv['freq'].get(l[3])
            ocode_name = dic_all_inv['ocode'].get(l[4])[1]

            if col == MED_CODE_FAV:
                return QVariant(code)
            
            elif col == MED_NAME_FAV:
                return QVariant(name)
            
            elif col == MED_USAGE_FAV:
                return QVariant(usage_code)
            
            elif col == MED_FREQ_FAV:
                return QVariant(freq_code)
            
            elif col == MED_DAYS_FAV:
                return QVariant(l[5])

            elif col == MED_DOSAGE_FAV:
                return QVariant(l[6])

            elif col == MED_OCODE_FAV:
                return QVariant(ocode_name)
            
        elif role == Qt.BackgroundRole:
            return QVariant(QBrush(QColor('lavender' if row % 2 else 'lightsteelblue')))
        return QVariant()

    def setData(self, ix, v, role=Qt.EditRole):
        if ix.isValid() and 0 <= ix.row() < len(self.ls):
            l = self.ls[ix.row()]
            col = ix.column()
            v, ok = v.toDouble() if col == MED_DOSAGE_FAV else v.toInt() 
            if ok:
                # displayed and internal data storage column 
                if col == MED_USAGE_FAV:
                    i = 2
                elif col == MED_FREQ_FAV:
                    i = 3
                elif col == MED_OCODE_FAV:
                    i = 4
                elif col == MED_DAYS_FAV:
                    i = 5
                elif col == MED_DOSAGE_FAV:
                    i = 6
                if v != l[i]:                
                    l[i] = v 

            self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), ix, ix)
            return True
        return False

class delg_med_fav(QStyledItemDelegate):

    def __init__(self, par=None):
        super(delg_med_fav, self).__init__(par)

    def createEditor(self, par, opt, ix):
        col = ix.column()
        if col == MED_USAGE_FAV:
            cbo = QComboBox(par)
            dd = dic_all_inv['usage']
            for k in sorted(dd.keys()):
                cbo.addItem(dd[k][0], QVariant(k))
            return cbo
        
        elif col == MED_FREQ_FAV:
            cbo = QComboBox(par)
            dd = dic_all_inv['freq']
            for k in sorted(dd.keys()):
                cbo.addItem(dd[k][0], QVariant(k))
            return cbo
        
        elif col == MED_OCODE_FAV:
            cbo = QComboBox(par)
            dd = dic_all_inv['ocode']
            for k in sorted(dd.keys()):
                cbo.addItem(dd[k][1], QVariant(k))
            return cbo

        elif col == MED_DAYS_FAV:
            sp = QSpinBox(par)
            sp.setRange(1, 180)
            sp.setSingleStep(1)
            sp.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
            return sp

        elif col == MED_DOSAGE_FAV:
            dsp = QDoubleSpinBox(par)
            dsp.setSingleStep(0.01)            
            return dsp

        #else:
        #    return QStyledItemDelegate.createEditor(self, par, opt, ix)

    def setEditorData(self, ed, ix):
        txt = ix.model().data(ix, Qt.DisplayRole).toString()
        col = ix.column()
        
        if col == MED_DAYS_FAV:
            ed.setValue(int(txt))
       
        elif col == MED_DOSAGE_FAV:
            ed.setValue(float(txt))

        elif col in (MED_USAGE_FAV, MED_FREQ_FAV, MED_OCODE_FAV):
            i = ed.findText(txt)
            if i == -1:
                i = 0
            ed.setCurrentIndex(i)
        
        #else:
        #    QStyledItemDelegate.setEditorData(self, ed, ix)

    def setModelData(self, ed, md, ix):
        col = ix.column()
        if col in (MED_DAYS_FAV, MED_DOSAGE_FAV):
            md.setData(ix, QVariant(ed.value()))
        
        elif col in (MED_FREQ_FAV, MED_USAGE_FAV, MED_OCODE_FAV):
            md.setData(ix, ed.itemData(ed.currentIndex()))
        
        #else:
        #    QStyledItemDelegate.setModelData(self, ed, md, ix)

class model_mat_fav(model):

    def __init__(self, ls, meta, dt):
        super(model_mat_fav, self).__init__(ls, meta, dt)

    def data(self, ix, role=Qt.DisplayRole):
        if not ix.isValid() or not (0 <= ix.row() < len(self.ls)):
            return QVariant()
        
        row = ix.row()
        col = ix.column()
        l = self.ls[row]
        dt = self.dt
        
        if role == Qt.DisplayRole:
            code, name = dic_all_inv['mat'].get(l[1])[:2]
            price = get_price('mat', code, dt)
            ocode_name = dic_all_inv['ocode'].get(l[2])[1]

            if col == MAT_CODE_FAV:
                return QVariant(code)
            
            elif col == MAT_NAME_FAV:
                return QVariant(name)

            elif col == MAT_PERCENT_FAV:
                return QVariant(l[3])
            
            elif col == MAT_QTY_FAV:
                return QVariant(l[4])            

            elif col == MAT_OCODE_FAV:
                return QVariant(ocode_name)

        elif role == Qt.BackgroundRole:
            return QVariant(QBrush(QColor('lavender' if row % 2 else 'lightsteelblue')))
        return QVariant()

    def setData(self, ix, v, role=Qt.EditRole):
        if ix.isValid() and 0 <= ix.row() < len(self.ls):
            l = self.ls[ix.row()]
            col = ix.column()
            v, ok = v.toInt()
            if ok:
                # displayed and internal data storage 
                if col == MAT_OCODE_FAV:
                    i = 2
                elif col == MAT_PERCENT_FAV:
                    i = 3
                elif col == MAT_QTY_FAV:
                    i = 4
                if v != l[i]:                
                    l[i] = v 
                 
            self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), ix, ix)
            return True
        return False

class delg_mat_fav(QStyledItemDelegate):

    def __init__(self, par=None):
        super(delg_mat_fav, self).__init__(par)

    def createEditor(self, par, opt, ix):
        col = ix.column()
        
        if col == MAT_QTY_FAV:
            sp = QSpinBox(par)
            sp.setRange(1, 100)
            sp.setSingleStep(1)
            sp.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
            return sp

        elif col == MAT_PERCENT_FAV:
            sp = QSpinBox(par)
            sp.setRange(1, 300)
            sp.setSingleStep(1)
            return sp

        elif col == MAT_OCODE_FAV:
            cbo = QComboBox(par)
            dd = dic_all_inv['ocode']
            for k in sorted(dd.keys()):
                cbo.addItem(dd[k][1], QVariant(k))
            return cbo

    def setEditorData(self, ed, ix):
        txt = ix.model().data(ix, Qt.DisplayRole).toString()
        col = ix.column()
        
        if col in (MAT_PERCENT_FAV, MAT_QTY_FAV):
            ed.setValue(int(txt))
        
        elif col in (MAT_OCODE_FAV,):
            i = ed.findText(txt)
            if i == -1:
                i = 0
            ed.setCurrentIndex(i)

    def setModelData(self, ed, md, ix):
        col = ix.column()
        
        if col in (MAT_PERCENT_FAV, MAT_QTY_FAV):
            md.setData(ix, QVariant(ed.value()))

        elif col in (MAT_OCODE_FAV,):
            md.setData(ix, ed.itemData(ed.currentIndex()))

class model_fav(model):

    def __init__(self, ls, meta):
        super(model_fav, self).__init__(ls, meta)

    def data(self, ix, role=Qt.DisplayRole):
        if not ix.isValid() or not (0 <= ix.row() < len(self.ls)):
            return QVariant()
        
        row = ix.row()
        col = ix.column()
        l = self.ls[row]
        
        if role == Qt.DisplayRole:
            if col == FAV_ID:
                return QVariant(l['fav_id'])

            elif col == FAV_CODE:
                return QVariant(l['code'])
            
            elif col == FAV_NAME:
                return QVariant(l['name'])

        elif role == Qt.BackgroundRole:
            return QVariant(QBrush(QColor('bisque' if row % 2 else 'beige')))
        
        return QVariant()

    def setData(self, ix, v, role=Qt.EditRole):
        if ix.isValid() and 0 <= ix.row() < len(self.ls):
            l = self.ls[ix.row()]
            col = ix.column()
            v = v.toString()
            # displayed and internal data storage mapping 
            if col == FAV_CODE :
                i = 'code' 
            elif col == FAV_NAME:
                i = 'name' 
            if v != l[i]:                
                l[i] = unicode(v) 
                 
            self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), ix, ix)
            return True
        return False

class delg_fav(QStyledItemDelegate):

    def __init__(self, par=None):
        super(delg_fav, self).__init__(par)

    def createEditor(self, par, opt, ix):
        col = ix.column()
        led = QLineEdit(par)
        return led 

    def setEditorData(self, ed, ix):
        ed.setText(ix.model().data(ix, Qt.DisplayRole).toString())

    def setModelData(self, ed, md, ix):
        row = ix.row()
        col = ix.column()
        txt = unicode(ed.text()).strip()
        if not txt:
            return
        
        l = md.ls[row]
        if col == FAV_CODE:
            code = txt 
            name = l['name']
        elif col == FAV_NAME:
            code = l['code']
            name = txt
        r = cr.execute('select * from fav where code = ? and name = ?', 
                       (code, name)).fetchone()
        if r:
            QMessageBox.warning(self.parent(), u'輸入代碼錯誤', u'此組「輸入代碼」/「識別名稱」重複存在。\n請重新修改後再嘗試存檔！')
        else:
            md.setData(ix, QVariant(ed.text()))

class model_dsp(model):

    def __init__(self, ls, meta):
        super(model_dsp, self).__init__(ls, meta)

    def data(self, ix, role=Qt.DisplayRole):
        if not ix.isValid() or not (0 <= ix.row() < len(self.ls)):
            return QVariant()
        
        row = ix.row()
        if role == Qt.DisplayRole:
            try:
                return QVariant(self.ls[row][ix.column()])
            except:
                return QVariant()

        elif role == Qt.BackgroundRole:
            return QVariant(QBrush(QColor('bisque' if row % 2 else 'sandybrown')))

        return QVariant()

class model_tk(model_dsp):

    def __init__(self, ls, meta):
        super(model_tk, self).__init__(ls, meta)

    def data(self, ix, role=Qt.DisplayRole):
        if not ix.isValid() or not (0 <= ix.row() < len(self.ls)):
            return QVariant()
        
        row = ix.row()
        col = ix.column()
        
        l = self.ls[row]
        if role == Qt.ForegroundRole:
            b1, b2 = l[-2:]
            if b1 == 0 or b2 == 0:
                c = 'white' 
            else:
                c = 'black' 
            return QVariant(QBrush(QColor(c)))

        elif role == Qt.BackgroundRole:
            b1, b2 = l[-2:]
            if b1 == 0:
                c = '#ffb6c1'
            elif b2 == 0:
                c = 'green'
            else:
                c = 'lavender' if row % 2 else 'lightsteelblue'
            return QVariant(QBrush(QColor(c)))

        elif role == Qt.DisplayRole:
            l_ = l[col]
            if col == 3:
                return QVariant(dt_s(l_, True))
            elif col == 4:
                return QVariant(dt_s(l_))
            elif col == 5:
                return QVariant(serial_s(l_, l[6], l[7], l[8], l[9]))
            elif col == 6:
                return QVariant(l[10])
            else:
                return QVariant(l_)

        return QVariant()
   
# ==============================================================================
#  all windows 
# ==============================================================================

class overlay(QWidget):

    def __init__(self, par=None):
    
        QWidget.__init__(self, par)
        palette = QPalette(self.palette())
        palette.setColor(palette.Background, Qt.transparent)
        self.setPalette(palette)
    
    def paintEvent(self, e):
        p = QPainter()
        p.begin(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.fillRect(e.rect(), QBrush(QColor(0, 0, 0, 30)))
        p.setPen(QPen(Qt.NoPen))
        
        n = 8 
        for i in range(n):
            if (self.cnt / (n - 1)) % n == i:
                p.setBrush(QBrush(QColor(127 + (self.cnt % (n - 1)) * 128 / (n - 1),
                                         127, 127)))
            else:
                p.setBrush(QBrush(QColor(127, 127, 127)))

            p.drawEllipse(
                self.width() / 2 + 30 * math.cos(2 * math.pi * i / (n * 1.)) - 10,
                self.height() / 2 + 30 * math.sin(2 * math.pi * i / (n * 1.)) - 10,
                14, 14)
        p.end()
    
    def showEvent(self, e):
        self.resize(self.parent().size())
        self.timer = self.startTimer(60)
        self.cnt = 0

    def timerEvent(self, e):
        self.update()        
        self.cnt += 1

    def hideEvent(self, e):
        try:
            self.killTimer(self.timer)
        except:
            pass

class wdg_fav(QWidget, Ui_wdg_fav):

    def __init__(self, par=None):
        QWidget.__init__(self, par)
        self.setupUi(self)
        
class wdg_probe(QWidget, Ui_wdg_probe):

    def __init__(self, par=None):
        QWidget.__init__(self, par)
        self.setupUi(self)

class win(QMainWindow):

    def __init__(self, *a):
        super(win, self).__init__(*a)
        
    def class_name(self):
        return self.__class__.__name__
    
    def send(self, **d):
        self.emit(SIGNAL('msg_%s' % self.class_name()), d)

class win_ic(win, Ui_win_ic):
    
    def __init__(self, par=None):
        win.__init__(self, par)
        self.setupUi(self)
        
        for i in ['get_basic', 'get_diag', 'get_ord', 'get_allergy',
                  'get_cum', 'get_tel', 'get_donate', 
                  'update_hc', 'set_allergy', 'set_tel', 'set_pwd','stop_pwd', 
                  'set_hpc', 'verify_hpc', 'unlock_hpc',  
                  'new_tab']:
            self.connect(getattr(self, 'act_%s' % i), SIGNAL('triggered()'), 
                         partial(self.handler, i))
        
        self.restoreGeometry(sts.value('%s/geometry' % self.class_name()).toByteArray())
    
        self.tw = t = QTabWidget()
        #t.setTabPosition(QTabWidget.East)
        t.setTabsClosable(True)
        t.setDocumentMode(False)
        self.setCentralWidget(t)
        self.new_tab()
        
        self.dll = dll(self)
        self.connect(self.dll, SIGNAL('msg_dll'), self.handler_dll)

    def new_tab(self):
        t = self.tw
        t.addTab(wdg_ic(), '')
        t.setCurrentIndex(t.count() - 1)

    def handler(self, c):
        if c == 'get_basic':
            self.dll.go(f='get_basic', var={'aim': 'show'})
        
        elif c == 'get_diag':
            self.dll.go(f='get_diag')
        
        elif c == 'get_ord':
            self.dll.go(f='get_ord')

            #meta={'caption': u'就醫類別', 
            #      'header': (u'新生兒就醫註記', u'就診日期時間', u'補卡註記', 
            #                 u'就醫序號', u'醫療院所代碼', u'門診費用', 
            #                 u'門診部分負擔', u'住院費用', u'短期住院部分負擔', 
            #                 u'長期住院部分負擔')
            #}
            #
            #meta={'caption': u'預防接種', 
            #      'header': (u'疫苗種類', u'接種日期', 
            #                 u'醫療院所代碼', u'疫苗批號')
            #}

        elif c == 'get_tel':
            self.dll.go(f='get_tel')
        
        elif c == 'get_cum':
            self.dll.go(f='get_cum')
        
        elif c == 'get_donate':
            self.dll.go(f='get_donate')
        
        elif c == 'set_tel':
            self.dll.go(f='get_basic', var={'aim': 'set_tel'})

        elif c == 'set_allergy':
            self.dll.go(f='get_basic', var={'aim': 'set_allergy'})

        elif c == 'update_hc':
            self.dll.go(f='update_hc')

        elif c == 'set_pwd':
            r = cs.csISSetPIN()
            if r == 0:  # 未設密碼狀況
                r = cs.csInputHCPIN()
                if r == 0: 
                    info(self, u'', u'IC卡密碼功能啟動成功！')
                else:    
                    show_error(self, r)
            
            elif r == 1: # 已設密碼狀況
                info(self, u'', 
                u'更改密碼：請從讀卡機鍵盤輸入原始密碼，並按讀卡機鍵盤[Enter]鍵！')

                r = cs.csVerifyHCPIN()
                if r == 0:
                    info(self, u'', u'IC卡原始密碼輸入正確！請輸入新密碼兩次！')
                    r = cs.csInputHCPIN()
                    if r == 0:
                        info(self, u'', u'IC卡密碼更改成功！')
                    else:
                        show_error(self, r)
                else:
                    show_error(self, r)
            
            else: 
                show_error(self, r)
     
        elif c == 'stop_pwd':
            self.dll.go(f='stop_pwd')
       
        elif c == 'set_hpc':
            self.dll.go(f='set_hpc')

        elif c == 'verify_hpc':
            self.dll.go(f='verify_hpc')

        elif c == 'unlock_hpc':
            self.dll.go(f='unlock_hpc')
 
    def handler_dll(self, d):
        result = d['result']
        if result is None:
            return
        
        f = d.get('f', '')
        if not f:
            return

        if f == 'get_basic':
            r, dd, t = result 
            var = d['var']
            aim = var.get('aim', '')
            if aim == 'set_allergy':
                if r == 0:
                    meds, ok = QInputDialog.getText(None, u'過敏藥物輸入', u'請輸入過敏藥物，以三組為限。\n各組藥物間用分號『;』區隔，名稱長度各不大於40 字元！\n\n『合法範例』：\n    amoxillin;dedema;lopan')
                    if ok and not meds.isEmpty():
                        meds = ''.join([s.ljust(40) for i, s in enumerate(unicode(meds).split(';')) if i < 3])
                        if meds.strip():
                            self.dll.go(f='set_allergy',
                                    kw={'pid': dd['pid'],
                                        'birthday': dd['birthday'],
                                        'meds': meds,
                                        'doctor_pid': DOCTOR_PID})
                else:
                    show_error(self, r)
            
            elif aim == 'set_tel':
                if r == 0:
                    tel, ok = QInputDialog.getText(self, u'緊急聯絡電話輸入', 
                                    u'請輸入緊急聯絡電話（最大長度：十五個字元）')
                    
                    if ok and not tel.isEmpty():
                        self.dll.go(f='set_tel', 
                                    kw={'pid': d['pid'], 
                                        'birthday': dd['birthday'], 
                                        'tel': unicode(tel)})
                else:
                    show_error(self, r)
 
            elif aim == 'show':
                if r == 0:
                    model_dsp(ls=t,
                            meta={'caption': u'基本資料', 
                                  'header': (u'卡片號碼', 
                                             u'姓名', 
                                             u'身份證號碼', 
                                             u'出生日期', 
                                             u'性別', 
                                             u'發卡日期', 
                                             u'卡片註銷註記', 
                                             u'保險人代碼', 
                                             u'身份註記', 
                                             u'有效期限', 
                                             u'可用次數', 
                                             u'新生兒出生日期', 
                                             u'新生兒胎胞註記')})
                    tw = self.tw
                    ix = tw.currentIndex()
                    tw.setTabIcon(ix, QIcon(':/res/img/patient.png'))
                    tw.setTabText(ix, u'%s %s' % (dd['pid'], dd['name'].strip()))

                else:
                    show_error(self, r)
        
        elif f == 'get_diag': 
            r, t1, t2 = result
            if r == 0: 
                w = self.tw.currentWidget()
                model_dsp(ls=t1,
                        meta={'caption': u'重大傷病註記', 
                              'header': (u'重大傷病名稱', 
                                         u'註記開始日期', 
                                         u'註記結束日期')})
                model_dsp(ls=t2,
                        meta={'caption': u'最近六次就醫資料',
                              'header': (u'就診日期', 
                                         u'主要診斷碼', 
                                         u'次要診斷碼一', 
                                         u'次要診斷碼二', 
                                         u'次要診斷碼三', 
                                         u'次要診斷碼四', 
                                         u'次要診斷碼五')})           

            else:
                show_error(self, r)

        elif f == 'get_ord':
            r, t1, t2, t3, t4 = result
            print(r, t1, t2, t3, t4)
            if r == 0:
                w = self.tw.currentWidget()
                model_dsp(ls=t1, 
                        meta={'caption': u'門診處方籤', 
                              'header': (u'使用日期', 
                                         u'醫令類別', 
                                         u'醫令代碼', 
                                         u'使用部位', 
                                         u'用法', 
                                         u'使用天數', 
                                         u'調劑方式')})
                model_dsp(ls=t2, 
                        meta={'caption': u'醫令', 
                              'header': (u'使用日期', 
                                         u'醫令代碼', 
                                         u'用法', 
                                         u'使用天數', 
                                         u'總量')})
                model_dsp(ls=t3, 
                        meta={'caption': u'重要醫令',
                              'header': (u'實施日期', 
                                         u'實施院所代碼', 
                                         u'醫令代碼', 
                                         u'使用部位', 
                                         u'總量')})
                model_dsp(ls=t4, 
                        meta={'caption': u'過敏藥物', 
                              'header': (u'過敏藥物成分',)})
                
            else:
                show_error(self, r)
        
        elif f == 'get_cum':
            r, t = result 
            if r == 0 and t: 
                w = self.tw.currentWidget()
                model_dsp(ls=t,
                        meta={'caption': u'就醫累計', 
                              'header': (u'年度', 
                                         u'總就醫累計次數', 
                                         u'門診費用總計', 
                                         u'住診費用總計', 
                                         u'門診部分負擔總計', 
                                         u'短期住診部分負擔', 
                                         u'長期住診部分負擔',
                                         u'所有部分負擔總計', 
                                         u'門診短期住診部分負擔')})
            else:
                show_error(self, r)

        elif f == 'get_tel':
            r, t = result 
            if r == 0:
                w = self.tw.currentWidget()
                model_dsp(ls=t,
                        meta={'caption': u'緊急聯絡電話', 
                              'header': (u'緊急聯絡電話',)})
            else:
                show_error(self, r)
        
        elif f == 'get_donate':
            r, t = result
            if r == 0:
                w = self.tw.currentWidget()
                model_dsp(ls=t,
                        meta={'caption': u'器官捐贈註記',
                              'header': (u'器官捐贈註記',)})           
            else:
                show_error(self, r)

        elif f == 'update_hc':
            r = result
            if r == 0:
                info(self, u'', u'IC卡狀態更新成功！')
            else:
                show_error(self, r)
        
        elif f == 'stop_pwd':
            r = result
            if r == 0:
                info(self, u'', u'IC卡密碼功能已停止！')
            else:
                show_error(self, r)
        
        elif f == 'unlock_hpc':
            r = result
            if r == 0:
                info(self, u'', u'醫事人員卡解除鎖定成功！')
            else:
                show_error(self, r)
    
        elif f == 'verify_hpc':
            r = result
            if r == 0: 
                info(self, u'', u'醫事人員卡密碼認證成功！')
            else:    
                show_error(self, r)
        
        elif f == 'set_hpc':
            r = result
            if r == 0: 
                info(self, u'', u'醫事人員卡密碼更改成功！')
            else:
                show_error(self, r)

        elif f == 'set_tel':
            r = result
            if r == 0:
                info(self, u'', u'緊急聯絡電話寫入成功！')
            else:
                show_error(self, r) 
        
        elif f == 'set_allergy':
            r = result
            if r == 0:
                info(self, u'', u'過敏藥物寫入成功！')
            else:
                show_error(self, r)
    
    def closeEvent(self, e):
        sts.setValue('%s/geometry' % self.class_name(), 
                     QVariant(self.saveGeometry()))

class win_main(win, Ui_win_main):
        
    def __init__(self):
        win.__init__(self)
        self.setupUi(self)

        for i in ['mnb', 'tb']:
            getattr(self, i).setContextMenuPolicy(Qt.PreventContextMenu)
        
        for i in ['tk', 'quit', 'inst', 'stat', 'renew', 
                  'app', 'backup', 'about', 'patient']:
            self.connect(getattr(self, 'act_%s' % i), SIGNAL('triggered()'), 
                    getattr(self, i))
        
        self.lbl_ded = QLabel(self)
        self.lbl_ded.setText(u'掛號日期') 

        self.ded = QDateEdit()
        self.ded.setDisplayFormat('M/d/yyyy')
        self.ded.setCalendarPopup(True)
        self.ded.setDate(QDate.currentDate())
        
        for k, i in enumerate(['lbl_ded', 'ded', '']):
            setattr(self, 'lbl_%s' % k, QLabel(self))
            lbl = getattr(self, 'lbl_%s' % k)
            lbl.setText(u'  ')

            self.tb.addWidget(lbl)
            if i:
                self.tb.addWidget(getattr(self, i))
            else:
                self.tb.addSeparator()
        
        self.tbv = tbv = QTableView(self)
        tbv.setEditTriggers(QAbstractItemView.NoEditTriggers)
        tbv.setSelectionBehavior(QAbstractItemView.SelectRows)
        tbv.setSelectionMode(QAbstractItemView.SingleSelection)
        tbv.setTabKeyNavigation(False)
        self.setCentralWidget(tbv)

        self.dll = dll(self)
        self.connect(self.dll, SIGNAL('msg_dll'), self.handler_dll)
        
        self.restoreState(sts.value('%s/state' % self.class_name()).toByteArray())
        
        # create labels in stb
        for ii, it in enumerate([('stb_gen',  2), 
                                 ('stb_ex', 4)]): 
            n, l = it
            setattr(self, n, QLabel(self))
            lbl = getattr(self, n)
            lbl.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
            self.stb.insertPermanentWidget(ii, lbl, l)
        self.stb.setSizeGripEnabled(False)

        self.refresher = r = refresher(self)
        self.connect(r, SIGNAL('done'), self.update_tbv)
        self.connect(r, SIGNAL('status'), self.status)
        self.connect(r, SIGNAL('stopped'), 
                     partial(self.status, u'終止掛號紀錄整理！'))
        
        self.uploader = u = uploader(self)
        self.connect(u, SIGNAL('status'), self.status)
        self.connect(u, SIGNAL('stopped'), 
                     partial(self.status, u'終止上傳作業！'))
            
        QTimer.singleShot(0, self.init)
        
        # XXX upload after 1 mins
        QTimer.singleShot(1 * 60000, self.upload)
        self.n_trial = 0

        # XXX update fav and reminder
        #dt = self.date()
        #r = cr.execute('''select med.code, name, valid_from, valid_till from med join fav on med.code = fav.code where ? between valid_from and valid_till and price < 0.001 order by valid_from desc''', (dt,)).fetchall()

    def init(self):
        self.item_probe = [
            ('probe', u'看診',     '', False),
            None,
            ('fee',   u'更改收費', '', False),
            None,
            ('query', u'患者查詢', '', False),
            None,
            ('prscr', u'處方籤',   '', False),
            ('chk',   u'檢驗單',   '', False),            
            ('rcptn', u'費用收據', '', False),
            ('rcpt',  u'明細收據', '', False),
            ('dtl',   u'總表',     '', False),
        ]
         
        for j in ['probe',]:
            setattr(self, 'mnu_%s' % j, QMenu(self))
            mnu = getattr(self, 'mnu_%s' % j)
            for i in getattr(self, 'item_%s' % j):                
                if i is None:
                    mnu.addSeparator()
                else:
                    n, t, sc, ck = i
                    setattr(self, 'act_%s' % n, QAction(t, self))
                    a = getattr(self, 'act_%s' % n)
                    a.setCheckable(ck)
                    if n in ['prscr', 'rcpt', 'rcptn', 'dtl', 'chk']:
                        self.connect(a, SIGNAL('triggered()'), 
                                     partial(self.printf, n))
                    else:
                        self.connect(a, SIGNAL('triggered()'), 
                                     getattr(self, n))
                    mnu.addAction(a)
        
        self.connect(self.ded, SIGNAL('dateChanged(QDate)'), self.refresh)
        tbv = self.tbv
        self.connect(tbv.verticalHeader(), SIGNAL('sectionClicked(int)'), 
                     self.ent_tk)
        tbv.setFocus()
        
        self.refresh()
        self.b_ask = True 
        self.overlay = overlay(self)
    
    def status(self, msg, sect='stb_gen', to=5000):
        stb = getattr(self, sect)
        stb.setText(msg)
        
        def cls():
            stb.setText('')
        if to:
            QTimer.singleShot(to, cls)
    
    def upload(self):
        if not is_dll_ok or not is_com_ok:
            return
        self.uploader.go()
    
    def date(self):
        return dt_tw(self.ded.date().toPyDate(), date_only=True)

    def refresh(self):
        self.refresher.go(dt=self.date())
    
    def printf(self, typ):
        printf(typ, self.tk_id, self)
    
    def query(self):
        w = win_patient(par=self, pid=self.pid)
        w.setWindowModality(Qt.ApplicationModal)
        w.show()

    def fee(self):
        dlg = dlg_fee(par=self, tk_id=self.tk_id)        
        if dlg.exec_():
            l = []
            if not dlg.rbn_na.isChecked():                
                if dlg.rbn_gen.isChecked():
                    fee_id = 2

                elif dlg.rbn_ini.isChecked():
                    fee_id = 3

                l = [(self.tk_id, fee_id, 1)]
            
            if dlg.chk_loan.isChecked():
                l.append((tk_id, 4, 1))     
            
            try:
                cr.execute('delete from tk_fee where tk_id = ?', (self.tk_id,))
                if l:
                    cr.executemany('''insert into tk_fee (tk_id, fee_id, qty) 
                                      values (?, ?, ?)''', l) 
                cn.commit()
            except:
                cn.rollback()

    def ent_tk(self, i):
        l = self.tbv.model().ls[i]
        self.tk_id = l[0]
        self.pid = l[2]
        self.mnu_probe.exec_(QCursor.pos())

    def update_tbv(self, ls):
        tbv = self.tbv
        tbv.setModel(
            model_tk(ls=ls,
                    meta={'header': (u'', u'患者姓名', u'身份證號', u'出生日期',
                                     u'掛號時間', u'就醫序號', u'案件號碼')}))      
        tbv.setColumnHidden(0, True)
        for i in range(tbv.model().columnCount()):
            n, ok = sts.value('%s/tbv/%s/width' % (self.class_name(), i)).toInt()
            if ok:
                tbv.setColumnWidth(i, n)
        tbv.show()

    def tk(self):
        dlg = dlg_tk_ini(self)
        if dlg.exec_():
            # XXX 
            if self.ded.date() != QDate.currentDate():
                self.ded.setDate(QDate.currentDate())
            
            tktype_code = 'AA' if dlg.chk_same.isChecked() else '01'
            amend_code = '1'
            
            if dlg.rbn_gen.isChecked():
                slc = 0

            elif dlg.rbn_amend.isChecked():
                slc = 1

            elif dlg.rbn_debt.isChecked():
                slc = 2
            
            elif dlg.rbn_voc.isChecked():
                slc = 3
           
            elif dlg.rbn_amend_f.isChecked():
                slc = 4

            if slc == 3:
                self.tk_nic(tktype_code='AA' if dlg.chk_same.isChecked() else 'AD', serial='IC06', insttype_code='B6')

            elif slc == 2:
                self.tk_nic(tktype_code=tktype_code, serial='')

            else:
                amend_code = '2' if slc == 1 else '1'
                self.overlay.show()
                self.dll.go(f='get_basic',
                            var={'slc': slc, 
                                 'amend_code': amend_code, 
                                 'tktype_code': tktype_code,
                                 'aim': 'fast_amend' if slc == 4 else ''})
                                
    def tk_nic(self, tktype_code='01', serial='B000', insttype_code='09', inst_id=0):
        dlg = dlg_tk_abn(self)
        
        b_abn = False 
        if serial == 'IC06' and insttype_code == 'B6':
            title = u'職災'
        
        elif serial == '' and tktype_code == 'AA':
            title = u'欠卡同療'
        
        elif serial == '':
            title = u'欠卡'
            dt = dt_before(dlg.dted_tk.dateTime().toPyDateTime())
            dlg.dted_tk.setDateTime(QDateTime.fromString(dt.strftime('%Y%m%d%H%M%S'), 'yyyyMMddhhmmss'))
        
        else:
            title = u'異常'
            b_abn = True

        dlg.cbo_abn.setEnabled(b_abn)
        dlg.setWindowTitle(u'%s掛號：請輸入患者資料' % title)

        if dlg.exec_():
            name = unicode(dlg.led_name.text())
            pid = unicode(dlg.led_pid.text())

            birthday = dt_tw(dlg.ded_birth.date().toPyDate(), date_only=True)
            id0, ok = dlg.cbo_state.itemData(dlg.cbo_state.currentIndex()).toInt()
            if not ok:
                show_error(self, title=u'手動掛號失敗', msg=u'請回報此問題！')
                return 
            state_code = dic_all_inv['state'].get(id0)[0]
            if b_abn:
                id0, ok = dlg.cbo_abn.itemData(dlg.cbo_abn.currentIndex()).toInt()
                if not ok: 
                    show_error(self, title=u'異常掛號失敗', msg=u'請回報此問題！')
                    return 
                serial = dic_all_inv['anormaly'].get(id0)[0]

            if tktype_code == 'AA': 
                serial = ''
                dlg1 = dlg_ent_inst(par=self, 
                                    pid=pid, 
                                    name=name, 
                                    birthday=birthday, 
                                    insttype_code=insttype_code)
                if dlg1.exec_():
                    inst_id = dlg1.inst_id
                    if not inst_id:
                        show_error(dlg1, title=u'無法實施同一療程掛號',
                                 msg=u'無原始同一療程案件可供選擇！')
                        return
                else:
                     #show_error(self, title=u'取消同一療程掛號',  
                     #         msg=u'使用者取消同一療程案件選擇動作！')
                     dlg1.close()
                     return
            
            dt = dlg.dted_tk.dateTime()
            tk_save(name=name, pid=pid, birthday=birthday, 
                    tktype_code=tktype_code, 
                    dt=dt_tw(dt.toPyDateTime()), 
                    serial=serial, insttype_code=insttype_code, inst_id=inst_id)
            # XXX 
            self.ded.setDateTime(dt)
            self.refresh()

    def handler_dll(self, d):
        result = d['result']
        
        # dll error
        if result is None:
            self.overlay.hide()
            return

        f = d.get('f', '') 
        if f == 'get_basic':
            r, dd, t = result 
            var = d['var']
            if r == 0:
                # XXX HACK
                if var.get('aim', '') == 'fast_amend':
                    # insert fake tk and get initial inst
                    d2 = tk_save(name=dd['name'], 
                                 pid=dd['pid'], 
                                 birthday=dd['birthday'], 
                                 dt=dt_tw(dt_before(dt_now())))
                    
                    amend_code = '2'
                    tktype_code = '01'
                    inst_id = d2['inst_id']
                
                else:
                    amend_code = var['amend_code']
                    tktype_code = var['tktype_code']
                    inst_id = 0 

                    # decide ini inst_id in 補卡、同一療程
                    if amend_code == '2' or tktype_code == 'AA':
                        if amend_code == '2' and tktype_code == 'AA':
                            tp = u'補卡同一療程'
                        elif amend_code == '2' and tktype_code != 'AA':
                            tp = u'補卡'
                        elif tktype_code == 'AA':
                            tp = u'同一療程'
                        
                        dlg1 = dlg_ent_inst(par=self, 
                                            pid=dd['pid'], 
                                            name=dd['name'], 
                                            birthday=dd['birthday'], 
                                            amend_code=amend_code)
                        if dlg1.exec_():
                            inst_id = dlg1.inst_id
                            if not inst_id:
                                show_error(self, title=u'無法實施%s掛號' % tp,
                                    msg=u'無符合%s條件之起始案件可供選擇！' % tp)

                                dlg1.close()
                                self.overlay.hide()
                                return 
                        else:
                            #show_error(self, title=u'取消%s掛號' % tp, 
                            #         msg=u'使用者取消%s案件選擇動作！' % tp)
                            #dlg1.close()
                            self.overlay.hide()
                            return  

                var['amend_code'] = amend_code
                var['tktype_code'] = tktype_code
                var['inst_id'] = inst_id 
                
                # prepare newborn stuffs before tk
                try:
                    newborn = dd['newborn'].strip()                        
                    newbornmark = dd['newbornmark'].strip()
                    newbornprobe = dd['newbornprobe'].strip()
                    if newbornmark:
                        ans = qna(self, u'使用新生兒註記掛號', 
                                  u'是否使用新生兒註記掛號？', 
                                  QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)
                        if ans == QMessageBox.No:
                            newborn, newbornmark, newbornprobe = '', '', ''
                            
                        elif ans == QMessageBox.Cancel:
                            show_error(self, title=u'取消 IC卡掛號',
                                     msg=u'使用者取消 IC卡掛號！')
                            
                            self.overlay.hide()
                            return 
                except:
                    newborn, newbornmark, newbornprobe = '', '', ''
                
                dd['newborn'] = newborn
                dd['newbornmark'] = newbornmark
                dd['newbornprobe'] = newbornprobe                    
                
                # XXX update stored patient data ... 
                try:
                    cr.execute('''update patient set name = ?, birthday = ? 
                        where pid = ?''', (dd['name'], dd['birthday'], dd['pid'])) 
                    cn.commit()
                except:
                    pass

                self.dll.go(f='get_seq', var=var,
                            kw={'amend_code': amend_code, 
                                'tktype_code': tktype_code,
                                'd': dd})
            
            elif r in (4029, 4042, 4050):
                self.dll.go(f='init_sam', var=var, f_next='get_basic')
                
            else:
                var['r'] = r
                self.tk_stop(var)

        elif f == 'get_seq':
            r, dd = result 
            var = d['var']
            if r == 0:
                dd['inst_id'] = var.get('inst_id', 0)
                tk_save(**dd)
                
                self.refresh()
                self.overlay.hide()

            elif r in (4029, 4042, 5001, 5003): 
                self.dll.go(f=('init_sam' if r in (4029, 4042) else 'update_hc'), 
                            f_next='get_seq', 
                            kw_next={'amend_code': var['amend_code'], 
                                     'tktype_code': var['tktype_code'],
                                     'd': dd},
                            var=var)
            else:
                var['r'] = r
                self.tk_stop(var)

        elif f == 'update_hc' or f == 'init_sam':
            r = result 
            var = d['var']
            if r == 0:
                self.dll.go(f=d.get('f_next', ''), kw=d.get('kw_next', {}), var=var)

            else:
                if f == 'init_sam' and self.n_trial < n_sam_trial:
                    #show_msg(u'與IDC 第%s次連線認證未成功，重試中 ...' % 
                    #                                   (self.n_trial + 1,))
                    time.sleep(3) 
                    self.dll.go(f='init_sam', 
                                f_next=d.get('f_next', ''), 
                                kw_next=d.get('kw_next', {}),
                                var=var)
                    self.n_trial += 1
                
                else:
                    var['r'] = r
                    self.tk_stop(var)
        
        elif f == 'unget_seq':
            r = result
            var = d['var']
            tp = var['tp']
            arg = var['arg']
            if r == 0:
                if self.remove_tk(*arg):
                    info(self, u'IC卡退掛成功', 
                         u'%s    %s\n%s\nIC卡序『 %s 』\n掛號資料退掛成功！' % tp)
                else:
                    # XXX
                    logger.error('tk deletion error -- %s %s %s [%s]'% tp) 
            else:
                show_error(self, r, u'IC卡退掛失敗', 
                         u'%s    %s\n%s\nIC卡序『 %s 』\n無法退掛，請檢查！' % tp)
            
            self.overlay.hide()
        
        else:
            self.overlay.hide()
        
    def tk_stop(self, d):
        slc = d['slc']
        r = d['r']

        if slc == 0:
            if qna(self, u'無法實施 IC 卡掛號', u'無法取得 IC卡序號！%s\n是否繼續執行異常掛號？' % error_ic(cr, r)) == QMessageBox.Yes:
                self.tk_nic(tktype_code=d['tktype_code'])

        elif slc in (1, 4):
            show_error(self, r, u'無法實施 IC卡補卡', u'無法取得 IC卡序號，請檢查後再試！')
        
        self.n_trial = 0
        self.overlay.hide()

    def probe(self):
        w = win_probe(par=self, tk_id=self.tk_id)
        w.setWindowModality(Qt.ApplicationModal)
        w.showMaximized()

    def quit(self):
        self.close()

    def inst(self):
        w = win_inst(self)
        w.setWindowModality(Qt.ApplicationModal)
        w.show()

    def patient(self):
        w = win_patient(self)
        w.setWindowModality(Qt.ApplicationModal)
        w.show()
    
    def stat(self):
        w = win_stat(self)
        w.show()

    def app(self):
        if not is_dll_ok:
            show_error(self, title=u'無法進行申報作業', msg=u'申報作業函數庫無法載入！')
        else:
            w = win_app(self)
            w.setWindowModality(Qt.ApplicationModal)
            w.show()

    def renew(self):
        if qna(self, u'開始資料庫更新', u'資料庫更新作業將先關閉 mycis 系統。確定繼續嗎？') == QMessageBox.Yes:
            atexit.register(partial(atexit_f, 'renew'))
            self.b_ask = False
            self.close() 

    def backup(self):
        if qna(self, u'開始資料庫備份', u'資料庫備份作業將先關閉 mycis 系統。確定繼續嗎？') == QMessageBox.Yes:
            atexit.register(partial(atexit_f, 'backup'))
            self.b_ask = False
            self.close()

    def about(self):
        QMessageBox.about(self, u'mycis', 
            u'''<b>mycis</b> version %s
            <p> 發行日期：%s 
            <p>台灣健保西醫門診專用診所資訊系統（CIS）。 
            <p>Python %s - Qt %s - PyQt %s on %s''' % 
               (__version__, release_date, platform.python_version(), 
                QT_VERSION_STR, PYQT_VERSION_STR, platform.system()))

    def remove_tk(self, row, tk_id, inst_id):
        try:
            # delete all data with tk_id 
            for t in ['tk_diag', 
                      'tk_ord', 
                      'tk_med',
                      'tk_mat',
                      'tk_upload',
                      'tk_fee',]: 
                cr.execute('delete from %s where tk_id = ?' % t, (tk_id,))
            cr.execute('delete from tk where id = ?', (tk_id,)) 
            
            # delete inst_id if #tk = 0  
            r = cr.execute('''select 1 from tk where inst_id = ?''',
                              (inst_id,)).fetchone() 
            if r is None:
                cr.execute('delete from inst_app where inst_id = ?', (inst_id,))
                cr.execute('delete from inst where id = ?', (inst_id,))

            cn.commit()

            self.tbv.model().removeRows(row)
            self.refresh()
            return True

        except:
            cn.rollback()
            return False

    def keyPressEvent(self, e):
        key = e.key()
        if key == Qt.Key_Delete:
            if not self.tbv.hasFocus():
                return

            tbv = self.tbv           
            ix = tbv.currentIndex()
            if not ix or not ix.isValid():
                return
            row = ix.row()
            
            # XXX
            r = tbv.model().ls[row]
            dt = r[4]
            tp = (r[2], r[1].strip(), dt_s(dt), serial_s(*r[5:10]))
            inst_id = r[10] 
            tk_id = r[0]
            serial = r[5]

            # no untk allowed when tk has been uploaded or applied
            if cr.execute('select 1 from tk_upload where tk_id = ?', 
                          (tk_id,)).fetchone() is not None: 
                info(self, u'不可退掛', u'此看診資料已上傳，不可退掛！')
                return

            if cr.execute('select 1 from inst_app where inst_id = ?', 
                          (inst_id,)).fetchone() is not None:
                info(self, u'不可退掛', u'此看診資料已申報，不可退掛！')
                return

            if qna(self, u'退掛', u'注意：退掛後即無法回復原有掛號資料。\n是否仍要退掛\n%s    %s\n%s\n序號『 %s 』\n之掛號資料？' % tp) != QMessageBox.Yes:
                return
            
            if serial.isdigit():
                if not is_dll_ok or not is_com_ok:
                    if qna(self, u'無法使用IC卡，僅可刪除資料庫內資料', u'由於無法使用IC卡，僅可刪除資料庫掛號資料。是否仍要繼續？\n\n選擇 [Yes] 繼續，[No] 停止退掛！') != QMessageBox.Yes:
                        return
                
                    if self.remove_tk(row, tk_id, inst_id):
                        show_error(self, r, u'IC卡就醫累計次數無法回復', u'%s    %s \n%s\nIC卡序『 %s 』\n之掛號資料已從資料庫刪除，惟 IC卡功能目前無法使用，就醫累計次數無法回復！' % tp)

                else:    
                    self.dll.go(f='unget_seq', kw={'dt': dt}, 
                                var={'tp': tp, 'arg': (row, tk_id, inst_id)})
                    self.overlay.show()

            else:
                if self.remove_tk(row, tk_id, inst_id):
                    info(self, u'退掛成功', 
                    u'%s    %s\n%s\n序號『 %s 』\n之掛號資料已從資料庫刪除！' % tp)
        
        else:
            QMainWindow.keyPressEvent(self, e)
    
    def closeEvent(self, e):
        if self.b_ask:
            a = qna(self, u'離開 mycis', u'確定離開mycis嗎？\n\n選擇 [Cancel] 將繼續留在mycis。\n選擇 [No] 不備份直接離開。\n選擇 [Yes] 離開並執行本機及遠端備份。', QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel) 
            if a == QMessageBox.Cancel:
                e.ignore()
            else:
                kill_adobe()
                if a == QMessageBox.Yes:
                    atexit.register(partial(atexit_f, 'backup', False))
 
        for i in [self.refresher, self.uploader]:
            i.end()
        
        n = self.class_name()
        try:
            tbv = self.tbv 
            for i in range(tbv.model().columnCount()):
                sts.setValue('%s/tbv/%s/width' % (n, i), 
                        QVariant(tbv.columnWidth(i)))
        except:
            pass
        
        sts.setValue('%s/state' % n, QVariant(self.saveState()))

    def event(self, e):
        if e.type() == QEvent.WindowActivate:
            self.refresh()
        return QMainWindow.event(self, e) 

class win_fav(win, Ui_win_fav):

    def __init__(self, par=None, staff_id=1):
        win.__init__(self, par)
        self.setupUi(self)
        
        # no menubar and toolbar
        self.mnb.setVisible(False)
        self.tb.setVisible(False)

        self.wdg = w = wdg_fav()
        self.setCentralWidget(w)
        
        # keyboard shortcut
        for i, k in [('done',    ('F2',)),
                     ('add_fav', ('F3',)),
                     ('search',  ('F4',)), 
                     ('redo',    ('Ctrl+R',)),
                     ('undo',    ('Ctrl+U',)),
                     ('focus',   ('Ctrl+K',)),
                     ('import',  ('Ctrl+I',)),
                     ('export',  ('Ctrl+E',)),
                     ]:
            s = 'act_%s' % i
            try:
                a = getattr(self, s)
            except:
                setattr(self, s, QAction(self))
            finally:
                a = getattr(self, s)
            a.setShortcuts([QKeySequence(kk) for kk in k])
            self.connect(a, SIGNAL('triggered()'), partial(self.handler_act, i))
            self.addAction(a)

        favs = import_favs(staff_id, cr) 
        self.favs_ini = deepcopy(favs)
        self.favs = deepcopy(favs)
        self.staff_id = staff_id

        tbv = self.wdg.tbv_fav
        self.connect(tbv.verticalHeader(), SIGNAL('sectionClicked(int)'), 
                     self.ent_fav)
        self.connect(tbv, SIGNAL('activated(QModelIndex)'), self.tbv_activated) 
        
        self.b_save = False 
        
        #self.undo_stack = QUndoStack(self)
        # debug only
        #self.undo_stack_view = QUndoView(self.undo_stack)
        #self.undo_stack_view.show()
        #self.undo_stack.push(cmd_fav(self, d0, d1,'ix:%s %s --> %s' % (ix, d0, d1)))

        self.restoreState(sts.value('%s/state' % self.class_name()).toByteArray())
        
        QTimer.singleShot(0, self.init)
        
        self.connect(self.wdg.led_find, SIGNAL('textChanged(QString)'), 
                     self.test_empty_favs)
    
    def test_empty_favs(self, t):
        if t and not self.favs:
            self.wdg.led_find.clear()
            self.handler_act('add_fav')           

    def tbv_activated(self, ix):
        if ix and ix.isValid():
            self.ent_fav(ix.row())

    def ent_fav(self, i):
        self.update_tbv(self.favs[i])
    
    def update_tbv_favs(self):
        tbv = self.wdg.tbv_fav
        tbv.setModel(model_fav(ls=self.favs, 
                               meta={'header': (u'', u'代碼', u'名稱')}))     
        tbv.setItemDelegate(delg_fav(self))
        tbv.setColumnHidden(0, True)

    def init(self):
        w = self.wdg
        favs = self.favs
        self.update_tbv_favs()

        if favs:
            self.update_tbv(favs[0])
            w.tbv_fav.selectRow(0)

        for i in ['spl_1', 'spl_2']:
            getattr(w, i).restoreState(sts.value('%s/%s' % (self.class_name(), 
                                                            i)).toByteArray())
        self.resize_tbv(['tbv_fav', 'tbv_diag', 'tbv_ord', 'tbv_med', 'tbv_mat'])
        w.led_find.setFocus()
        
        self.pop = QTreeView()
        self.pop.setUniformRowHeights(True)        
        self.pop.setHeaderHidden(True)
        self.completer = QCompleter()
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setPopup(self.pop)
        self.connect(self.completer, SIGNAL('activated(QModelIndex)'), self.hit) 

        w.led_find.setCompleter(self.completer)
        
        self.completer.setModel(model_orig)
        self.completer.setModelSorting(QCompleter.CaseSensitivelySortedModel)
        self.completer.popup().setColumnWidth(0, 450)
        self.completer.popup().setColumnHidden(2, True)

    def hit(self, ix):
        m = ix.model()
        self.enter_item(unicode(m.data(m.index(ix.row(), ix.column() + 2), Qt.DisplayRole).toString()))
        QTimer.singleShot(0, self.focus)

    def handler_act(self, i):
        if i == 'add_fav':
            dlg = dlg_fav(self) 
            if dlg.exec_():
                self.favs.append({
                    'name': unicode(dlg.led_name.text()), 
                    'code': unicode(dlg.led_code.text()), 
                    'fav_id': 0,
                    'diag': [], 'ord': [], 'med': [], 'mat': [],
                })
                self.update_tbv_favs()
                row = len(self.favs) - 1
                self.update_tbv(self.favs[row])
                tbv = self.wdg.tbv_fav
                tbv.selectRow(row)
                tbv.showRow(row)
                #QTimer.singleShot(0, self.wdg.tbv_fav.scrollToBottom)

        elif i == 'search':
            pass

        elif i == 'redo':
            pass

        elif i == 'undo':
            pass

        elif i == 'done':
            
            start_time = time.time()
            print('beginning transaction')
            favs_i = self.favs_ini
            favs_f = self.favs
            favs = diff_favs(favs_i, favs_f)
            
            for fav in favs['l_insert']:

                cr.execute('''insert into fav (code, name, staff_id) 
                    values (?, ?, ?)''', (fav['code'], fav['name'], self.staff_id))
                fav_id = cr.execute('select last_insert_rowid()').fetchone()[0]

                for t in ['diag', 'ord', 'med', 'mat']:
                    table = 'fav_%s' % t
                    cl = columns(table)
                    if fav[t]:
                        cr.executemany('insert into %s (%s) values (%s)' % (table, ', '.join(cl), ', '.join(['?'] * len(cl))), [tuple([fav_id,] + ll[1:]) for ll in fav[t]])

            id_del = [(fav['fav_id'],) for fav in favs['l_delete']]
            if id_del:
                for t in ['diag', 'ord', 'med', 'mat']:
                    table = 'fav_%s' % t
                    cl = columns(table)
                    cr.executemany('delete from %s where fav_id = ?' % (table,), 
                                   id_del)
                cr.executemany('delete from fav where id = ?', id_del)

            for nn, fav in enumerate(favs['l_update_i']):
                fav1 = favs['l_update_f'][nn] 
                if fav['code'] != fav1['code'] or fav['name'] != fav1['name']:
                    cr.execute('update fav set code = ?, name = ? where id = ?',
                            (fav1['code'], fav1['name'], fav1['fav_id']))

                for t in ['diag', 'ord', 'med', 'mat']:
                    d = diff(fav[t], fav1[t]) 
                    table = 'fav_%s' % t
                    cl = columns(table)
                    
                    if d['l_insert']:
                        cr.executemany('insert into %s (%s) values (%s)' % (table, ', '.join(cl), ', '.join(['?'] * len(cl))), d['l_insert'])
                    
                    if d['l_delete']:
                        cr.executemany('delete from %s where %s = ? and %s = ?' % (table, cl[0], cl[1]), ids(d['l_delete']))

                    if d['l_update']:
                        cr.executemany('update %s set %s where %s' % (table, ', '.join([ll + ' = ?' for ll in cl[2:]]), ' and '.join([ll + ' = ?' for ll in cl[:2]])), [tuple(ll[2:] + ll[:2]) for ll in d['l_update']])
            
            cn.commit()
            self.favs_ini = deepcopy(self.favs)
            print('elapsed total: %f seconds' % (time.time() - start_time))
            self.send(cnd='saved')
            self.close()

        elif i == 'focus':
            self.focus()

        elif i == 'import':
            pass

        elif i == 'export':
            for fav in self.favs:
                pass

    def focus(self):
        w = self.wdg
        w.led_find.setFocus()
        w.led_find.selectAll()

    def enter_item(self, iid):
        typ, i = iid.split('_')
        id0 = int(i)

        fav_id = self.fav_id
        w = self.wdg   
        b_inserted = False

        if typ == 'diag':
            m = w.tbv_diag.model()
            if id0 in [l[1] for l in m.ls]:
                info(self, u'診斷重複輸入', u'此診斷已輸入，請另選其他診斷！')
                return

            else:
                m.ls.append([fav_id, id0])
                m.insertRows(m.rowCount())
                b_inserted = True

        elif typ == 'ord':  
            code = dic_all_inv['ord'].get(id0)[0]
            m = w.tbv_ord.model()
            if id0 in [l[1] for l in m.ls]:
                info(self, u'處置重複輸入', u'此處置已輸入，請另選其他處置！') 
                return

            else:
                oid = dic_all['ocode'][json.dumps(ocode_def(code))]
                percent = 100 
                qty = 1 
                m.ls.append([fav_id, id0, oid, percent, qty])
                m.insertRows(m.rowCount())
                b_inserted = True

        elif typ == 'med':
            code = dic_all_inv['med'].get(id0)[0]
            m = w.tbv_med.model()
            if id0 in [l[1] for l in m.ls]:
                info(self, u'藥品重複輸入', u'此藥品已輸入，請另選其他藥品！')
                return

            else:
                id1 = dic_all['usage'].get('PO') 
                id2 = dic_all['freq'].get('TID') 
                oid = dic_all['ocode'].get(json.dumps(ocode_def(code, typ='med'))) 
                days = 3 
                dosage = 1.0 
                # fav_id, med_id, usage_id, freq_id, ocode_id, days, dosage
                m.ls.append([fav_id, id0, id1, id2, oid, days, dosage])
                m.insertRows(m.rowCount())
                b_inserted = True

        elif typ == 'mat':  
            code = dic_all_inv['mat'].get(id0)[0]
            m = w.tbv_mat.model()
            if id0 in [l[1] for l in m.ls]:
                info(self, u'特材重複輸入', u'此特材已輸入，請另選其他特材！')
                return

            else:
                oid = dic_all['ocode'][json.dumps(ocode_def(code))]
                percent = 100 
                qty = 1 
                m.ls.append([fav_id, id0, oid, percent, qty])
                m.insertRows(m.rowCount())
                b_inserted = True

        self.resize_tbv(['tbv_%s' % typ,])
        if b_inserted:
            w.led_find.clear() 
        
    def update_tbv(self, fav):
        self.favs0 = deepcopy(self.favs)

        w = self.wdg

        self.fav_id = fav['fav_id']
        w.tbv_diag.setModel(
            model_diag(ls=fav['diag'], 
                       meta={'header': (u'ICD10-CM', u'疾病名稱')}))
        w.tbv_diag.show()

        w.tbv_ord.setModel(
            model_ord_fav(ls=fav['ord'], dt=now(),
                          meta={'header': (u'健保代碼', u'處置名稱', u'成數', 
                                           u'總數', u'申報模式')}))
        w.tbv_ord.setItemDelegate(delg_ord_fav(self))
        w.tbv_ord.show()

        w.tbv_med.setModel(
            model_med_fav(ls=fav['med'], dt=now(),
                       meta={'header': (u'健保代碼', u'藥品名稱', u'劑量', u'頻率', 
                                        u'天數', u'用法', u'申報模式')}))           
        w.tbv_med.setItemDelegate(delg_med_fav(self))
        w.tbv_med.show()
        
        w.tbv_mat.setModel(
            model_mat_fav(ls=fav['mat'], dt=now(),
                          meta={'header': (u'健保代碼', u'特材名稱', u'成數', 
                                           u'總數', u'申報模式')}))
        w.tbv_mat.setItemDelegate(delg_mat_fav(self))
        w.tbv_mat.show()
        
        for s in ['diag', 'ord', 'med', 'mat']:
            t = getattr(w, 'tbv_%s' % s)
            self.connect(t.model(), SIGNAL('dataChanged(QModelIndex, QModelIndex)'),
                         self.edited)

    def edited(self, i, j):
        snd = self.sender()
        for s in ['diag', 'ord', 'med', 'mat']:
            t = getattr(self.wdg, 'tbv_%s' % s)
            if snd is t.model():
                print('edited in %s' % s)
                break

    def resize_tbv(self, l): 
        w = self.wdg
        for i in l:
            try:
                for j in range(getattr(w, i).model().columnCount()):
                    n, ok = sts.value('%s/%s/%s/width' % (self.class_name(), i, j)).toInt()
                    if ok:
                        getattr(w, i).setColumnWidth(j, n)
            except:
                pass
    
    def save_widgets_pos(self):
        w = self.wdg
        class_name = self.class_name()

        for i in ['spl_1', 'spl_2',]: 
            sts.setValue('%s/%s' % (class_name, i), 
                QVariant(getattr(w, i).saveState()))

        for i in ['tbv_fav', 'tbv_diag', 'tbv_ord', 'tbv_med', 'tbv_mat']:
            tbv = getattr(w, i)
            for j in range(tbv.model().columnCount()):
                sts.setValue('%s/%s/%s/width' % (class_name, i, j), 
                    QVariant(tbv.columnWidth(j)))
        
        sts.setValue('%s/state' % class_name, QVariant(self.saveState()))
        
    def save(self):
        #try:      
        #    cn.commit()
        #    
        #    self.update_tbv(fav)
        #    return True
        # 
        #except:
        #    cn.rollback()
        #    return False
        pass

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Delete:
            w = self.wdg
            tbv = None
            for s in ['fav', 'diag', 'ord', 'med', 'mat']:
                t = getattr(w, 'tbv_%s' % s)
                if t.hasFocus():
                    tbv = t
                    break

            if tbv is None:
                return
            
            ix = tbv.currentIndex()
            if not ix or not ix.isValid():
                return
            
            row = ix.row()
            m = tbv.model()
            m.removeRows(row)
            if s == 'fav':
                favs = self.favs
                if favs:
                    row1 = row - 1 if row else 0
                    self.update_tbv(favs[row1])
                    tbv = self.wdg.tbv_fav
                    tbv.selectRow(row1)
                    tbv.showRow(row1)

                else:
                    # clear all views
                    self.update_tbv({'name': '', 'code': '', 'fav_id': 0,
                    'diag': [], 'ord': [], 'med': [], 'mat': [],})

            w.led_find.clear()
            self.focus()

        else:
            QMainWindow.keyPressEvent(self, e)

    def closeEvent(self, e):
        self.save_widgets_pos()

        if self.b_save:
            self.save()    

class lw_history(QListWidget):

    def __init__(self, par):
        QListWidget.__init__(self, par)
        self.par = par
        self.p = None
    
    def contextMenuEvent(self, e):
        m = QMenu(self)
        l = [(u'匯入此次看診資料', 'import'), 
             None, 
             (u'轉至此次看診', 'set_tk'), 
            ]  
        for ll in l:
            if ll is None:
                m.addSeparator()
            else:
                s, f = ll
                m.addAction(s, partial(self.handler, f))
        
        self.p = e.pos() 
        m.exec_(e.globalPos())

    def handler(self, f):
        ix = self.itemAt(self.p)
        if ix is None:
            return
        try:
            d = json.loads(unicode(ix.data(Qt.UserRole).toString()))
        except:
            return

        if f == 'import':
            info(self, u'test', u'dt: %s, tk_id: %s, soap: %s' % (d['dt'], d['tk_id'], d['soap']))
        elif f == 'set_tk':
            pass

class win_probe(win, Ui_win_probe):

    def __init__(self, par=None, tk_id=0):
        win.__init__(self, par)
        self.setupUi(self)
        
        #self.setStyleSheet('''
        #    QMainWindow::separator {
	#    	width: 1px;
	#	height: 1px;
	#    }
        #
        #    QDockWidget::title {
        #        text-align: center; 
        #        background: lightgray;
        #        font: bold 14px;
        #    }
        #''')
        
        # no menubar and toolbar
        self.mnb.setVisible(False)
        self.tb.setVisible(False)

        self.tw = t = QTabWidget()
        t.setTabPosition(QTabWidget.South)
        t.setTabsClosable(False)
        t.setDocumentMode(False)
        self.setCentralWidget(t)
        i = t.addTab(wdg_probe(), QIcon(':/res/img/stethoscope.png'), u'看診內容')  
        w = t.widget(i)

        # keyboard shortcut
        for i, k in [('done',       ('F2',)),
                     ('favs',       ('F3',)),
                     ('search',     ('F4',)), 
                     ('printf',     ('F5',)),
                     ('ic',         ('F6',)),
                     ('add_as_fav', ('F7',)),
                     ('reserve',    ('F8',)),
                     ('refer',      ('F9',)),
                     ('redo',       ('Ctrl+R',)),
                     ('undo',       ('Ctrl+U',)),
                     ('focus',      ('Ctrl+K',)),
                     ]:

            s = 'act_%s' % i
            try:
                a = getattr(self, s)
            except:
                setattr(self, s, QAction(self))
            finally:
                a = getattr(self, s)
            a.setShortcuts([QKeySequence(kk) for kk in k])
            self.connect(a, SIGNAL('triggered()'), partial(self.handler_act, i))
            self.addAction(a)

        self.tk = tk = import_tk(tk_id, cr)
        self.tk_i = deepcopy(self.tk)
        self.setWindowIcon(QIcon(QPixmap(':/res/img/user-%s.png' % gender(tk['pid']))))
        self.setWindowTitle(tk['name'] + '  ' + dt_s(tk['birthday'], True))
         
        self.fav_refresher = fav_refresher(self)
        m = self.fav_refresher
        self.connect(m, SIGNAL('begin'), self.begin_refresh_model)
        self.connect(m, SIGNAL('done'), self.refresh_model)
        m.go(dt=tk['dt'], staff_id=1)

        self.undo_stack = QUndoStack(self)
        #self.undo_stack_view = QUndoView(self.undo_stack)
        #self.undo_stack_view.show()
        #self.undo_stack.push(cmd_tk(self, d0, d1,'ix:%s %s --> %s' % (ix, d0, d1)))

        self.dll = dll(self)
        self.connect(self.dll, SIGNAL('msg_dll'), self.handler_dll)
        
        # setup dwgs
        self.dwg = dwg = QDockWidget(u'就診歷史', self)
        dwg.setObjectName('dwg') 
        dwg.setFeatures(QDockWidget.NoDockWidgetFeatures)
        dwg.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)

        self.lw_history = lw = lw_history(self)
        
        w = QWidget(self)
        lo = QVBoxLayout()
        lo.addWidget(lw)
        w.setLayout(lo)
        dwg.setWidget(w)
        self.addDockWidget(Qt.RightDockWidgetArea, dwg)
       
        self.dwg1 = dwg1 = QDockWidget(u'註記與SOAP', self)
        dwg1.setObjectName('dwg1') 
        dwg1.setFeatures(QDockWidget.NoDockWidgetFeatures)
        dwg1.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
        
        self.ted_note = QTextEdit(self)
        self.ted_soap = QTextEdit(self)
        self.ted_past = QTextEdit(self)
        self.spl1 = spl1 = QSplitter(Qt.Vertical, self)
        spl1.addWidget(self.ted_note)
        spl1.addWidget(self.ted_soap)
        spl1.addWidget(self.ted_past)
        
        w1 = QWidget(self)
        lo1 = QVBoxLayout()
        lo1.addWidget(spl1)
        w1.setLayout(lo1)
        dwg1.setWidget(w1)
        self.addDockWidget(Qt.LeftDockWidgetArea, dwg1)

        self.completer = QCompleter()
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.popup = QTreeView()
        self.popup.setUniformRowHeights(True)        
        self.popup.setHeaderHidden(True)
        self.completer.setPopup(self.popup)
        self.tw.widget(0).led_find.setCompleter(self.completer)
        self.connect(self.completer, SIGNAL('activated(QModelIndex)'), self.hit)

        self.connect(lw, SIGNAL('currentRowChanged(int)'), self.get_history_item)

        self.is_busy = False
        self.b_save = False 
        
        self.restoreState(sts.value('%s/state' % self.class_name()).toByteArray())
        
        QTimer.singleShot(0, self.init)
    
    def apply_tk_load_rules(self, tk):
        # insert diags of the same inst if tk['diag'] is empty:
        if not tk['diag']:
            for i in cr.execute('''select distinct tk_diag.diag_id from tk_diag 
                                   join tk on tk_diag.tk_id = tk.id 
                                   where tk.inst_id in 
                                   (select inst_id from tk where id = ?)''',
                                   (tk_id,)).fetchall():
                tk['diag'].append([tk_id, i[0]])
        return tk

    def init(self):
        class_name = self.class_name()
        for (i, j) in [(0, 'spl'),]:
            getattr(self.tw.widget(i), j).restoreState(sts.value('%s/%s' % (class_name, j)).toByteArray())

        for i in ['spl1',]:
            getattr(self, i).restoreState(sts.value('%s/%s' % (class_name, i)).toByteArray())

        tk = self.apply_tk_load_rules(self.tk)
        self.update_tbv(tk)    
        self.resize_tbv(['tbv_diag', 'tbv_ord', 'tbv_med', 'tbv_mat'])
        self.focus()
        note = cr.execute('''select note from patient 
                             where id = (select patient_id from tk where id = ?)''',
                          (tk['tk_id'],)).fetchone()[0]
        self.ted_note.setText(note)
        self.ted_soap.setText(tk['soap'])
        
        tk_id = tk['tk_id']
        # get historical soap, diag, ord, med, mat
        lw = self.lw_history
        for (dtt, ii, soap) in cr.execute('''select dt, id, soap from tk 
                    where patient_id = (select patient_id from tk where id = ?) 
                    order by dt desc''', (tk_id,)).fetchall():
            d = {} 
            d['dt'] = dtt
            d['tk_id'] = ii
            d['soap'] = soap
            d['diag'] = [] 
            for r in cr.execute('''select distinct diag.code, diag.name_zh from diag
                                   join tk_diag on diag.id = tk_diag.diag_id 
                                   where tk_diag.tk_id = ? order by diag.code''', 
                                   (ii,)).fetchall():
                l = [unicode(rr).strip() for rr in r]
                l[0], l[1] = dic_custom_code_name.get(l[0], l[:2])
                d['diag'].append(l)

            d['ord'] = []
            for r in cr.execute('''select ord.code, ord.name from tk_ord
                                      join ord on tk_ord.ord_id = ord.id
                                      join tk on tk_ord.tk_id = tk.id
                                      where tk_ord.tk_id = ? order by ord.code''',
                                      (ii,)).fetchall():
                l = [unicode(rr).strip() for rr in r]
                l[0], l[1] = dic_custom_code_name.get(l[0], l[:2])
                d['ord'].append(l)

            d['med'] = []
            for r in cr.execute('''select med.code, med.name, freq.code, 
                                          tk_med.days from tk_med 
                             join med on tk_med.med_id = med.id 
                             join freq on tk_med.freq_id = freq.id 
                             where tk_med.tk_id = ? order by med.code''',
                             (ii,)).fetchall():
                l = [unicode(rr).strip() for rr in r]
                l[0], l[1] = dic_custom_code_name.get(l[0], l[:2])
                d['med'].append(l)

            d['mat'] = []
            for r in cr.execute('''select mat.code, mat.name from tk_mat
                                      join mat on tk_mat.mat_id = mat.id
                                      join tk on tk_mat.tk_id = tk.id
                                      where tk_mat.tk_id = ? order by mat.code''',
                                      (ii,)).fetchall():
                l = [unicode(rr).strip() for rr in r]
                l[0], l[1] = dic_custom_code_name.get(l[0], l[:2])
                d['mat'].append(l)
            it = QListWidgetItem(QIcon(':/res/img/patient.png'), dt_s(dtt, True))
            it.setData(Qt.UserRole, QVariant(json.dumps(d)))
            lw.addItem(it)
        
        lw.setCurrentRow(1)
        
        # XXX can't be taken out init !!
        self.overlay = overlay(self)

    def update_favs(self, d):
        cnd = d['cnd']  
        if cnd == 'saved':
            self.fav_refresher.go(dt=self.tk['dt'], staff_id=1)

    def handler_act(self, i):
        if i == 'add_as_fav':
            dlg = dlg_fav(self) 
            if dlg.exec_():
                cr.execute('''insert into fav (code, name, staff_id) 
                    values (?, ?, ?)''', 
        (unicode(dlg.led_name.text()), unicode(dlg.led_code.text()), self.staff_id))
                fav_id = cr.execute('select last_insert_rowid()').fetchone()[0]

                for t in ['diag', 'ord', 'med', 'mat']:
                    table = 'fav_%s' % t
                    cl = columns(table)
                    ls = getattr(self.tw.widget(0), 'tbv_%s' % t).model().ls
                    if ls:
                        cr.executemany('insert into %s (%s) values (%s)' % (table, ', '.join(cl), ', '.join(['?'] * len(cl))), [tuple([fav_id,] + ll[1:]) for ll in ls])

        elif i == 'favs':
            w = win_fav(par=self, staff_id=1)
            w.setWindowModality(Qt.ApplicationModal)
            w.showMaximized()
            self.connect(w, SIGNAL('msg_%s' % w.class_name()), self.update_favs)

        #elif i == 'search':
        #elif i == 'printf':
        #elif i == 'ic':
        #elif i == 'redo':
        #elif i == 'undo':
        #elif i == 'reserve':
        #elif i == 'refer':
        elif i == 'done':
            tk = self.tk
            tk_id = tk['tk_id']
            if tk['diag'] and (tk['ord'] or tk['med'] or tk['mat']):
                if self.is_busy:
                    logger.error(u"consecutive press of 'done'") 
                    return
                
                if not self.save():
                    logger.error('db insert error: %s' % tk)
                    info(self, u'資料庫寫入失敗', u'資料庫寫入失敗，請檢查是否有重複診斷、處置及藥品！')
                    return
                self.b_save = False
               
                # XXX ic writing complexities
                #if is_duplicate_tk(tk_id, cr):
                #    info(self, u'存在未寫入IC卡之較晚同日就診紀錄', u'『由於健保局讀卡機控制軟體之邏輯問題』\n寫入同日就診紀錄必須從掛號時間較晚者開始！\n\n資料已存檔；請稍候再次寫卡！')
                #    self.close()
                #    return
                #  
                #self.is_busy = True
                #a = cr.execute('''select amend.code from tk 
                #                  join amend on tk.amend_id = amend.id
                #                  where tk.id = ?''', 
                #                  (tk_id,)).fetchone()[0]
                #self.dll.go(f='write', kw={'tk_id': tk_id, 'amend_code': a}) 
                #self.overlay.show()
                
            else:
                if not tk['diag']:
                    s = u'無診斷'
                    w.led_find.setFocus()
                
                elif not (tk['ord'] or tk['med'] or tk['mat']):
                    s = u'無處置或藥品或特材'
                    w.led_find.setFocus()
                
                show_error(self, title=u'看診無法完成', 
                         msg=u'看診資料未輸入完整，請檢查！\n（原因：%s）' % s)
        
        elif i == 'focus':
            self.focus()

    def set_tk(self, tk):
        pass

    def focus(self):
        w = self.tw.widget(0)
        w.led_find.setFocus()
        w.led_find.selectAll()

    def enter_item(self, iid):
        typ, i = iid.split('_')
        id0 = int(i)

        tk_id = self.tk['tk_id']
        w = self.tw.widget(0)   
        b_inserted = False

        if typ == 'fav':
            d = {}
            for t in ['diag', 'ord', 'med', 'mat']:
                d[t] = [list(r[1:]) for r in cr.execute('select * from fav_%s where fav_id = ?' % (t,), (id0,)).fetchall()]
                for ll in d[t]:
                    m = getattr(w, 'tbv_%s' % t).model() 
                    if ll[0] not in [l[1] for l in m.ls]:
                        #if t == 'med':
                        # tk_id, med_id, usage_id, freq_id, ocode_id, days, dosage
                        #set([l[-2] for l in m.ls])
                        ml = [tk_id,] + ll
                        if t != 'diag': # note that fav_xxx has no sign
                            ml += ['',]
                        m.ls.append(ml) 
                        m.insertRows(m.rowCount())
                        b_inserted = True

        if b_inserted:
            QTimer.singleShot(0, w.led_find.clear)

    def get_history_item(self, i):
        ix = self.lw_history.item(i)
        try:
            d = json.loads(unicode(ix.data(Qt.UserRole).toString()))
        except:
            return
        l = []
        if d['soap']:
            l.append(d['soap'])
            l.append('=' * 35)
        for t in ['diag', 'ord', 'med', 'mat']:
            for r in d[t]:
                l.append((u'%s %20s %s x %s days' if t == 'med' else '%s %20s') % tuple(r))
            if d[t]:
                l.append('=' * 35)
        self.ted_past.setText('\n'.join(l)) 

    def update_tbv(self, tk):
        w = self.tw.widget(0)
        w.tbv_diag.setModel(
            model_diag(ls=tk['diag'], 
                        meta={'header': (u'ICD10-CM', u'疾病名稱')}))
        w.tbv_diag.show()

        w.tbv_ord.setModel(
            model_ord(ls=tk['ord'], dt=tk['dt'],
                       meta={'header': (u'代碼', u'處置名稱', u'單價', 
                                        u'成數', u'總數', u'小計', u'申報模式')}))
        w.tbv_ord.setItemDelegate(delg_ord(self))
        w.tbv_ord.show()

        w.tbv_med.setModel(
            model_med(ls=tk['med'], dt=tk['dt'],
                       meta={'header': (u'代碼', u'藥品名稱', u'劑量', u'頻率', 
                                        u'天數', u'總數', u'用法', u'單價', u'小計',
                                        u'申報模式')}))           
        w.tbv_med.setItemDelegate(delg_med(self))
        w.tbv_med.show()
        
        w.tbv_mat.setModel(
            model_mat(ls=tk['mat'], dt=tk['dt'],
                       meta={'header': (u'代碼', u'特材名稱', u'單價', 
                                        u'成數', u'總數', u'小計', u'申報模式')}))
        w.tbv_mat.setItemDelegate(delg_mat(self))
        w.tbv_mat.show()

    #    w.cbo_insttype.setCurrentIndex(w.cbo_insttype.findData(QVariant(tk['insttype_id']))) 
    #    w.chk_severe.setChecked(tk['is_severe'])
    #    w.chk_cont.setChecked(tk['is_cont'])
    #
    #def set_insttype(self, insttype_code):
    #    w = self.tw.widget(0)
    #    r = cr.execute('select code, name, id from insttype where code = ?', 
    #                   (insttype_code,)).fetchone()
    #    txt = r[0] + ': ' + r[1] if r else ''
    #    ix = w.cbo_insttype.findText(txt)
    #    if ix != -1:
    #        w.cbo_insttype.setCurrentIndex(ix)

    def resize_tbv(self, l): 
        w = self.tw.widget(0)
        for i in l:
            try:
                tbv = getattr(w, i)
                for j in range(tbv.model().columnCount()):
                    n, ok = sts.value('%s/%s/%s/width' % (self.class_name(), i, j)).toInt()
                    if ok:
                        tbv.setColumnWidth(j, n)
                if i[-4:] == 'diag':
                    tbv.horizontalHeader().hide()
            except:
                pass
    
    def begin_refresh_model(self):
        self.tw.widget(0).led_find.setEnabled(False) 

    def refresh_model(self, i):
        self.tw.widget(0).led_find.setEnabled(True)
        c = self.completer
        model, dic_custom_code_name = i 
        with open(cat('cache', 'dic_custom_code_name.json'), 'wb') as outfile:
            json.dump(dic_custom_code_name, outfile)
        c.setModel(model)
        c.setModelSorting(QCompleter.CaseSensitivelySortedModel)
        c.popup().setColumnWidth(0, 150)
        c.popup().setColumnHidden(2, True)

    def hit(self, ix):
        m = ix.model()
        self.enter_item(unicode(m.data(m.index(ix.row(), ix.column() + 2), Qt.DisplayRole).toString()))
        QTimer.singleShot(0, self.focus)

    def save_widgets_pos(self):
        w = self.tw.widget(0)
        class_name = self.class_name()

        for i in ['spl',]:
            sts.setValue('%s/%s' % (class_name, i), QVariant(getattr(w, i).saveState()))
        for i in ['spl1',]:
            sts.setValue('%s/%s' % (class_name, i), QVariant(getattr(self, i).saveState()))

        for i in ['tbv_diag', 'tbv_ord', 'tbv_med', 'tbv_mat']:
            tbv = getattr(w, i)
            for j in range(tbv.model().columnCount()):
                sts.setValue('%s/%s/%s/width' % (class_name, i, j), 
                    QVariant(tbv.columnWidth(j)))
        
        sts.setValue('%s/state' % class_name, QVariant(self.saveState()))
        
    def save(self):
        try:      
            tk_i = self.tk_i
            tk_f = self.tk
            tk_id = self.tk['tk_id']
            
            #cr.execute('''update inst set insttype_id = ?, is_severe = ?, 
            #                              is_cont = ? where id = ?''', 
            #   (tk['insttype_id'], tk['is_severe'], tk['is_cont'], tk['inst_id']))
            
            note = unicode(self.ted_note.toPlainText()).strip()
            if note != tk_i['note'].strip():
                cr.execute('''update patient set note = ? 
                    where id = (select patient_id from tk where id = ?)''', 
                    (note, tk_id)) 

            soap = unicode(self.ted_soap.toPlainText()).strip()
            if soap != tk_i['soap'].strip():
                cr.execute('update tk set soap = ? where id = ?', (soap, tk_id))

            for t in ['diag', 'ord', 'med', 'mat']:
                d = diff(tk_i[t], tk_f[t])
                table = 'tk_%s' % t
                cl = columns(table)
                
                if d['l_insert']:
                    cr.executemany('insert into %s (%s) values (%s)' % (table, ', '.join(cl), ', '.join(['?'] * len(cl))), d['l_insert'])
                    
                if d['l_delete']:
                    cr.executemany('delete from %s where %s = ? and %s = ?' % (table, cl[0], cl[1]), ids(d['l_delete']))

                if d['l_update']:
                    cr.executemany('update %s set %s where %s' % (table, ', '.join([ll + ' = ?' for ll in cl[2:]]), ' and '.join([ll + ' = ?' for ll in cl[:2]])), [tuple(ll[2:] + ll[:2]) for ll in d['l_update']])

            cn.commit()
            self.tk_i = deepcopy(self.tk)
            print('save tk successfully')
            return True
            
        except:
            print('failure saving tk')
            cn.rollback()
            return False

    def handler_dll(self, d):
        result = d['result']
        if result is None:
            logger.error('dll error in %s' % self.class_name())
        
        else:
            f = d.get('f', '') 
            if f == 'write':
                r, t = result 
                if r == 0:
                    for tbl, sgn, i1, i2 in t:
                        cr.execute('''update tk_%s set sign = ? 
                                      where tk_id = ? 
                                      and %s_id = ?''' % (tbl, tbl), (sgn, i1, i2))
                    cn.commit()
                    
                    # XXX 30/06/11 09:48:10
                    b = False
                    #for i in ['prscr', 'chk']: XXX 05/01/13 Do not print prscr
                    for i in ['chk']:
                        try:
                            self.printf(i)                
                        except:
                            logger.error('print error')
                            b = True
                    if b:
                        show_error(self, title=u'無法列印', 
                            msg=u'請手動列印此案件資料！')
    
                    self.close()
    
                else:
                    if qna(self, u'無法寫入IC卡', u'無法寫入IC卡：%s\n請檢查後重試一次。\n\n選擇 [Yes] 停留在此看診畫面，[No] 離開！' % error_ic(cr, r)) == QMessageBox.No:
                        self.close()        
            
        self.is_busy = False
        self.overlay.hide()
    
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Delete:
            tbv = None
            w = self.tw.widget(0)
            for s in ['diag', 'ord', 'med', 'mat']:
                t = getattr(w, 'tbv_%s' % s)
                if t.hasFocus():
                    tbv = t
                    break

            if tbv is None:
                return
            
            ix = tbv.currentIndex()
            if not ix or not ix.isValid():
                return
            tbv.model().removeRows(ix.row())
        
        else:
            QMainWindow.keyPressEvent(self, e)

    def closeEvent(self, e):
        self.save_widgets_pos()

        if self.b_save:
            self.save()    
        
        for i in [self.fav_refresher,]:
            i.end()

class win_inst_base(win, Ui_win_inst):

    def __init__(self, par=None):
        win.__init__(self, par)
        self.setupUi(self)
       
        trv = self.trv
        trv.setEditTriggers(QAbstractItemView.NoEditTriggers)
        trv.setHeaderHidden(True)
        trv.setAlternatingRowColors(True)
        trv.setSelectionBehavior(QTreeView.SelectRows)
        trv.setSelectionMode(QTreeView.ExtendedSelection)
        trv.setUniformRowHeights(True)        
        trv.setItemsExpandable(False)
        self.connect(trv, SIGNAL('doubleClicked(QModelIndex)'), self.probe)
        self.connect(trv, SIGNAL('clicked(QModelIndex)'), self.click) 
                
        self.pbn = QPushButton(self)
        self.pbn.setText(u'顯示案件(&D)')
        self.connect(self.pbn, SIGNAL('clicked()'), self.display)    
        
        for j in ['',]:
            setattr(self, 'item_%s' % j, [
                ('p_sl', u'列印', '', False),
            ])

            setattr(self, 'mnu_%s' % j, QMenu(self))
            mnu = getattr(self, 'mnu_%s' % j)
            for i in getattr(self, 'item_%s' % j):                
                if i is None:
                    mnu.addSeparator()
                else:
                    n, t, sc, ck = i
                    setattr(self, 'act_%s' % n, QAction(t, self))
                    act = getattr(self, 'act_%s' % n)
                    act.setCheckable(ck)
                    self.connect(act, SIGNAL('triggered()'), getattr(self, n))
                    mnu.addAction(act)
  
        self.printer = printer(self)
        p = self.printer
        self.connect(p, SIGNAL('status'), self.status)
        self.connect(p, SIGNAL('stopped'), partial(self.status, u'終止列印作業！'))
        self.dtl_only = False

    def init_w(self, w_l, slt):
        for k, i in enumerate(w_l):
            setattr(self, 'lbl_%s' % k, QLabel(self))
            lbl = getattr(self, 'lbl_%s' % k)
            lbl.setText(u'  ')
            self.tb.addWidget(lbl)
            if i:
                self.tb.addWidget(getattr(self, i))
            else:
                self.tb.addSeparator()
        
        self.selector = slt
        s = self.selector
        self.connect(s, SIGNAL('done'), self.select_inst)
        self.connect(s, SIGNAL('status'), self.status)
        self.connect(s, SIGNAL('stopped'), self.stopped)

        n = self.class_name() 
        self.restoreGeometry(sts.value('%s/geometry' % n).toByteArray())     
        self.restoreState(sts.value('%s/state' % n).toByteArray())
        
    def p_sl(self):
        ls = self.selected()
        if ls:
            dlg = dlg_print(self, ls=[(i, cr.execute('select distinct patient.name from tk join patient on patient.id = tk.patient_id where tk.inst_id = ?', (int(i),)).fetchone()[0]) for i in ls], dtl_only=self.dtl_only)
            if dlg.exec_():
                self.printer.go(l_print=dlg.l_print)
        else:
            show_error(self, title=u'無勾選', msg=u'請勾選案件！')

    def cls(self):
        self.trv.setModel(QStandardItemModel())

    def select_inst(self, m):
        m = set_icons(m)
        self.trv.setModel(m)
        self.trv.expandAll()
        self.pbn.setText(u'顯示案件(&D)')

    def stopped(self):
        self.pbn.setText(u'顯示案件(&S)') 

    def status(self, s):
        self.stb.showMessage(s, 5000)

    def click(self, ix):
        it = self.trv.model().itemFromIndex(ix)
        
        if it.isCheckable() and it.hasChildren() :
            for i in range(it.rowCount()):
                for j in range(it.columnCount()):
                    itc = it.child(i, j)
                    if itc.isCheckable():
                        itc.setCheckState(it.checkState())

    def selected(self):
        try:
            cc = []
            m = self.trv.model()
            for i in range(m.rowCount()):
                for j in range(m.columnCount()):
                    it = m.item(i, j)
                    if it.isCheckable() and it.hasChildren() :
                        for ii in range(it.rowCount()):
                            for jj in range(it.columnCount()):
                                itc = it.child(ii, jj)
                                if itc.checkState():
                                    # data: inst_24200, tk_23222, insttype_03
                                    cc.append(unicode(itc.data().toString()).split('_')[-1])        
        except:
            cc = []
        finally:
            return cc

    def probe(self, ix):
        tp, id = unicode(self.trv.model().itemFromIndex(ix).data().toString()).split('_') 
        if tp == 'tk':
            w = win_probe(par=self, tk_id=id)
            w.setWindowModality(Qt.ApplicationModal)
            w.showMaximized()

    def display(self):
        pass

    def contextMenuEvent(self, e):
        self.mnu_.exec_(QCursor.pos()) 
    
    def closeEvent(self, e):
        try:
            for i in [self.selector, self.printer]:
                i.end()
        except:
            pass

        n = self.class_name()
        sts.setValue('%s/geometry' % n, QVariant(self.saveGeometry()))
        sts.setValue('%s/state' % n, QVariant(self.saveState()))

class win_patient(win_inst_base):

    def __init__(self, par=None, pid=''):
        win_inst_base.__init__(self, par)
        self.setWindowIcon(QIcon(':/res/img/patient.png'))
        self.setWindowTitle(u'患者')
        self.lbl_led = QLabel(self)
        self.lbl_led.setText(u'身份證號')

        self.led = QLineEdit(self)
        
        self.init_w(['lbl_led', 'led', '', 'pbn', ''], patient_inst_selector(self))
         
        self.connect(self.led, SIGNAL('returnPressed()'), self.display)
    
        if pid:
            self.led.setText(pid)
            self.display()
        self.led.setFocus()      
    
    def display(self):
        l = self.led
        l.setText(l.text().toUpper())
        if not validate_pid(l):
            return

        u = self.selector
        if u.isRunning():
            u.end()
        else:
            u.go(pid=unicode(l.text()))
            self.cls()
            self.pbn.setText(u'停止整理(&D)')

class win_inst(win_inst_base):

    def __init__(self, par=None):
        win_inst_base.__init__(self, par)
        
        self.lbl_ded = QLabel(self)
        self.lbl_ded.setText(u'費用年月')

        self.ded = QDateEdit(self)
        self.ded.setDisplayFormat('MM/yyyy')
        self.ded.setDate(QDate.currentDate())

        self.lbl_cbo = QLabel(self)
        self.lbl_cbo.setText(u'檢視模式')       
        
        self.cbo = QComboBox(self)
        
        self.init_w(['lbl_ded', 'ded', '', 'lbl_cbo', 'cbo', '', 'pbn', ''], 
                     inst_selector(self))
        
        for i, j in self.selector.views:
            self.cbo.addItem(i) 
        self.cbo.setCurrentIndex(0)
        self.dtl_only = True

    def display(self):
        u = self.selector
        if u.isRunning():
            u.end()
        else:
            u.go(ym=self.ym(), sql=self.sql())
            self.cls()
            self.pbn.setText(u'停止整理(&D)')

    def ym(self):
        return dt_tw(self.ded.date().toPyDate(), date_only=True)[:5]
    
    def sql(self):
        return self.selector.views[self.cbo.currentIndex()][1]

class win_app(win, Ui_win_app):

    def __init__(self, par=None):
        win.__init__(self, par)
        self.setupUi(self)

        self.lbl_ded = QLabel(self)
        self.lbl_ded.setText(u'費用年月') 

        self.ded = QDateEdit(self)
        self.ded.setDisplayFormat('MM/yyyy')
        cd = QDate.currentDate()
        if cd.day() <= 15:
            cd = cd.addMonths(-1)
        self.ded.setDate(cd)
        
        self.pbn_app = QPushButton(self)
        self.pbn_app.setText(u'申報(&A)')    
        self.pbn_qry = QPushButton(self)
        self.pbn_qry.setText(u'查詢(&Q)')    
        
        for k, i in enumerate(['lbl_ded', 'ded', '', 'pbn_app', '', 'pbn_qry', '']):
            setattr(self, 'lbl_%s' % k, QLabel(self))
            lbl = getattr(self, 'lbl_%s' % k)
            lbl.setText('  ')

            self.tb.addWidget(lbl)
            if i:
                self.tb.addWidget(getattr(self, i))
            else:
                self.tb.addSeparator()        
    
        self.applier = a = applier(self)
        self.connect(a, SIGNAL('status'), self.status)
        self.connect(a, SIGNAL('printf'), self.printf)

        self.connect(self.pbn_app, SIGNAL('clicked()'), partial(self.app, 'apply')) 
        self.connect(self.pbn_qry, SIGNAL('clicked()'), partial(self.app, 'query')) 

        n = self.class_name()
        self.restoreGeometry(sts.value('%s/geometry' % n).toByteArray())    
        self.restoreState(sts.value('%s/state' % n).toByteArray())
    
    def app(self, typ):
        a = self.applier
        if a.isRunning():
            return

        ym = self.ym()
        yr = ym[:3]
        mon = ym[3:]
            
        # XXX
        #r = cr.execute('select serial from app where ym = ?', (ym,)).fetchone()
        #if typ == 'apply':
        #    if r is not None:
        #        if qna(self, u'是否重新申報', u'%s 年 %s 月已申報過，是否重新申報？\n\n選擇 [Yes] 重新申報，[No] 取消！' % (yr, mon)) != QMessageBox.Yes:
        #            return

        #else:
        #    if r is None:
        #        info(self, u'未申報', u'查詢月份 %s 年 %s 月未申報過，請先申報！' % (yr, mon))
        #        return

        self.status(u'\n開始 %s 年 %s 月%s作業，請稍候...' % (yr, mon, zh(typ)))
        a.go(ym=ym, typ=typ)

    def printf(self, f):
        if qna(self, u'申報總表下載成功', u'申報總表下載成功，準備進行列印；請放入兩張 A4 紙。\n\n選擇 [Yes] 開始列印，[No] 取消！') == QMessageBox.Yes:
            for i in range(2):
                pdf_print(f)
        self.status(u'申報結果查詢完畢！')

    def status(self, s):
        self.log.appendPlainText(s)
    
    def ym(self):
        return dt_tw(self.ded.date().toPyDate(), date_only=True)[:5]

    def closeEvent(self, e):
        for i in [self.applier,]:
            i.end()
        
        n = self.class_name()
        sts.setValue('%s/geometry' % n, QVariant(self.saveGeometry()))
        sts.setValue('%s/state' % n, QVariant(self.saveState()))

class win_stat(win, Ui_win_stat):

    def __init__(self, par=None):
        win.__init__(self, par)
        self.setupUi(self)

        self.lbl_ded = QLabel(self)
        self.lbl_ded.setText(u'費用年月') 

        self.ded = QDateEdit(self)
        self.ded.setDisplayFormat('MM/yyyy')
        self.ded.setDate(QDate.currentDate())

        self.pbn = QPushButton(self)
        self.pbn.setText(u'製作圖表(&D)')    

        for k, i in enumerate(['lbl_ded', 'ded', '', 'pbn', '']):
            setattr(self, 'lbl_%s' % k, QLabel(self))
            lbl = getattr(self, 'lbl_%s' % k)
            lbl.setText('  ')

            self.tb.addWidget(lbl)
            if i:
                self.tb.addWidget(getattr(self, i))
            else:
                self.tb.addSeparator()
        
        self.stats = stats(self)
        s = self.stats
        self.connect(s, SIGNAL('done'), self.plot)
        self.connect(s, SIGNAL('status'), self.status)
                
        self.connect(self.pbn, SIGNAL('clicked()'), self.display) 
        self.restoreGeometry(sts.value('%s/geometry' % self.class_name()).toByteArray())
    
    def display(self):
        self.stats.go(ym=self.ym())
    
    def status(self, s):
        self.stb.showMessage(s, 5000)

    def ym(self):
        return dt_tw(self.ded.date().toPyDate(), date_only=True)[:5]

    def plot(self, data):
        dd, series = data
        htm = '''
<html>
<head>
  <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
  <!--[if lt IE 9]><script language='javascript' type='text/javascript' src='excanvas.min.js'></script><![endif]-->
  <link rel='stylesheet' type='text/css' href='jquery.jqplot.min.css' />
  <script type='text/javascript' src='jquery.min.js'></script>
  <script type='text/javascript' src='jquery.jqplot.min.js'></script>
  <script type='text/javascript' src='plugins/jqplot.barRenderer.min.js'></script>
  <script type='text/javascript' src='plugins/jqplot.categoryAxisRenderer.min.js'></script>
  <script type='text/javascript' src='plugins/jqplot.pointLabels.min.js'></script>
  <script type='text/javascript' src='plugins/jqplot.pieRenderer.min.js'></script>
  <style type="text/css">
    html, body {
        height: 99%;
    }

    #outer {
        height: 100%; 
        width: 100%;
        overflow: visible;
        position: relative;
    }

    #outer[id] {
        display: table; 
        position: static;
    }

    #middle[id] {
        display: table-cell; 
        vertical-align: middle; 
        width: 100%;
    }

    #inner {
        width: 100%; 
        margin-left: auto; 
        margin-right: auto; 
    }
    
    #stat .jqplot-point-label {
      border: 1px solid #aaaaaa;
      padding: 1px 1px;
      background-color: #eeccdd;
      font-size: 0.7em;
    }

    #stat {
      height: 500px;
    }
  </style>
  <script type='text/javascript'>
      $(document).ready(function(){
        var dd = ''' + dd + ''';

        plot1 = $.jqplot('stat', dd['l'], {
          title: dd['title'],
          seriesDefaults:{
            renderer: $.jqplot.BarRenderer,
            rendererOptions: {fillToZero: true},
            pointLabels: {show: true}
          },
          series: [''' + series + '''],
          legend: {
            show: true
          },
          axes: {
            xaxis: {renderer: $.jqplot.CategoryAxisRenderer}
          }
        });

      });
  </script>
</head>
<body> 
  <div id='outer'><div id='middle'><div id='inner'>
    <div id='stat'></div>
    <div id='pie'></div>
  </div></div></div>
</body>
</html>''' 
        self.gr.setHtml(htm, QUrl.fromLocalFile(cat(os.getcwd(),'bin','dist','.')))

        self.pbn.setText(u'開始圖表製作(&D)')
        #'Cumulative Points of %s: %s %s' % (ym, cum, inst_s)

    def closeEvent(self, e):
        for i in [self.stats,]:
            i.end() 
        sts.setValue('%s/geometry' % self.class_name(), QVariant(self.saveGeometry()))

# ==============================================================================
#  all dialogs   
# ==============================================================================

class dlg(QDialog):

    def __init__(self, *a):
        super(dlg, self).__init__(*a)

    def class_name(self):
        return self.__class__.__name__

class dlg_tk_ini(dlg, Ui_dlg_tk_ini):

    def __init__(self, par=None):
        dlg.__init__(self, par)
        self.setupUi(self)

class dlg_ent_inst(dlg, Ui_dlg_ent_inst):

    def __init__(self, par=None, pid='', name='', birthday='', insttype_code='', inst_id=0, amend_code='1'):
        dlg.__init__(self, par)
        self.setupUi(self)
         
        attrs_from_dict(locals())
        
        self.connect(self.tbv.verticalHeader(), SIGNAL('sectionClicked(int)'), 
                     self.ent_inst)
        QTimer.singleShot(0, self.init)
    
    def init(self): 
        self.lbl_gender.setPixmap(QPixmap(':/res/img/user-%s.png' % 
                                                            gender(self.pid)))
        self.lbl_details.setText('\n'.join((self.name, 
                                            self.pid, 
                                            dt_s(self.birthday, True),))) 
        
        dt = datetime.date.today() - datetime.timedelta(days=45)
        month = str(dt.year - 1911).zfill(3) + str(dt.month).zfill(2)
        
        sql = '''select distinct inst.id from inst 
                 join tk on inst.id = tk.inst_id 
                 join patient on tk.patient_id = patient.id 
                 join insttype on inst.insttype_id = insttype.id 
                 where patient.pid = ? 
                 and tk.dt > ? 
                 and insttype.code = ?''' if self.insttype_code == 'B6' else '''
                 select distinct inst.id from inst 
                 join tk on inst.id = tk.inst_id 
                 join patient on tk.patient_id = patient.id 
                 where patient.pid = ? 
                 and tk.dt > ?'''
        
        if self.amend_code == '2': # 補卡-->尋找欠卡
            sql += ' and trim(tk.serial) = "" and tk.sign = ""'
        sql += ' order by tk.dt desc'
        arg = (self.pid, month, self.insttype_code) if self.insttype_code == 'B6' else (self.pid, month)

        r = cr.execute(sql, arg).fetchall()        
        if not r:
            QMessageBox.warning(self, u'無符合案件', u'無符合案件可供選擇！')
            self.close()

        all_ = []
        for i in r:
            tks = '\n'.join((dt_s(j[0]) for j in cr.execute('select dt from tk where inst_id = ?', (i[0],)).fetchall()))
            diags = '\n'.join((j[0] for j in cr.execute('select distinct diag.name from tk_diag join diag on tk_diag.diag_id = diag.id where tk_diag.tk_id in (select id from tk where inst_id = ?)', (i[0],)).fetchall()))            
            all_.append((str(i[0]), tks if tks.strip() else u'（無掛號紀錄）', diags if diags.strip() else u'（尚未看診）'))
          
        self.tbv.setModel(model_dsp(ls=all_, 
                                  meta={'caption': u'選擇案件', 
                                        'header': (u'', u'掛號時間', u'診斷')}))   
        try:
            n = self.class_name()
            self.restoreGeometry(sts.value('%s/geometry' % n).toByteArray())
            for i in range(self.tbv.model().columnCount()):
                v, ok = sts.value('%s/tbv/%s/width' % (n, i)).toInt()
                if ok:
                    self.tbv.setColumnWidth(i, v)
        except:
            pass 
        
        self.tbv.setColumnHidden(0, True)
        self.tbv.show()     

    def ent_inst(self, i):
        self.inst_id = self.tbv.model().ls[i][0]
        self.emit(SIGNAL('done'))
        self.accept()
        self.close()
    
    def closeEvent(self, e):       
        try:
            tbv = self.tbv
            n = self.class_name()
            sts.setValue('%s/geometry' % n, QVariant(self.saveGeometry()))
            for i in range(tbv.model().columnCount()):
                sts.setValue('%s/tbv/%s/width' % (n, i), 
                             QVariant(tbv.columnWidth(i)))
        except:
            pass

class dlg_login(dlg, Ui_dlg_login):

    def __init__(self, par=None):
        dlg.__init__(self, par)
        self.setupUi(self)

class dlg_pwd(dlg, Ui_dlg_pwd):

    def __init__(self, par=None):
        dlg.__init__(self, par)
        self.setupUi(self)

class dlg_fav(dlg, Ui_dlg_fav):

    def __init__(self, par=None):
        dlg.__init__(self, par)
        self.setupUi(self)
        
    def accept(self):
        if not validate_code_name(self.led_code, self.led_name):
            return        
        QDialog.accept(self)

class dlg_tk_abn(dlg, Ui_dlg_tk_abn):

    def __init__(self, par=None):
        dlg.__init__(self, par)
        self.setupUi(self)
        
        self.ded_birth.setDisplayFormat('M/d/yyyy')
        self.dted_tk.setDisplayFormat('M/d/yyyy h:mm:ss')
        
        d = dic_all_inv['state']
        for k in d.keys():
            self.cbo_state.addItem(d[k][1], QVariant(k)) 
        self.cbo_state.setCurrentIndex(2) 
        
        self.dted_tk.setDateTime(QDateTime.currentDateTime())
        self.led_name.setText(u'＊＊＊')
        
        d = dic_all_inv['anormaly']
        for k in d.keys():
            self.cbo_abn.addItem(d[k][1], QVariant(k))
        self.cbo_abn.setCurrentIndex(4)

        self.connect(self.led_pid, SIGNAL('textEdited(QString)'), self.lookup)
        self.led_pid.setFocus()
        
    def lookup(self):
        pid = unicode(self.led_pid.text().toUpper())
        if not valid_pid(pid):
            return
        self.led_pid.setText(pid)
        r = cr.execute('select name, birthday from patient where pid = ?', 
                       (pid,)).fetchone()
        if r:    
            self.led_name.setText(r[0])
            b = r[1]
            self.ded_birth.setDate(QDate.fromString(str(int(b[:3]) + 1911) + b[3:], 'yyyyMMdd'))

    def accept(self):
        if not validate_pid(self.led_pid):
            return        
        QDialog.accept(self)

class dlg_fee(dlg, Ui_dlg_fee):

    def __init__(self, par=None, tk_id=0):
        dlg.__init__(self, par)
        self.setupUi(self)
        
        r = cr.execute('select fee_id from tk_fee where tk_id = ?', 
                       (tk_id,)).fetchall() 
        if r:
            for i in r:
                fee_id = i[0]
                if fee_id == 4: # loan
                    self.chk_loan.setChecked(True)
                elif fee_id == 3:
                    self.rbn_ini.setChecked(True)
                elif fee_id == 2:
                    self.rbn_gen.setChecked(True)
                else: # 1 or others
                    self.rbn_na.setChecked(True)
        else:
            self.rbn_na.setChecked(True)

class dlg_print(dlg, Ui_dlg_print):

    def __init__(self, par=None, ls=None, dtl_only=False):
        dlg.__init__(self, par)
        self.setupUi(self)
       
        typs = ['chk', 'prscr', 'rcpt', 'rcptn', 'dtl']
        
        tbv = self.tbv
        #tbv.setAlternatingRowColors(True)
        #tbv.setStyleSheet("alternate-background-color: yellow;background-color: red;");
        # ls: [(u'20000', u'杜進旺'), (u'20001', u'杜尚穎'),]
        m = QStandardItemModel(len(ls), len(typs))      
        for i in range(m.columnCount()):
            h = QStandardItem(zh(typs[i]))            
            m.setHorizontalHeaderItem(i, h)

        # create c_s and set the default last as Qt.Checked  
        c_s = [Qt.Unchecked if dtl_only else Qt.Checked] * (len(typs) - 1) 
        c_s.append(Qt.Checked) 
        self.chk_state = c_s 
        for i in range(m.rowCount()):
            v = QStandardItem('  '.join([unicode(ii) for ii in ls[i]]))
            m.setVerticalHeaderItem(i, v)
            for j in range(m.columnCount()):
                si = QStandardItem()
                si.setData(QVariant(u'%s_%s' % (typs[j], ls[i][0])))
                si.setCheckable(True)
                si.setCheckState(self.chk_state[j])
                m.setItem(i, j, si)
        
        tbv.setFocusPolicy(Qt.NoFocus)
        tbv.setSelectionMode(QAbstractItemView.NoSelection)
        tbv.setModel(m)
        self.connect(tbv.horizontalHeader(), SIGNAL('sectionClicked(int)'), 
                     self.click_hd)
        
        n = self.class_name()
        self.restoreGeometry(sts.value('%s/geometry' % n).toByteArray()) 
        for i in range(tbv.model().columnCount()):
            v, ok = sts.value('%s/tbv/%s/width' % (n, i)).toInt()
            if ok:
                tbv.setColumnWidth(i, v)        
        tbv.show()
        self.l_print = {}

    def click_hd(self, i):
        m = self.tbv.model()
        self.chk_state[i] = Qt.Unchecked if self.chk_state[i] == Qt.Checked else Qt.Checked
        for j in range(m.rowCount()):
            si = m.item(j, i)
            si.setCheckState(self.chk_state[i])
    
    def accept(self): 
        m = self.tbv.model()
        for i in range(m.rowCount()):
            for j in range(m.columnCount()):
                si = m.item(i, j)
                if si.checkState() == Qt.Checked:
                    # si.data(): chk_20003
                    tp, id = unicode(si.data().toString()).split('_')
                    try:
                        self.l_print[id]
                    except KeyError:
                        self.l_print[id] = []
                    self.l_print[id].append(tp)
        
        # self.l_print:
        # {u'20000': [u'chk', u'prscr', u'dtl'], u'20000': [u'chk', u'dtl']}
        
        n = self.class_name()
        for i in range(m.columnCount()):
            sts.setValue('%s/tbv/%s/width' % (n, i), 
                         QVariant(self.tbv.columnWidth(i)))
        sts.setValue('%s/geometry' % n, QVariant(self.saveGeometry()))
        QDialog.accept(self)

# ==============================================================================
#  main    
# ==============================================================================

n_com_trial = 10
n_sam_trial = 3
com_port = 0

start_time0 = time.time()
model_orig = model_collect(now())
print('load grand model: %f seconds.' % (time.time() - start_time0,))

is_com_ok = False
if is_dll_ok:
    show_msg(u'開啟 com 埠 ...')
    start_time0 = time.time()
    for i in range(n_com_trial):
        if cs.csOpenCom(i) == 0:
            is_com_ok = True
            com_port = i
            break
    print('open com: %f seconds.' % (time.time() - start_time0,))

    if not is_com_ok:
        if qna(title=u'無法使用 IC 卡作業', msg=u'因為以下錯誤：\n（讀卡機與電腦連結問題）\nmycis 無法使用 IC 卡作業。是否繼續載入？\n\n選擇 [Yes] 繼續 mycis，[No] 離開！') != QMessageBox.Yes:
           sys.exit()
else:
    if qna(title=u'無法上傳、申報及使用 IC 卡', msg=u'因為以下錯誤：\n（dll 未安裝妥當）\nmycis 無法上傳、申報及使用 IC 卡。是否繼續載入？\n\n選擇 [Yes] 繼續 mycis，[No] 離開！') != QMessageBox.Yes:
           sys.exit()

#w = win_main()
w = win_probe(tk_id=120)
w.showMaximized()
spl.finish(w)

app.processEvents()
app.restoreOverrideCursor()
app.exec_()

# -*- coding: utf-8 -*-

import os, sys
cat = os.path.join
    
import reportlab.rl_config
reportlab.rl_config.warnOnMissingFontGlyphs = 0
from reportlab.rl_config import TTFSearchPath
TTFSearchPath.append(cat(os.path.dirname(__file__), 'res', 'fonts'))
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('wtm', 'WT021.TTF'))
pdfmetrics.registerFont(TTFont('msjh', 'msjh.ttf'))
#pdfmetrics.registerFont(TTFont('ming', 'mingliu.ttc'))
A4_w, A4_h = 210, 297
from reportlab.platypus import Paragraph, Frame, KeepInFrame
from reportlab.lib.styles import getSampleStyleSheet

def print_test_pdf():   
    f = cat(os.path.dirname(__file__), 'test.pdf')
    cv = canvas.Canvas(f)

    def line(l, cv):
        cv.line(*tuple([l[0]*mm, (A4_h - l[1])*mm, l[2]*mm, (A4_h - l[3])*mm]))

    def text(s, cv, size=9, font='wtm', centered=False):
        cv.setFont(font, size)
        f = cv.drawCentredString if centered else cv.drawString        
        f(*(s[0]*mm, (A4_h - s[1])*mm, unicode(s[2])))

    def rect(s, cv, fill=0):
        cv.rect(s[0]*mm, (A4_h - s[1])*mm, 3*mm, 3*mm, fill=fill)

    def certificate_form(cv):
        cv.setLineWidth(1*mm)
        cv.rect(8*mm, 8*mm, 194*mm, 281*mm) 
        line((8, 40, 202, 40), cv)
        cv.setLineWidth(0.2*mm)

        lines = [
            (8,    8,   202,    8),    
            (8,  289,   202,  289),
            (8,    8,     8,  289), 
            (202,  8,   202,  289),

            (8,   40,   202,   40),    
            (8,   56,   202,   56), 
            (8,   72,   202,   72),
            (8,   88,   202,   88),
            (8,  116,   202,  116),
            (8,  167,   202,  167),
            (8,  237,   202,  237),
            
            (19,   40,   19,  237), 
            (105,  40,  105,   72),
            (116,  40,  116,   56),
            (123,  56,  123,   72),
            (105,  88,  105,  116),
            (116,  88,  116,  116),
        ]
        for s in lines:
            line(s, cv)

        s = [
            (10,  47,    u'姓'),   (107, 47, u'性'),
            (10,  53,    u'名'),   (107, 53, u'別'),
            (10,  63,    u'生'),   (107, 63, u'身'),
            (10,  69,    u'日'),   (107, 69, u'份'),
            (10,  79,    u'住'),   (114, 63, u'證'),
            (10,  85,    u'址'),   (114, 69, u'號'),
            (10,  95,    u'應'),   (107, 95, u'應'),
            (10,  101,   u'診'),  (107, 101, u'診'),
            (10,  107,   u'日'),  (107, 107, u'科'),
            (10,  113,   u'期'),  (107, 113, u'別'),
            (10,  124,   u'病'),
            (10,  163,   u'名'),
            (10,  174,   u'醫'),
            (10,  194,   u'師'),
            (10,  214,   u'囑'), 
            (10,  234,   u'言'),
        ]
        for ss in s:
            text(ss, cv, size=20)
            
        s = [
            (10,  242,   u'以上病人經本院醫師診斷屬實特予證明'),
            (116, 242,   u'本證明書需加蓋本院印信否則無效'),
            (10,  248,   u'院    長  魏  筱  筠'), 
            (10,  254,   u'診治醫師  魏筱筠醫師'),  
            (10,  260,   u'醫師證書字號'),
            (10,  274,   u'惠生婦產科診所  南縣衛醫字第           號'),
            (10,  280,   u'台南市新營區民權路    號'),
            (10,  286,   u'中華民國       年       月       日'),
        ]
        for ss in s:
            text(ss, cv, size=16)

        s_n = [
            (49,   260,   u'037964'),
            (90,   274,   u'3541012321'),
            (61,   280,   u'30-1'),
            (39,   286,   u'105'),
            (65,   286,   u'06'),
            (90,   286,   u'09'),
        ]
        for ss in s_n:
            text(ss, cv, size=14, font='msjh')

        text((105, 20, u'惠 生 婦 產 科 診 所'), cv, size=36, centered=True)
        text((105, 35, u'診   斷   證   明   書'), cv, size=36, centered=True)
        
    def certificate(cv):
        s = [
            (21,   50,   u'魏筱筠'),       # 姓名
            (123,  50,   u'女'),           # 性別
            (21,   66,   u'101-06-20'),    # 生日 
            (125,  66,   u'R220154944'),   # 身份證號
            (21,   82,   u'台南市新營區民權路 30-1 號'), # 住址 
            (21,   104,  u'105-05-14'),    # 應診日期 
            (118,  104,  u'婦產科'),       # 應診科別
        ]
        for ss in s:
            text(ss, cv, size=20, font='msjh')
        
        #rect((42, 80), cv)
        #rect((52, 80), cv, fill=1)
    
    certificate_form(cv)
    certificate(cv)

    style_sheet = getSampleStyleSheet()
    style = style_sheet['Normal']
    style.fontName = 'msjh'
    style.fontSize = 16 
    style.leading = 18 
    frame1 = Frame(19*mm, 130*mm, 183*mm, 51*mm, showBoundary=0)
    s1 = u'''為提倡有科學根基的服務精神，中央氣象局依照職掌業務的範疇舉辦「天地人學思論壇」，邀請國內外具有國際聲望與影響力的學者分享其學術及人生的寶貴經驗，期能達到「天地人」和「學思論」分別呈現氣象局職掌業務與活動內容，藉由聆聽、討論、學習過程，擴大思考層面，深化科學涵養。活動相關訊息請參閱海報，竭誠歡迎大家報名參加。另「104年天地人學思論壇」產出的「氣象老先覺」專題電子版連結網址請「點此進入」，歡迎大家上網點閱，謝謝。'''  
    soap1 = [Paragraph(s1, style)]
    soap_in_frame1 = KeepInFrame(183*mm, 51*mm, soap1)
    frame1.addFromList([soap_in_frame1,], cv)

    frame2 = Frame(19*mm, 60*mm, 183*mm, 70*mm, showBoundary=0)
    s2 = u'''其實，無論是行動設備還是桌上型電腦，一直以來都有整合的傾向。一方面，是因為行動晶片更強大了。另一方面，則是使用者對計算能力的需求正在下降，而執行的任務卻越來越行動化。或許，大多數人可能會覺得自己的辦公室陳設並沒有太大的變化，因為許多的工作站依然擺在那裡，旁邊還放著印表機。但事實並非如此，因為越來越多的工作在辦公室之外就被完成了，而完成它們的主要工具是來自手機。雖說許多專業任務，如PhotoshopLightroom等應用依然需要macOS，但iPadPro的出現已經宣示了蘋果的新企圖心。在 Windows平台上X8意義重大，因為它與龐大的遊戲市場相銜接，但對於幾乎無遊戲可玩的macOS來說，X86的這點優勢顯得毫無意義。過去幾年中，蘋果將主要的研發精力放在iOS上。從許多方面來看，macOS都是一款老操作系統。不過，現在macOS最吸引人的地方，則在於它與iOS和iPhone的關係。未來，英特爾的領袖地位還會延續，尤其是在高階市場。但是，由於高階市場較為小眾，其控制能力將會有所降低。尤其，現在人們製作影像時多數用的是Snapchat的Live Stories，而非專業的AdobePremiere Pro時，就知道高階市場產品的影響力已經開始逐漸式微。其實，無論是行動設備還是桌上型電腦，一直以來都有整合的傾向。一方面，是因為行動晶片更強大了。另一方面，則是使用者對計算能力的需求正在下降，而執行的任務卻越來越行動化。或許，大多數人可能會覺得自己的辦公室陳設並沒有太大的變化，因為許多的工作站依然擺在那裡，旁邊還放著印表機。但事實並非如此，因為越來越多的工作在辦公室之外就被完成了，而完成它們的主要工具是來自手機。雖說許多專業任務，但的出現已經宣示了蘋果的新企圖心。在平台上意義重大，因為它與龐大的遊戲市場相銜接，但對於幾乎無遊戲可玩的來說，的這點優勢顯得毫無意義。過去幾年中，蘋果將主要的研發精力放在上。從許多方面來看，都是一款老操作系統。不過，現在最吸引人的地方，則在於它與和的關係。未來，英特爾的領袖地位還會延續，尤其是在高階市場。但是，由於高階市場較為小眾，其控制能力將會有所降低。尤其，現在人們製作影像時多數用的是的，而非專業的時，就知道高階市場產品的影響力已經開始逐漸式微。'''  
    soap2 = [Paragraph(s2, style)]
    soap_in_frame2 = KeepInFrame(183*mm, 70*mm, soap2)
    frame2.addFromList([soap_in_frame2,], cv)

    cv.save()

print_test_pdf()

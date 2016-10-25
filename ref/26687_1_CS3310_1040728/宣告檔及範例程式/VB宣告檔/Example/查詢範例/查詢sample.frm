VERSION 5.00
Begin VB.Form 查詢 
   Caption         =   "查詢sample畫面"
   ClientHeight    =   3915
   ClientLeft      =   3345
   ClientTop       =   945
   ClientWidth     =   10890
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   ScaleHeight     =   3915
   ScaleWidth      =   10890
   Begin VB.Frame Frame3 
      BackColor       =   &H8000000B&
      Caption         =   "基本資料段"
      Height          =   2175
      Left            =   360
      TabIndex        =   0
      Top             =   120
      Width           =   10095
      Begin VB.Label Label17 
         Height          =   255
         Left            =   1800
         TabIndex        =   14
         Top             =   1755
         Width           =   1575
      End
      Begin VB.Label Label16 
         Height          =   375
         Left            =   1800
         TabIndex        =   13
         Top             =   800
         Width           =   1335
      End
      Begin VB.Label Label15 
         Height          =   375
         Left            =   6120
         TabIndex        =   12
         Top             =   1280
         Width           =   1215
      End
      Begin VB.Label Label8 
         BackStyle       =   0  '透明
         Caption         =   "卡片號碼"
         Height          =   255
         Left            =   240
         TabIndex        =   11
         Top             =   360
         Width           =   1455
      End
      Begin VB.Label Label10 
         Caption         =   "姓名"
         Height          =   375
         Left            =   240
         TabIndex        =   10
         Top             =   800
         Width           =   855
      End
      Begin VB.Label Label12 
         Caption         =   "性別"
         Height          =   255
         Left            =   240
         TabIndex        =   9
         Top             =   1755
         Width           =   1095
      End
      Begin VB.Label Label21 
         BackColor       =   &H8000000A&
         Height          =   375
         Left            =   6120
         TabIndex        =   8
         Top             =   360
         Width           =   1455
      End
      Begin VB.Label Label20 
         Height          =   375
         Left            =   6120
         TabIndex        =   7
         Top             =   795
         Width           =   1215
      End
      Begin VB.Label Label19 
         BackStyle       =   0  '透明
         Height          =   255
         Left            =   1800
         TabIndex        =   6
         Top             =   360
         Width           =   1335
      End
      Begin VB.Label Label18 
         Height          =   375
         Left            =   1800
         TabIndex        =   5
         Top             =   1280
         Width           =   1095
      End
      Begin VB.Label Label14 
         Caption         =   "卡片註銷註記"
         Height          =   375
         Left            =   4440
         TabIndex        =   4
         Top             =   360
         Width           =   1335
      End
      Begin VB.Label Label9 
         Caption         =   "身分證字號"
         Height          =   255
         Left            =   240
         TabIndex        =   3
         Top             =   1280
         Width           =   1335
      End
      Begin VB.Label Label11 
         Caption         =   "出生日期"
         Height          =   375
         Left            =   4440
         TabIndex        =   2
         Top             =   1280
         Width           =   1095
      End
      Begin VB.Label Label13 
         Caption         =   "發卡日期"
         Height          =   255
         Left            =   4440
         TabIndex        =   1
         Top             =   800
         Width           =   1215
      End
   End
   Begin VB.Label Label33 
      Caption         =   "新生兒胎胞註記"
      Height          =   255
      Left            =   7320
      TabIndex        =   26
      Top             =   3240
      Width           =   1455
   End
   Begin VB.Label Label32 
      Caption         =   " "
      Height          =   255
      Left            =   8940
      TabIndex        =   25
      Top             =   3240
      Width           =   1455
   End
   Begin VB.Label Label31 
      Caption         =   "新生兒出生日期"
      Height          =   255
      Left            =   7320
      TabIndex        =   24
      Top             =   2520
      Width           =   1455
   End
   Begin VB.Label Label30 
      Caption         =   " "
      Height          =   255
      Left            =   8940
      TabIndex        =   23
      Top             =   2520
      Width           =   1455
   End
   Begin VB.Label Label24 
      Caption         =   "就醫可用次數"
      Height          =   255
      Left            =   360
      TabIndex        =   22
      Top             =   3120
      Width           =   1335
   End
   Begin VB.Label Label26 
      Caption         =   " "
      Height          =   255
      Left            =   2040
      TabIndex        =   21
      Top             =   3120
      Width           =   1695
   End
   Begin VB.Label Label23 
      Height          =   255
      Left            =   5760
      TabIndex        =   20
      Top             =   3120
      Width           =   1335
   End
   Begin VB.Label Label22 
      Caption         =   "卡片有效期限"
      Height          =   255
      Left            =   4080
      TabIndex        =   19
      Top             =   3120
      Width           =   1095
   End
   Begin VB.Label Label3 
      Caption         =   " "
      Height          =   255
      Left            =   5700
      TabIndex        =   18
      Top             =   2520
      Width           =   1455
   End
   Begin VB.Label Label4 
      Caption         =   "保險人身分註記"
      Height          =   255
      Left            =   4080
      TabIndex        =   17
      Top             =   2520
      Width           =   1455
   End
   Begin VB.Label Label2 
      Caption         =   "保險人代碼"
      Height          =   255
      Left            =   360
      TabIndex        =   16
      Top             =   2520
      Width           =   1335
   End
   Begin VB.Label Label5 
      Height          =   255
      Left            =   2040
      TabIndex        =   15
      Top             =   2520
      Width           =   1695
   End
End
Attribute VB_Name = "查詢"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private Sub Form_Load()
Dim iBufferLen As Integer
Dim err As Integer
Dim pBuffer As String * 100

err = csOpenCom(0) '使用COM1
'call hisgetregisterbasic
'卡片號碼+姓名 +身分證+出生日期+性別+發卡日期+卡片註銷註記
'1-12    +13-20+33_42 +43_49   +50  +51_57   +58
'保險人代碼+身份註記+卡片有效期限
'59_60     +61      +62_68
'就醫可用次數+新生兒出生日期+新生兒胎胞註記
'69_70     +71_77       +78

iBufferLen = 78
err = hisGetRegisterBasic(pBuffer, iBufferLen)

If err = 0 Then

'基本資料段
'卡片號碼
    Label19.Caption = MidMbcs(pBuffer, 1, 12)

'姓名
    Label16.Caption = MidMbcs(pBuffer, 13, 20)

'身份證字號
    Label18.Caption = MidMbcs(pBuffer, 33, 10)

'出生日期
    Label15.Caption = MidMbcs(pBuffer, 43, 7)

'性別
    Label17.Caption = MidMbcs(pBuffer, 50, 1)
    If Label17.Caption = "M" Then
        Label17.Caption = "男"
    Else
        Label17.Caption = "女"
    End If

'發卡日期
    Label20.Caption = MidMbcs(pBuffer, 51, 7)

'卡片註銷註記
    Label21.Caption = MidMbcs(pBuffer, 58, 1)

'健保資料段
'保險人代碼
    Label5.Caption = MidMbcs(pBuffer, 59, 2)

'健保資料段
'保險對象身分註記
    Label3.Caption = MidMbcs(pBuffer, 61, 1)

'卡片有效期限
    Label23.Caption = MidMbcs(pBuffer, 62, 7)

'就醫可用次數
    Label26.Caption = MidMbcs(pBuffer, 69, 2)

'新生兒出生日期
    Label30.Caption = MidMbcs(pBuffer, 71, 7)
'新生兒胎胞註記
    Label32.Caption = MidMbcs(pBuffer, 78, 1)

Else
    MsgBox (err)
End If

End Sub

Function MidMbcs(ByVal str As String, start, length)
   MidMbcs = StrConv(MidB(StrConv(str, vbFromUnicode), start, length), vbUnicode)
End Function

Private Sub Form_Unload(Cancel As Integer)
   Dim err As Integer
   
   err = csCloseCom()
End Sub

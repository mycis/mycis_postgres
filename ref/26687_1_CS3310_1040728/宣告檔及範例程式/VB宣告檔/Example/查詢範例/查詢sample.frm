VERSION 5.00
Begin VB.Form �d�� 
   Caption         =   "�d��sample�e��"
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
      Caption         =   "�򥻸�Ƭq"
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
         BackStyle       =   0  '�z��
         Caption         =   "�d�����X"
         Height          =   255
         Left            =   240
         TabIndex        =   11
         Top             =   360
         Width           =   1455
      End
      Begin VB.Label Label10 
         Caption         =   "�m�W"
         Height          =   375
         Left            =   240
         TabIndex        =   10
         Top             =   800
         Width           =   855
      End
      Begin VB.Label Label12 
         Caption         =   "�ʧO"
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
         BackStyle       =   0  '�z��
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
         Caption         =   "�d�����P���O"
         Height          =   375
         Left            =   4440
         TabIndex        =   4
         Top             =   360
         Width           =   1335
      End
      Begin VB.Label Label9 
         Caption         =   "�����Ҧr��"
         Height          =   255
         Left            =   240
         TabIndex        =   3
         Top             =   1280
         Width           =   1335
      End
      Begin VB.Label Label11 
         Caption         =   "�X�ͤ��"
         Height          =   375
         Left            =   4440
         TabIndex        =   2
         Top             =   1280
         Width           =   1095
      End
      Begin VB.Label Label13 
         Caption         =   "�o�d���"
         Height          =   255
         Left            =   4440
         TabIndex        =   1
         Top             =   800
         Width           =   1215
      End
   End
   Begin VB.Label Label33 
      Caption         =   "�s�ͨ�L�M���O"
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
      Caption         =   "�s�ͨ�X�ͤ��"
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
      Caption         =   "�N��i�Φ���"
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
      Caption         =   "�d�����Ĵ���"
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
      Caption         =   "�O�I�H�������O"
      Height          =   255
      Left            =   4080
      TabIndex        =   17
      Top             =   2520
      Width           =   1455
   End
   Begin VB.Label Label2 
      Caption         =   "�O�I�H�N�X"
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
Attribute VB_Name = "�d��"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private Sub Form_Load()
Dim iBufferLen As Integer
Dim err As Integer
Dim pBuffer As String * 100

err = csOpenCom(0) '�ϥ�COM1
'call hisgetregisterbasic
'�d�����X+�m�W +������+�X�ͤ��+�ʧO+�o�d���+�d�����P���O
'1-12    +13-20+33_42 +43_49   +50  +51_57   +58
'�O�I�H�N�X+�������O+�d�����Ĵ���
'59_60     +61      +62_68
'�N��i�Φ���+�s�ͨ�X�ͤ��+�s�ͨ�L�M���O
'69_70     +71_77       +78

iBufferLen = 78
err = hisGetRegisterBasic(pBuffer, iBufferLen)

If err = 0 Then

'�򥻸�Ƭq
'�d�����X
    Label19.Caption = MidMbcs(pBuffer, 1, 12)

'�m�W
    Label16.Caption = MidMbcs(pBuffer, 13, 20)

'�����Ҧr��
    Label18.Caption = MidMbcs(pBuffer, 33, 10)

'�X�ͤ��
    Label15.Caption = MidMbcs(pBuffer, 43, 7)

'�ʧO
    Label17.Caption = MidMbcs(pBuffer, 50, 1)
    If Label17.Caption = "M" Then
        Label17.Caption = "�k"
    Else
        Label17.Caption = "�k"
    End If

'�o�d���
    Label20.Caption = MidMbcs(pBuffer, 51, 7)

'�d�����P���O
    Label21.Caption = MidMbcs(pBuffer, 58, 1)

'���O��Ƭq
'�O�I�H�N�X
    Label5.Caption = MidMbcs(pBuffer, 59, 2)

'���O��Ƭq
'�O�I��H�������O
    Label3.Caption = MidMbcs(pBuffer, 61, 1)

'�d�����Ĵ���
    Label23.Caption = MidMbcs(pBuffer, 62, 7)

'�N��i�Φ���
    Label26.Caption = MidMbcs(pBuffer, 69, 2)

'�s�ͨ�X�ͤ��
    Label30.Caption = MidMbcs(pBuffer, 71, 7)
'�s�ͨ�L�M���O
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

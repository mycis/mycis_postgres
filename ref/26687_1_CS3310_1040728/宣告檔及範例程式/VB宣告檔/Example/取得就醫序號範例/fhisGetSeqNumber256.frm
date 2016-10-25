VERSION 5.00
Begin VB.Form fhisGetSeqNumber256 
   Caption         =   "fhisGetSeqNumber256"
   ClientHeight    =   5205
   ClientLeft      =   60
   ClientTop       =   345
   ClientWidth     =   6255
   LinkTopic       =   "Form1"
   ScaleHeight     =   5205
   ScaleWidth      =   6255
   StartUpPosition =   2  '螢幕中央
   Begin VB.TextBox cTreatAfterCheck 
      BeginProperty Font 
         Name            =   "Times New Roman"
         Size            =   12
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Left            =   3480
      TabIndex        =   2
      Text            =   "1"
      Top             =   120
      Width           =   375
   End
   Begin VB.CommandButton Command2 
      Caption         =   "離開"
      BeginProperty Font 
         Name            =   "新細明體"
         Size            =   9.75
         Charset         =   136
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   495
      Left            =   5400
      TabIndex        =   16
      Top             =   120
      Width           =   735
   End
   Begin VB.TextBox cBabyTreat 
      BeginProperty Font 
         Name            =   "Times New Roman"
         Size            =   12
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Left            =   2280
      MaxLength       =   2
      TabIndex        =   1
      Top             =   120
      Width           =   615
   End
   Begin VB.TextBox cTreatItem 
      BeginProperty Font 
         Name            =   "Times New Roman"
         Size            =   12
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Left            =   720
      MaxLength       =   2
      TabIndex        =   0
      Top             =   120
      Width           =   615
   End
   Begin VB.Frame Frame1 
      Caption         =   "傳回資料"
      Height          =   4335
      Left            =   120
      TabIndex        =   6
      Top             =   840
      Width           =   6015
      Begin VB.TextBox Text1 
         BackColor       =   &H80000004&
         Height          =   1335
         Left            =   1200
         MultiLine       =   -1  'True
         TabIndex        =   20
         Top             =   1680
         Width           =   4575
      End
      Begin VB.Label IsSameDay 
         BorderStyle     =   1  '單線固定
         Height          =   375
         Left            =   1200
         TabIndex        =   19
         Top             =   3840
         Width           =   975
      End
      Begin VB.Label Label3 
         Caption         =   "同日就診"
         Height          =   375
         Left            =   240
         TabIndex        =   18
         Top             =   3840
         Width           =   615
      End
      Begin VB.Label Label14 
         Caption         =   "安全模組代碼:"
         Height          =   375
         Index           =   2
         Left            =   240
         TabIndex        =   15
         Top             =   3240
         Width           =   615
      End
      Begin VB.Label SAMID 
         BorderStyle     =   1  '單線固定
         BeginProperty Font 
            Name            =   "Times New Roman"
            Size            =   12
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   375
         Left            =   1200
         TabIndex        =   14
         Top             =   3240
         Width           =   2175
      End
      Begin VB.Label Label14 
         Caption         =   "安全簽章:"
         Height          =   375
         Index           =   1
         Left            =   240
         TabIndex        =   13
         Top             =   1680
         Width           =   615
      End
      Begin VB.Label Label14 
         Caption         =   "醫療院所代碼:"
         Height          =   375
         Index           =   0
         Left            =   240
         TabIndex        =   10
         Top             =   1200
         Width           =   615
      End
      Begin VB.Label Label13 
         Caption         =   "就醫序號:"
         Height          =   495
         Index           =   0
         Left            =   360
         TabIndex        =   11
         Top             =   720
         Width           =   495
      End
      Begin VB.Label Label11 
         Caption         =   "就診日期時間:"
         Height          =   495
         Index           =   0
         Left            =   240
         TabIndex        =   12
         Top             =   240
         Width           =   615
      End
      Begin VB.Label TreatHospVisit 
         BorderStyle     =   1  '單線固定
         BeginProperty Font 
            Name            =   "Times New Roman"
            Size            =   12
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   375
         Left            =   1200
         TabIndex        =   9
         Top             =   720
         Width           =   1095
      End
      Begin VB.Label TreatDateTime 
         BorderStyle     =   1  '單線固定
         BeginProperty Font 
            Name            =   "Times New Roman"
            Size            =   12
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   375
         Left            =   1200
         TabIndex        =   8
         Top             =   240
         Width           =   2175
      End
      Begin VB.Label TreatHospCode 
         BorderStyle     =   1  '單線固定
         BeginProperty Font 
            Name            =   "Times New Roman"
            Size            =   12
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   375
         Left            =   1200
         TabIndex        =   7
         Top             =   1200
         Width           =   2175
      End
   End
   Begin VB.CommandButton Command1 
      Caption         =   "取得就醫序號"
      Height          =   495
      Left            =   3960
      TabIndex        =   5
      Top             =   120
      Width           =   1335
   End
   Begin VB.Label Label2 
      Caption         =   "補卡註記"
      Height          =   495
      Left            =   3000
      TabIndex        =   17
      Top             =   120
      Width           =   375
   End
   Begin VB.Label Label1 
      Caption         =   "就醫類別:"
      Height          =   375
      Index           =   0
      Left            =   120
      TabIndex        =   4
      Top             =   120
      Width           =   495
   End
   Begin VB.Label Label4 
      Caption         =   "新生兒就醫註記:"
      Height          =   375
      Index           =   0
      Left            =   1440
      TabIndex        =   3
      Top             =   120
      Width           =   735
   End
End
Attribute VB_Name = "fhisGetSeqNumber256"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False

Private Sub Form_Load()

   Dim i As Integer
      
   i = csOpenCom(0)
  
End Sub


Private Sub Command2_Click()
    
    Unload fhisGetSeqNumber256
End Sub


Private Sub Command1_Click()
Dim iBufferLen As Integer
Dim err As Integer
Dim head_str As String
Dim counter As Integer
Dim pBuffer1 As String * 296
Dim pBuffer As String * 296

Dim pTreatAfterCheck As String * 1

Dim i As Integer




i = 0
iBufferLen = 165
iBufferLen = 296
If cBabyTreat.Text = "" Then
   cBabyTreat.Text = " "
End If

pTreatAfterCheck = cTreatAfterCheck.Text

err = hisGetSeqNumber256(cTreatItem.Text, cBabyTreat.Text, pTreatAfterCheck, pBuffer, iBufferLen)

If err = 0 Then

   TreatDateTime.Caption = ""

   TreatHospVisit.Caption = ""
   TreatHospCode.Caption = ""
   Text1 = ""
   SAMID.Caption = ""
   
  
       '就診日期時間日
        TreatDateTime.Caption = MidMbcs(pBuffer, 1, 13)
       
       '就醫序號
        TreatHospVisit.Caption = MidMbcs(pBuffer, 14, 4)
       
       '醫療院所代碼
        TreatHospCode.Caption = MidMbcs(pBuffer, 18, 10)
       
       '安全簽章
        Text1 = MidMbcs(pBuffer, 28, 256)
       
       '安全模組代碼
        SAMID.Caption = MidMbcs(pBuffer, 284, 12)

       '是否同日就診
        IsSameDay.Caption = MidMbcs(pBuffer, 296, 1)
       
Else
    MsgBox (err)
End If

End Sub

Function MidMbcs(ByVal str As String, start, length)
   MidMbcs = StrConv(MidB(StrConv(str, vbFromUnicode), start, length), vbUnicode)
End Function


Private Sub Form_Unload(Cancel As Integer)
   Dim i As Integer
   i = csCloseCom()
End Sub




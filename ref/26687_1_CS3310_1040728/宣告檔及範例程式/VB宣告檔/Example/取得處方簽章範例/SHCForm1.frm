VERSION 5.00
Begin VB.Form Form1 
   Caption         =   "處方箋簽章範例"
   ClientHeight    =   3465
   ClientLeft      =   60
   ClientTop       =   345
   ClientWidth     =   10380
   ForeColor       =   &H8000000A&
   LinkTopic       =   "Form1"
   PaletteMode     =   2  '自訂調色盤
   ScaleHeight     =   3465
   ScaleWidth      =   10380
   StartUpPosition =   3  '系統預設值
   Begin VB.CommandButton Command40 
      Caption         =   "寫入單筆處方箋取得簽章(3.0版新增)"
      Height          =   495
      Left            =   5520
      TabIndex        =   14
      Top             =   2640
      Width           =   1815
   End
   Begin VB.CommandButton Command39 
      Caption         =   "寫入多筆處方箋取得簽章(3.0版新增)"
      Height          =   495
      Left            =   2160
      TabIndex        =   13
      Top             =   2640
      Width           =   1815
   End
   Begin VB.TextBox Text5 
      Height          =   372
      Left            =   8520
      TabIndex        =   7
      Text            =   "1"
      Top             =   1800
      Width           =   492
   End
   Begin VB.TextBox Text4 
      Height          =   372
      Left            =   1800
      TabIndex        =   6
      Top             =   1800
      Width           =   1095
   End
   Begin VB.TextBox Text3 
      Height          =   372
      Left            =   480
      TabIndex        =   5
      Top             =   1800
      Width           =   1215
   End
   Begin VB.TextBox Text2 
      Height          =   372
      Left            =   3000
      TabIndex        =   4
      Top             =   1800
      Width           =   1572
   End
   Begin VB.TextBox Text1 
      Height          =   372
      Left            =   4680
      TabIndex        =   3
      Top             =   1800
      Width           =   3375
   End
   Begin VB.CommandButton cmdCloseCom 
      Caption         =   "Close Com"
      Enabled         =   0   'False
      BeginProperty Font 
         Name            =   "新細明體"
         Size            =   9
         Charset         =   136
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   495
      Left            =   1320
      TabIndex        =   1
      Top             =   240
      Width           =   735
   End
   Begin VB.CommandButton cmdOpenCom 
      BackColor       =   &H80000002&
      Caption         =   "Open Com"
      Enabled         =   0   'False
      BeginProperty Font 
         Name            =   "新細明體"
         Size            =   9
         Charset         =   136
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   495
      Left            =   480
      MaskColor       =   &H0080FFFF&
      TabIndex        =   0
      Top             =   240
      UseMaskColor    =   -1  'True
      Width           =   735
   End
   Begin VB.Label Label16 
      Caption         =   "Birthday"
      Height          =   255
      Left            =   1920
      TabIndex        =   12
      Top             =   1560
      Width           =   1095
   End
   Begin VB.Label Label15 
      Caption         =   "ID"
      Height          =   255
      Left            =   600
      TabIndex        =   11
      Top             =   1560
      Width           =   855
   End
   Begin VB.Label Label7 
      Caption         =   "Count"
      Height          =   255
      Left            =   8520
      TabIndex        =   10
      Top             =   1560
      Width           =   615
   End
   Begin VB.Label Label6 
      Caption         =   "DataWrite"
      Height          =   255
      Left            =   4680
      TabIndex        =   9
      Top             =   1560
      Width           =   2175
   End
   Begin VB.Label Label5 
      Caption         =   "Datetime"
      Height          =   255
      Left            =   3000
      TabIndex        =   8
      Top             =   1560
      Width           =   1215
   End
   Begin VB.Line Line2 
      X1              =   480
      X2              =   10200
      Y1              =   1320
      Y2              =   1320
   End
   Begin VB.Label lblCom 
      BeginProperty Font 
         Name            =   "新細明體"
         Size            =   12
         Charset         =   136
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H000000FF&
      Height          =   495
      Left            =   2760
      TabIndex        =   2
      Top             =   240
      Width           =   1455
   End
End
Attribute VB_Name = "Form1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Public comStatus

Private Sub Command39_Click()

Dim iWriteCount As Integer
Dim pDateTime As String * 14
Dim pPatientID As String * 11
Dim pPatientBirthDate As String * 10
Dim pDataWrite As String * 3660
Dim iLen As Integer
Dim pBuf As String * 2400
Dim err As Integer

    pDataWrite = Text1.Text
    pDateTime = Text2.Text
    pPatientID = Text3.Text
    pPatientBirthDate = Text4.Text
   
    iWriteCount = Val(Text5.Text)
    iLen = 40 * iWriteCount
    
    err = hisWriteMultiPrescriptSign(pDateTime, pPatientID, pPatientBirthDate, pDataWrite, iWriteCount, pBuf, iLen)
    
    If err <> 0 Then
        MsgBox (err)
    Else
        MsgBox "取得處方簽章內容：" & pBuf
        MsgBox ("OK")
    End If
End Sub

Private Sub Command40_Click()
Dim i As Integer
Dim iWriteCount As Integer


Dim pDateTime As String * 14
Dim pPatientID As String * 11
Dim pPatientBirthDate As String * 10
Dim pDataWrite As String * 61
Dim iLen As Integer
Dim pBuf As String * 40

    pDataWrite = Text1.Text
    pDateTime = Text2.Text
    pPatientID = Text3.Text
    pPatientBirthDate = Text4.Text
   
    iLen = 40
    
    err = hisWritePrescriptionSign(pDateTime, pPatientID, pPatientBirthDate, pDataWrite, pBuf, iLen)
    
    If err <> 0 Then
        MsgBox (err)
    Else
        MsgBox "取得處方簽章內容：" & pBuf
        MsgBox ("OK")
    End If
End Sub


Private Sub Form_Load()
Dim rdcom As Integer '
Dim i As Integer
Dim err As Integer
Dim pBuffer As String * 73
Dim iBufferLen As Integer

comStatus = -1
lblCom.Caption = comStatus

i = 0

Do While (i <= 3)
 rdcom = csOpenCom(i)
 If rdcom = 0 Then
 Exit Do
 End If
 i = i + 1
Loop

If (rdcom = 0) Then
    'MsgBox "開啟com成功"
    comStatus = 0
    lblCom.Caption = "讀卡機正常"
Else
    MsgBox "讀卡機偵測失敗，程式無法使用將自動關閉，請查明原因後再重新啟動程式", vbCritical, "錯誤!"
    End
End If

End Sub

Private Sub Form_Unload(Cancel As Integer)
Dim rdcom  As Integer
rdcom = csCloseCom
If (rdrcom = 0) Then
    'MsgBox "關閉com成功"
    'comStatus = -1
    'Label12.Caption = "讀卡機不可用"
    comStatus = -1
Else
    MsgBox "關閉讀卡機失敗，請查明原因", vbCritical, "錯誤!"
End If

'Close all open files
Close #1
Close #2
Close #3

End Sub


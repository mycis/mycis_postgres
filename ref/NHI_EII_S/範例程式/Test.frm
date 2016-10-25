VERSION 5.00
Begin VB.Form Form1 
   Caption         =   "醫療資料傳輸共通介面 API"
   ClientHeight    =   6540
   ClientLeft      =   60
   ClientTop       =   345
   ClientWidth     =   13365
   LinkTopic       =   "Form1"
   ScaleHeight     =   6540
   ScaleWidth      =   13365
   StartUpPosition =   3  'Windows Default
   Begin VB.TextBox ReturnVal 
      Enabled         =   0   'False
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   13.5
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Left            =   6840
      MaxLength       =   10
      TabIndex        =   20
      Top             =   5040
      Width           =   1095
   End
   Begin VB.TextBox sNHI_ID 
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   13.5
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Left            =   6840
      MaxLength       =   12
      TabIndex        =   18
      Text            =   "XXXXXXXXXXXX"
      Top             =   4440
      Width           =   2655
   End
   Begin VB.TextBox sLocal_ID 
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   13.5
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Left            =   6840
      MaxLength       =   12
      TabIndex        =   17
      Text            =   "NHI_XXXXXXXX"
      Top             =   3840
      Width           =   2655
   End
   Begin VB.TextBox sDownloadPath 
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   13.5
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Left            =   6840
      MaxLength       =   256
      TabIndex        =   16
      Text            =   "C:\AP\"
      Top             =   3240
      Width           =   6375
   End
   Begin VB.TextBox sTypeCode 
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   13.5
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Left            =   6840
      MaxLength       =   2
      TabIndex        =   15
      Text            =   "00"
      Top             =   2640
      Width           =   495
   End
   Begin VB.TextBox sRequestFileName 
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   13.5
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Left            =   6840
      MaxLength       =   256
      TabIndex        =   14
      Text            =   "C:\AP\3501200000-1010704-001.txt"
      Top             =   2040
      Width           =   6375
   End
   Begin VB.TextBox sUploadFileName 
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   13.5
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Left            =   6840
      MaxLength       =   256
      TabIndex        =   13
      Text            =   "C:\AP\3501200000-1010704-001.txt"
      Top             =   1440
      Width           =   6375
   End
   Begin VB.TextBox sReaderDllPathName 
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   13.5
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Left            =   6840
      MaxLength       =   256
      TabIndex        =   12
      Text            =   "C:\AP\Reader.dll"
      Top             =   840
      Width           =   6375
   End
   Begin VB.TextBox iRs232PortNo 
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   13.5
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Left            =   6840
      MaxLength       =   2
      TabIndex        =   11
      Text            =   "0"
      Top             =   240
      Width           =   855
   End
   Begin VB.CommandButton btnNHI_GetB 
      Caption         =   "NHI_GetB"
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   13.5
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Left            =   240
      TabIndex        =   2
      Top             =   1440
      Width           =   2775
   End
   Begin VB.CommandButton btnNHI_DownloadB 
      Caption         =   "NHI_DownloadB"
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   13.5
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Left            =   240
      TabIndex        =   1
      Top             =   840
      Width           =   2775
   End
   Begin VB.CommandButton btnNHI_SendB 
      Caption         =   "NHI_SendB"
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   13.5
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Left            =   240
      TabIndex        =   0
      Top             =   240
      Width           =   2775
   End
   Begin VB.Label Return 
      Caption         =   "[out] Return："
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   13.5
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Left            =   3480
      TabIndex        =   19
      Top             =   5040
      Width           =   3135
   End
   Begin VB.Label LabelsNHI_ID 
      Caption         =   "[in/out] sNHI_ID："
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   13.5
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Left            =   3480
      TabIndex        =   10
      Top             =   4440
      Width           =   3135
   End
   Begin VB.Label LabelsLocal_ID 
      Caption         =   "[in/out] sLocal_ID："
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   13.5
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Left            =   3480
      TabIndex        =   9
      Top             =   3840
      Width           =   3135
   End
   Begin VB.Label LabelsDownloadPath 
      Caption         =   "[in]sDownloadPath："
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   13.5
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Left            =   3480
      TabIndex        =   8
      Top             =   3240
      Width           =   3135
   End
   Begin VB.Label LabelsTypeCode 
      Caption         =   "[in]sTypeCode："
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   13.5
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Left            =   3480
      TabIndex        =   7
      Top             =   2640
      Width           =   3135
   End
   Begin VB.Label LabelsRequestFileName 
      Caption         =   "[in]sRequestFileName："
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   13.5
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Left            =   3480
      TabIndex        =   6
      Top             =   2040
      Width           =   3135
   End
   Begin VB.Label LabelsUploadFileName 
      Caption         =   "[in]sUploadFileName："
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   13.5
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Left            =   3480
      TabIndex        =   5
      Top             =   1440
      Width           =   3135
   End
   Begin VB.Label LabelsReaderDllPathName 
      Caption         =   "[in]sReaderDllPathName："
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   13.5
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Left            =   3480
      TabIndex        =   4
      Top             =   840
      Width           =   3135
   End
   Begin VB.Label LableiRs232PortNo 
      Caption         =   "[in]iRs232PortNo："
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   13.5
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   375
      Left            =   3480
      TabIndex        =   3
      Top             =   240
      Width           =   2775
   End
End
Attribute VB_Name = "Form1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False

Private Sub btnNHI_DownloadB_Click()
    Dim iRet As Integer
    Dim l_iRs232PortNo As Integer
    Dim l_sReaderDllPathName As String
    Dim l_sDownloadFileName As String
    Dim l_sTypeCode As String
    Dim l_sLocal_ID() As Byte
    Dim l_sNHI_ID() As Byte
    ReDim l_sLocal_ID(13)
    ReDim l_sNHI_ID(13)
    Dim strLocal_ID As String
    Dim strNHI_ID As String
    l_iRs232PortNo = Int(iRs232PortNo.Text)
    l_sReaderDllPathName = sReaderDllPathName.Text
    l_sDownloadFileName = sRequestFileName.Text
    l_sTypeCode = sTypeCode.Text
    iRet = NHI_DownloadB(l_iRs232PortNo, l_sReaderDllPathName, l_sDownloadFileName, l_sTypeCode, l_sLocal_ID(0), l_sNHI_ID(0))
    strLocal_ID = Trim(StrConv(l_sLocal_ID, vbUnicode))
    strNHI_ID = Trim(StrConv(l_sNHI_ID, vbUnicode))
    sLocal_ID.Text = strLocal_ID
    sNHI_ID.Text = strNHI_ID
    ReturnVal.Text = Format(iRet)
End Sub

Private Sub btnNHI_GetB_Click()
    Dim iRet As Integer
    Dim l_iRs232PortNo As Integer
    Dim l_sReaderDllPathName As String
    Dim l_sDownloadPath As String
    Dim strLocal_ID As String
    Dim strNHI_ID As String
    l_iRs232PortNo = Int(iRs232PortNo.Text)
    l_sReaderDllPathName = sReaderDllPathName.Text
    sDownloadPath = sDownloadPath.Text
    strLocal_ID = sLocal_ID.Text
    strNHI_ID = sNHI_ID.Text
    iRet = NHI_GetB(l_iRs232PortNo, l_sReaderDllPathName, strLocal_ID, strNHI_ID, sDownloadPath)
    ReturnVal.Text = Format(iRet)
End Sub

Private Sub btnNHI_SendB_Click()
    Dim iRet As Integer
    Dim l_iRs232PortNo As Integer
    Dim l_sReaderDllPathName As String
    Dim l_sUploadFileName As String
    Dim l_sTypeCode As String
    Dim l_sLocal_ID() As Byte
    Dim l_sNHI_ID() As Byte
    ReDim l_sLocal_ID(13)
    ReDim l_sNHI_ID(13)
    Dim strLocal_ID As String
    Dim strNHI_ID As String
    l_iRs232PortNo = Int(iRs232PortNo.Text)
    l_sReaderDllPathName = sReaderDllPathName.Text
    l_sUploadFileName = sUploadFileName.Text
    l_sTypeCode = sTypeCode.Text
    iRet = NHI_SendB(l_iRs232PortNo, l_sReaderDllPathName, l_sUploadFileName, l_sTypeCode, l_sLocal_ID(0), l_sNHI_ID(0))
    strLocal_ID = Trim(StrConv(l_sLocal_ID, vbUnicode))
    strNHI_ID = Trim(StrConv(l_sNHI_ID, vbUnicode))
    sLocal_ID.Text = strLocal_ID
    sNHI_ID.Text = strNHI_ID
    ReturnVal.Text = Format(iRet)
End Sub

VERSION 5.00
Begin VB.Form Form1 
   Caption         =   "Form1"
   ClientHeight    =   3090
   ClientLeft      =   60
   ClientTop       =   450
   ClientWidth     =   4680
   LinkTopic       =   "Form1"
   ScaleHeight     =   3090
   ScaleWidth      =   4680
   StartUpPosition =   3  '�t�ιw�]��
   Begin VB.CommandButton Command1 
      Caption         =   "csGetVersionEx"
      Height          =   615
      Left            =   1440
      TabIndex        =   0
      Top             =   1920
      Width           =   1455
   End
End
Attribute VB_Name = "Form1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private Sub Command1_Click()
Dim sPath As String * 256
Dim iRet As Long, iLen As Integer

iRet = csGetVersionEx(sPath)
MsgBox "�����N�X" & iRet
MsgBox "CSHIS���|��" & sPath

End Sub

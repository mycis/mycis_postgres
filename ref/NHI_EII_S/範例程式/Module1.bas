Attribute VB_Name = "Module1"
Public Declare Function NHI_SendB Lib "nhi_eiiapi.dll" _
                        (ByVal viRs232PortNo As Integer, _
                         ByVal vsReaderDllPathName As String, _
                         ByVal vsUploadFileName As String, _
                         ByVal vsTypeCode As String, _
                         ByRef vsLocal_ID As Any, _
                         ByRef vsNHI_ID As Any) As Integer


Public Declare Function NHI_DownloadB Lib "nhi_eiiapi.dll" _
                        (ByVal viRs232PortNo As Integer, _
                         ByVal vsReaderDllPathName As String, _
                         ByVal vsRequestFileName As String, _
                         ByVal vsTypeCode As String, _
                         ByRef vsLocal_ID As Any, _
                         ByRef vsNHI_ID As Any) As Integer


Public Declare Function NHI_GetB Lib "nhi_eiiapi.dll" _
                        (ByVal viRs232PortNo As Integer, _
                         ByVal vsReaderDllPathName As String, _
                         ByVal vsLocal_ID As String, _
                         ByVal vsNHI_ID As String, _
                         ByVal vsDownloadPath As String) As Integer




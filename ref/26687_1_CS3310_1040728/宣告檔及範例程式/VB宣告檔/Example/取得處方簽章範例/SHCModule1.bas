Attribute VB_Name = "SHCModule1"
' 1.31 �}��Ū�d���s����
Declare Function csOpenCom Lib "cshis.dll" (ByVal pcom As Integer) As Integer
' 1.32 ����Ū�d���s����
Declare Function csCloseCom Lib "cshis.dll" () As Integer

'�B���g�J-�tñ��
Declare Function hisWritePrescriptionSign Lib "cshis.dll" (ByVal pDateTime As String, ByVal pPatientID As String, ByVal pPatientBirthDate As String, ByVal pDataWrite As String, ByVal pBuffer As String, ByRef iLen As Integer) As Integer
Declare Function hisWriteMultiPrescriptSign Lib "cshis.dll" (ByVal pDateTime As String, ByVal pPatientID As String, ByVal pPatientBirthDate As String, ByVal pDataWrite As String, ByRef iWriteCount As Integer, ByVal pBuffer As String, ByRef iLen As Integer) As Integer

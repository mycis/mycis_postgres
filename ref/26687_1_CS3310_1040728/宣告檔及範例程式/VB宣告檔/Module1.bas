Attribute VB_Name = "Module1"
' 1.1 Ū�����ݭӤHPIN�X���
Declare Function hisGetBasicData Lib "cshis.dll" (ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer
' 1.2 �����γ����Ū���򥻸��
Declare Function hisGetRegisterBasic Lib "cshis.dll" (ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer
' 1.3 �w���O�������@�~
Declare Function hisGetRegisterPrevent Lib "cshis.dll" (ByVal pBuffer As String, ByRef intpBufferLen As Integer) As Integer
' 1.4 �������e�ˬd�����@�~
Declare Function hisGetRegisterPregnant Lib "cshis.dll" (ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer
' 1.5 Ū���N���Ƥ���HPC�d������
Declare Function hisGetTreatmentNoNeedHPC Lib "cshis.dll" (ByVal strpBuffer As String, ByRef intpBufferLen As Integer) As Integer
' 1.6 Ū���N��֭p���
Declare Function hisGetCumulativeData Lib "cshis.dll" (ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer
' 1.7 Ū�������O�νu�֭p
Declare Function hisGetCumulativeFee Lib "cshis.dll" (ByVal strpBuffer As String, ByRef intpBufferLen As Integer) As Integer
' 1.8 Ū���N���ƻ�HPC�d������
Declare Function hisGetTreatmentNeedHPC Lib "cshis.dll" (ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer
' 1.9 ���o�N��Ǹ�
Declare Function hisGetSeqNumber Lib "cshis.dll" (ByVal strcTreatItem As String, ByVal strcBabyTreat As String, strpBuffer As Any, ByRef intpBufferLen As Integer) As Integer
' 1.10 Ū���B���@�~
Declare Function hisReadPrescription Lib "cshis.dll" (ByVal pOutpatientPrescription As String, ByRef iBufferLenOutpatient As Integer, ByVal pLongTermPrescription As String, ByRef iBufferLenLongTerm As Integer, ByVal pImportantTreatmentCode As String, ByRef iBufferLenImportant As Integer, ByVal pIrritationDrug As String, ByRef iBufferLenIrritation As Integer) As Integer
' 1.11 Ū���w�����ظ��
Declare Function hisGetInoculateData Lib "cshis.dll" (ByVal strpBuffer As String, ByRef intpBufferLen As Integer) As Integer
' 1.12 Ū�����x���ظ��
Declare Function hisGetOrganDonate Lib "cshis.dll" (ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer
' 1.13 Ū������p���q�ܸ��
Declare Function HisGetEmergentTel Lib "cshis.dll" Alias "hisGetEmergentTel" (ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer
' 1.14 Ū���̪�@���N��Ǹ�
Declare Function hisGetLastSeqNum Lib "cshis.dll" (ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer
' 1.15 Ū���d�����A
Declare Function hisGetCardStatus Lib "cshis.dll" (ByVal CardType As Integer) As Integer
' 1.16 �N��E����Ƽg�J�@�~
Declare Function hisWriteTreatmentCode Lib "cshis.dll" (ByVal pDateTime As String, ByVal pPatientID As String, ByVal pPatientBirthDate As String, ByVal pDataWrite As String, ByVal pBufferDocID As String) As Integer
' 1.17 �N��O�θ�Ƽg�J�@�~
Declare Function hisWriteTreatmentFee Lib "cshis.dll" (ByVal pDateTime As String, ByVal pPatientID As String, ByVal pPatientBirthDate As String, ByVal pDataWrite As String) As Integer
' 1.18 �B���g�J�@�~
Declare Function hisWritePrescription Lib "cshis.dll" (ByVal pDateTime As String, ByVal pPatientID As String, ByVal pPatientBirthDate As String, ByVal pDataWrite As String) As Integer
' 1.19 �s�ͨ���O�g�J�@�~
Declare Function hisWriteNewBorn Lib "cshis.dll" (ByVal pPatientID As String, ByVal pPatientBirthDate As String, ByVal pNewBornDate As String, ByVal pNoOfDelivered As String) As Integer
' 1.20 �L���Ī��g�J�@�~
Declare Function hisWriteAllergicMedicines Lib "cshis.dll" (ByVal pPatientID As String, ByVal pPatientBirthDate As String, ByVal pDataWrite As String, ByVal pBufferDocID As String) As Integer
' 1.21 �P�N���x���ؤΦw��w�M�������O�g�J�@�~
Declare Function hisWriteOrganDonate Lib "cshis.dll" (ByVal pPatientID As String, ByVal pPatientBirthDate As String, ByVal pOrganDonate As String) As Integer
' 1.22 �w���O����Ƽg�J�@�~
Declare Function hisWriteHealthInsurance Lib "cshis.dll" (ByVal pPatientID As String, ByVal pPatientBirthDate As String, ByVal pServiceItem As String, ByVal pServiceItemCode As String) As Integer
' 1.23 ����p���q�ܸ�Ƽg�J�@�~
Declare Function hisWriteEmergentTel Lib "cshis.dll" (ByVal pPatientID As String, ByVal pPatientBirthDate As String, ByVal pEmergentTel As String) As Integer
' 1.24 �g�J���e�ˬd���
Declare Function hisWritePredeliveryCheckup Lib "cshis.dll" (ByVal pPatientID As String, ByVal pPatientBirthDate As String, ByVal pCheckupCode As String) As Integer
' 1.25 �M�����e�ˬd���
Declare Function hisDeletePredeliveryData Lib "cshis.dll" (ByVal pPatientID As String, ByVal pPatientBirthDate As String) As Integer
' 1.26 �w�����ظ�Ƽg�J�@�~
Declare Function hisWriteInoculateData Lib "cshis.dll" (ByVal pPatientID As String, ByVal pPatientBirthDate As String, ByVal pItem As String, ByVal pPackageNumber As String) As Integer
' 1.27 ���Ұ��OIC�d��PIN��
Declare Function csVerifyHCPIN Lib "cshis.dll" () As Integer
' 1.28 ��J�s�����OIC�dPIN��
Declare Function csInputHCPIN Lib "cshis.dll" () As Integer
' 1.29 ���ΰ��OIC�d��PIN�X��J�\��
Declare Function csDisableHCPIN Lib "cshis.dll" () As Integer
' 1.30 ���OIC�d�d�����e��s�@�~
Declare Function csUpdateHCContents Lib "cshis.dll" () As Integer
' 1.31 �}��Ū�d���s����
Declare Function csOpenCom Lib "cshis.dll" (ByVal pcom As Integer) As Integer
' 1.32 ����Ū�d���s����
Declare Function csCloseCom Lib "cshis.dll" () As Integer
' 1.33 Ū�����j�˯f���O���
Declare Function hisGetCriticalIllness Lib "cshis.dll" (ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer

'1.34 csGetDateTime (Ū��Ū�d������ɶ�)
Declare Function csGetDateTime Lib "cshis.dll" (ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer

'1.35 csGetCardNo (Ū���d�����X)
Declare Function csGetCardNo Lib "cshis.dll" (ByVal CardType As Integer, ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer

'1.36 csISSetPIN (�ˬd���OIC�d�O�_�]�w�K�X)
Declare Function csISSetPIN Lib "cshis.dll" () As Integer

'1.37 hisGetSeqNumber256 (���o�N��Ǹ��s��)
Declare Function hisGetSeqNumber256 Lib "cshis.dll" (ByVal cTreatItem As String, ByVal cBabyTreat As String, ByVal cTreatAfterCheck As String, ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer

'1.38 hisGetRegisterBasic2(�����γ����Ū���򥻸��)
Declare Function hisGetRegisterBasic2 Lib "cshis.dll" (ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer

'1.39 csUnGetSeqNumber(�^�_�N���Ʋ֭p��---�h��)
Declare Function csUnGetSeqNumber Lib "cshis.dll" (ByVal pUnTreatDate As String) As Integer

'1.40 csUpdateHCNoReset (���OIC�d�d�����e��s�@�~)
Declare Function csUpdateHCNoReset Lib "cshis.dll" () As Integer

'1.41 hisReadPrescriptMain (Ū���N����-���E�B���)
Declare Function hisReadPrescriptMain Lib "cshis.dll" (ByVal pOutpatientPrescription As String, ByRef iBufferLenOutpatient As Integer, ByVal iStartPos As Integer, ByVal iEndPos As Integer, ByRef iRecCount As Integer) As Integer

'1.42 hisReadPrescriptLongTerm (Ū���N����-�����B���)
Declare Function hisReadPrescriptLongTerm Lib "cshis.dll" (ByVal pLongTermPrescription As String, ByRef iBufferLenLongTerm As Integer, ByVal iStartPos As Integer, ByVal iEndPos As Integer, ByRef iRecCount As Integer) As Integer

'1.43 hisReadPrescriptHVE (Ū���N����-���n��O)
Declare Function hisReadPrescriptHVE Lib "cshis.dll" (ByVal pImportantTreatmentCode As String, ByRef iBufferLenImportant As Integer, ByVal iStartPos As Integer, ByVal iEndPos As Integer, ByRef iRecCount As Integer) As Integer

'1.44 hisReadPrescriptAllergic (Ū���N����-�L���Ī�)
Declare Function hisReadPrescriptAllergic Lib "cshis.dll" (ByVal pIrritationDrug As String, ByRef iBufferLenIrritation As Integer, ByVal iStartPos As Integer, ByVal iEndPos As Integer, ByRef iRecCount As Integer) As Integer

'1.45 hisWriteMultiPrescript (�h���B���g�J�@�~)
'Declare Function hisWriteMultiPrescript Lib "cshis.dll" (ByRef pDateTime As String, ByRef pPatientID As String, ByRef pPatientBirthDate As String, ByRef pDataWrite As String, ByRef iWriteCount As Integer) As Integer
Declare Function hisWriteMultiPrescript Lib "cshis.dll" (ByVal pDateTime As String, ByVal pPatientID As String, ByVal pPatientBirthDate As String, ByVal pDataWrite As String, ByRef iWriteCount As Integer) As Integer

'1.46 hisWriteAllergicNum (�L���Ī��g�J���w���@�~)
Declare Function hisWriteAllergicNum Lib "cshis.dll" (ByVal pPatientID As String, ByVal pPatientBirthDate As String, ByVal pDataWrite As String, ByVal pBufferDocID As String, ByVal iNum As Integer) As Integer
'Declare Function hisWriteAllergicNum Lib "cshis.dll" (ByRef pPatientID As String, ByRef pPatientBirthDate As String, ByRef pDataWrite As String, ByRef pBufferDocID As String, ByVal iNum As Integer) As Integer

'1.47 hisWriteTreatmentData (�N��E����ƤζO�μg�J�@�~)
Declare Function hisWriteTreatmentData Lib "cshis.dll" (ByVal pDateTime As String, ByVal pPatientID As String, ByVal pPatientBirthDate As String, ByVal pDataWrite As String, ByVal pBufferDocID As String) As Integer

'1.48
Declare Function hisWritePrescriptionSign Lib "cshis.dll" (ByVal pDateTime As String, ByVal pPatientID As String, ByVal pPatientBirthDate As String, ByVal pDataWrite As String, ByVal pBuffer As String, ByRef iLen As Integer) As Integer

'1.49
Declare Function hisWriteMultiPrescriptSign Lib "cshis.dll" (ByVal pDateTime As String, ByVal pPatientID As String, ByVal pPatientBirthDate As String, ByVal pDataWrite As String, ByRef iWriteCount As Integer, ByVal pBuffer As String, ByRef iLen As Integer) As Integer

'1.50
Declare Function hisGetCriticalIllnessID Lib "cshis.dll" (ByVal pPatientID As String, ByVal pPatientBirthDate As String, ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer

'1.52 
Declare Function csSoftwareReset Lib "cshis.dll" (ByVal iType As Long) As Integer
' 2.1 �w���Ҳջ{��
Declare Function csVerifySAMDC Lib "cshis.dll" () As Integer
' 2.2 
Declare Function csGetHospID Lib "cshis.dll" (ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer

' 3.1 ��ƤW��
Declare Function csUploadData Lib "cshis.dll" (ByVal pUploadFileName As String, ByVal fFileSize As String, ByVal pNumber As String, ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer
' 4.1 ���o��ƤH���d���A
Declare Function hpcGetHPCStatus Lib "cshis.dll" (ByVal Req As Integer, ByRef Status As Integer) As Integer
' 4.2 �ˬd��ƤH���d��PIN��
Declare Function hpcVerifyHPCPIN Lib "cshis.dll" () As Integer
' 4.3 ��J�s����ƤH���d��PIN��
Declare Function hpcInputHPCPIN Lib "cshis.dll" () As Integer
' 4.4 �Ѷ}�����ƤH���d
Declare Function hpcUnlockHPC Lib "cshis.dll" () As Integer
' 4.5 ���o��ƤH���d�Ǹ�
Declare Function hpcGetHPCSN Lib "cshis.dll" (ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer
' 4.6 ���o��ƤH���d�����Ҧr��
Declare Function hpcGetHPCSSN Lib "cshis.dll" (ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer
' 4.7 ���o��ƤH���d����m�W
Declare Function hpcGetHPCCNAME Lib "cshis.dll" (ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer
' 4.8 ���o��ƤH���d�^��m�W
Declare Function hpcGetHPCENAME Lib "cshis.dll" (ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer
                 
' 5.1 �i��e�f�E�_�X��X
Declare Function hisGetICD10EnC Lib "cshis.dll" (ByVal pIN As String, ByVal pOUT As String) As Integer
' 5.2 �i��e�f�E�_�X�ѩ�X
Declare Function hisGetICD10DeC Lib "cshis.dll" (ByVal pIN As String, ByVal pOUT As String) As Integer

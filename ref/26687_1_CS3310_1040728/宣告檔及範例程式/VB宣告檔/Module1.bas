Attribute VB_Name = "Module1"
' 1.1 讀取不需個人PIN碼資料
Declare Function hisGetBasicData Lib "cshis.dll" (ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer
' 1.2 掛號或報到時讀取基本資料
Declare Function hisGetRegisterBasic Lib "cshis.dll" (ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer
' 1.3 預防保健掛號作業
Declare Function hisGetRegisterPrevent Lib "cshis.dll" (ByVal pBuffer As String, ByRef intpBufferLen As Integer) As Integer
' 1.4 孕婦產前檢查掛號作業
Declare Function hisGetRegisterPregnant Lib "cshis.dll" (ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer
' 1.5 讀取就醫資料不需HPC卡的部份
Declare Function hisGetTreatmentNoNeedHPC Lib "cshis.dll" (ByVal strpBuffer As String, ByRef intpBufferLen As Integer) As Integer
' 1.6 讀取就醫累計資料
Declare Function hisGetCumulativeData Lib "cshis.dll" (ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer
' 1.7 讀取醫療費用線累計
Declare Function hisGetCumulativeFee Lib "cshis.dll" (ByVal strpBuffer As String, ByRef intpBufferLen As Integer) As Integer
' 1.8 讀取就醫資料需HPC卡的部份
Declare Function hisGetTreatmentNeedHPC Lib "cshis.dll" (ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer
' 1.9 取得就醫序號
Declare Function hisGetSeqNumber Lib "cshis.dll" (ByVal strcTreatItem As String, ByVal strcBabyTreat As String, strpBuffer As Any, ByRef intpBufferLen As Integer) As Integer
' 1.10 讀取處方箋作業
Declare Function hisReadPrescription Lib "cshis.dll" (ByVal pOutpatientPrescription As String, ByRef iBufferLenOutpatient As Integer, ByVal pLongTermPrescription As String, ByRef iBufferLenLongTerm As Integer, ByVal pImportantTreatmentCode As String, ByRef iBufferLenImportant As Integer, ByVal pIrritationDrug As String, ByRef iBufferLenIrritation As Integer) As Integer
' 1.11 讀取預防接種資料
Declare Function hisGetInoculateData Lib "cshis.dll" (ByVal strpBuffer As String, ByRef intpBufferLen As Integer) As Integer
' 1.12 讀取器官捐贈資料
Declare Function hisGetOrganDonate Lib "cshis.dll" (ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer
' 1.13 讀取緊急聯絡電話資料
Declare Function HisGetEmergentTel Lib "cshis.dll" Alias "hisGetEmergentTel" (ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer
' 1.14 讀取最近一次就醫序號
Declare Function hisGetLastSeqNum Lib "cshis.dll" (ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer
' 1.15 讀取卡片狀態
Declare Function hisGetCardStatus Lib "cshis.dll" (ByVal CardType As Integer) As Integer
' 1.16 就醫診療資料寫入作業
Declare Function hisWriteTreatmentCode Lib "cshis.dll" (ByVal pDateTime As String, ByVal pPatientID As String, ByVal pPatientBirthDate As String, ByVal pDataWrite As String, ByVal pBufferDocID As String) As Integer
' 1.17 就醫費用資料寫入作業
Declare Function hisWriteTreatmentFee Lib "cshis.dll" (ByVal pDateTime As String, ByVal pPatientID As String, ByVal pPatientBirthDate As String, ByVal pDataWrite As String) As Integer
' 1.18 處方箋寫入作業
Declare Function hisWritePrescription Lib "cshis.dll" (ByVal pDateTime As String, ByVal pPatientID As String, ByVal pPatientBirthDate As String, ByVal pDataWrite As String) As Integer
' 1.19 新生兒註記寫入作業
Declare Function hisWriteNewBorn Lib "cshis.dll" (ByVal pPatientID As String, ByVal pPatientBirthDate As String, ByVal pNewBornDate As String, ByVal pNoOfDelivered As String) As Integer
' 1.20 過敏藥物寫入作業
Declare Function hisWriteAllergicMedicines Lib "cshis.dll" (ByVal pPatientID As String, ByVal pPatientBirthDate As String, ByVal pDataWrite As String, ByVal pBufferDocID As String) As Integer
' 1.21 同意器官捐贈及安寧緩和醫療註記寫入作業
Declare Function hisWriteOrganDonate Lib "cshis.dll" (ByVal pPatientID As String, ByVal pPatientBirthDate As String, ByVal pOrganDonate As String) As Integer
' 1.22 預防保健資料寫入作業
Declare Function hisWriteHealthInsurance Lib "cshis.dll" (ByVal pPatientID As String, ByVal pPatientBirthDate As String, ByVal pServiceItem As String, ByVal pServiceItemCode As String) As Integer
' 1.23 緊急聯絡電話資料寫入作業
Declare Function hisWriteEmergentTel Lib "cshis.dll" (ByVal pPatientID As String, ByVal pPatientBirthDate As String, ByVal pEmergentTel As String) As Integer
' 1.24 寫入產前檢查資料
Declare Function hisWritePredeliveryCheckup Lib "cshis.dll" (ByVal pPatientID As String, ByVal pPatientBirthDate As String, ByVal pCheckupCode As String) As Integer
' 1.25 清除產前檢查資料
Declare Function hisDeletePredeliveryData Lib "cshis.dll" (ByVal pPatientID As String, ByVal pPatientBirthDate As String) As Integer
' 1.26 預防接種資料寫入作業
Declare Function hisWriteInoculateData Lib "cshis.dll" (ByVal pPatientID As String, ByVal pPatientBirthDate As String, ByVal pItem As String, ByVal pPackageNumber As String) As Integer
' 1.27 驗證健保IC卡之PIN值
Declare Function csVerifyHCPIN Lib "cshis.dll" () As Integer
' 1.28 輸入新的健保IC卡PIN值
Declare Function csInputHCPIN Lib "cshis.dll" () As Integer
' 1.29 停用健保IC卡之PIN碼輸入功能
Declare Function csDisableHCPIN Lib "cshis.dll" () As Integer
' 1.30 健保IC卡卡片內容更新作業
Declare Function csUpdateHCContents Lib "cshis.dll" () As Integer
' 1.31 開啟讀卡機連結埠
Declare Function csOpenCom Lib "cshis.dll" (ByVal pcom As Integer) As Integer
' 1.32 關閉讀卡機連結埠
Declare Function csCloseCom Lib "cshis.dll" () As Integer
' 1.33 讀取重大傷病註記資料
Declare Function hisGetCriticalIllness Lib "cshis.dll" (ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer

'1.34 csGetDateTime (讀取讀卡機日期時間)
Declare Function csGetDateTime Lib "cshis.dll" (ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer

'1.35 csGetCardNo (讀取卡片號碼)
Declare Function csGetCardNo Lib "cshis.dll" (ByVal CardType As Integer, ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer

'1.36 csISSetPIN (檢查健保IC卡是否設定密碼)
Declare Function csISSetPIN Lib "cshis.dll" () As Integer

'1.37 hisGetSeqNumber256 (取得就醫序號新版)
Declare Function hisGetSeqNumber256 Lib "cshis.dll" (ByVal cTreatItem As String, ByVal cBabyTreat As String, ByVal cTreatAfterCheck As String, ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer

'1.38 hisGetRegisterBasic2(掛號或報到時讀取基本資料)
Declare Function hisGetRegisterBasic2 Lib "cshis.dll" (ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer

'1.39 csUnGetSeqNumber(回復就醫資料累計值---退掛)
Declare Function csUnGetSeqNumber Lib "cshis.dll" (ByVal pUnTreatDate As String) As Integer

'1.40 csUpdateHCNoReset (健保IC卡卡片內容更新作業)
Declare Function csUpdateHCNoReset Lib "cshis.dll" () As Integer

'1.41 hisReadPrescriptMain (讀取就醫資料-門診處方箋)
Declare Function hisReadPrescriptMain Lib "cshis.dll" (ByVal pOutpatientPrescription As String, ByRef iBufferLenOutpatient As Integer, ByVal iStartPos As Integer, ByVal iEndPos As Integer, ByRef iRecCount As Integer) As Integer

'1.42 hisReadPrescriptLongTerm (讀取就醫資料-長期處方箋)
Declare Function hisReadPrescriptLongTerm Lib "cshis.dll" (ByVal pLongTermPrescription As String, ByRef iBufferLenLongTerm As Integer, ByVal iStartPos As Integer, ByVal iEndPos As Integer, ByRef iRecCount As Integer) As Integer

'1.43 hisReadPrescriptHVE (讀取就醫資料-重要醫令)
Declare Function hisReadPrescriptHVE Lib "cshis.dll" (ByVal pImportantTreatmentCode As String, ByRef iBufferLenImportant As Integer, ByVal iStartPos As Integer, ByVal iEndPos As Integer, ByRef iRecCount As Integer) As Integer

'1.44 hisReadPrescriptAllergic (讀取就醫資料-過敏藥物)
Declare Function hisReadPrescriptAllergic Lib "cshis.dll" (ByVal pIrritationDrug As String, ByRef iBufferLenIrritation As Integer, ByVal iStartPos As Integer, ByVal iEndPos As Integer, ByRef iRecCount As Integer) As Integer

'1.45 hisWriteMultiPrescript (多筆處方箋寫入作業)
'Declare Function hisWriteMultiPrescript Lib "cshis.dll" (ByRef pDateTime As String, ByRef pPatientID As String, ByRef pPatientBirthDate As String, ByRef pDataWrite As String, ByRef iWriteCount As Integer) As Integer
Declare Function hisWriteMultiPrescript Lib "cshis.dll" (ByVal pDateTime As String, ByVal pPatientID As String, ByVal pPatientBirthDate As String, ByVal pDataWrite As String, ByRef iWriteCount As Integer) As Integer

'1.46 hisWriteAllergicNum (過敏藥物寫入指定欄位作業)
Declare Function hisWriteAllergicNum Lib "cshis.dll" (ByVal pPatientID As String, ByVal pPatientBirthDate As String, ByVal pDataWrite As String, ByVal pBufferDocID As String, ByVal iNum As Integer) As Integer
'Declare Function hisWriteAllergicNum Lib "cshis.dll" (ByRef pPatientID As String, ByRef pPatientBirthDate As String, ByRef pDataWrite As String, ByRef pBufferDocID As String, ByVal iNum As Integer) As Integer

'1.47 hisWriteTreatmentData (就醫診療資料及費用寫入作業)
Declare Function hisWriteTreatmentData Lib "cshis.dll" (ByVal pDateTime As String, ByVal pPatientID As String, ByVal pPatientBirthDate As String, ByVal pDataWrite As String, ByVal pBufferDocID As String) As Integer

'1.48
Declare Function hisWritePrescriptionSign Lib "cshis.dll" (ByVal pDateTime As String, ByVal pPatientID As String, ByVal pPatientBirthDate As String, ByVal pDataWrite As String, ByVal pBuffer As String, ByRef iLen As Integer) As Integer

'1.49
Declare Function hisWriteMultiPrescriptSign Lib "cshis.dll" (ByVal pDateTime As String, ByVal pPatientID As String, ByVal pPatientBirthDate As String, ByVal pDataWrite As String, ByRef iWriteCount As Integer, ByVal pBuffer As String, ByRef iLen As Integer) As Integer

'1.50
Declare Function hisGetCriticalIllnessID Lib "cshis.dll" (ByVal pPatientID As String, ByVal pPatientBirthDate As String, ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer

'1.52 
Declare Function csSoftwareReset Lib "cshis.dll" (ByVal iType As Long) As Integer
' 2.1 安全模組認證
Declare Function csVerifySAMDC Lib "cshis.dll" () As Integer
' 2.2 
Declare Function csGetHospID Lib "cshis.dll" (ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer

' 3.1 資料上傳
Declare Function csUploadData Lib "cshis.dll" (ByVal pUploadFileName As String, ByVal fFileSize As String, ByVal pNumber As String, ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer
' 4.1 取得醫事人員卡狀態
Declare Function hpcGetHPCStatus Lib "cshis.dll" (ByVal Req As Integer, ByRef Status As Integer) As Integer
' 4.2 檢查醫事人員卡之PIN值
Declare Function hpcVerifyHPCPIN Lib "cshis.dll" () As Integer
' 4.3 輸入新的醫事人員卡之PIN值
Declare Function hpcInputHPCPIN Lib "cshis.dll" () As Integer
' 4.4 解開鎖住的醫事人員卡
Declare Function hpcUnlockHPC Lib "cshis.dll" () As Integer
' 4.5 取得醫事人員卡序號
Declare Function hpcGetHPCSN Lib "cshis.dll" (ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer
' 4.6 取得醫事人員卡身份證字號
Declare Function hpcGetHPCSSN Lib "cshis.dll" (ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer
' 4.7 取得醫事人員卡中文姓名
Declare Function hpcGetHPCCNAME Lib "cshis.dll" (ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer
' 4.8 取得醫事人員卡英文姓名
Declare Function hpcGetHPCENAME Lib "cshis.dll" (ByVal pBuffer As String, ByRef iBufferLen As Integer) As Integer
                 
' 5.1 進行疾病診斷碼押碼
Declare Function hisGetICD10EnC Lib "cshis.dll" (ByVal pIN As String, ByVal pOUT As String) As Integer
' 5.2 進行疾病診斷碼解押碼
Declare Function hisGetICD10DeC Lib "cshis.dll" (ByVal pIN As String, ByVal pOUT As String) As Integer

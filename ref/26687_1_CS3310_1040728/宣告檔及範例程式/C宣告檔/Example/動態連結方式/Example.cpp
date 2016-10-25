/*
*	Sample by Robin.
*   本範例為讀取掛號或報到時之基本資料
*/

#include <windows.h>
#include <stdlib.h>
#include <stdio.h>
#include <memory.h>

typedef int (WINAPI* LP0)();
typedef int (WINAPI* LP1)(char);
typedef int (WINAPI* LP2)(char *, int *);

void main()
{
	HINSTANCE hDll = NULL;
	char pBuffer[200], tmpMessage[100] ;
	int iBufferLen, res ;
	LP0 CloseCom;
	LP1 OpenCom;
	LP2 GetRegisterBasic;
	
	hDll = LoadLibrary("cshis.dll");           //載入 cshis.dll檔
	if(hDll == NULL)
	{
	   printf("Can't open cshis.dll\n") ;
	   exit(0);
	}
	OpenCom = (LP1)GetProcAddress(hDll,"csOpenCom");  // 準備開啟讀卡機連接PC之COM 埠
	if(OpenCom == NULL)
	{
		FreeLibrary(hDll);
		exit(0);
	}
    res = OpenCom(0);                          // 0:COM1, 1:COM2, ....
	if (res !=0)
	{
		printf("Open Com Port Error! \n") ;
		FreeLibrary(hDll);
		exit(0);
	}

	GetRegisterBasic = (LP2)GetProcAddress(hDll,"hisGetRegisterBasic");  //準備讀取掛號報到時之基本資料
	if(GetRegisterBasic == NULL)
	{
		FreeLibrary(hDll);
		exit(0);
	}

	iBufferLen = 78 ;                          // 回傳長度共78 Bytes
	res = GetRegisterBasic(pBuffer, &iBufferLen);
	if(res == 0)                               // 表成功
	{
	    memcpy(tmpMessage, pBuffer, 12) ;      //卡片號碼(12)
	    tmpMessage[12] = '\0' ;
	    printf("卡片號碼:%s\n", tmpMessage) ;
	    memcpy(tmpMessage, pBuffer + 12, 20) ; //姓名 (20)
	    tmpMessage[20] = '\0' ;
	    printf("姓名:%s\n", tmpMessage) ;
	    memcpy(tmpMessage, pBuffer + 32, 10) ; //身分證號 (10)
	    tmpMessage[10] = '\0' ;
	    printf("身分證號:%s\n", tmpMessage) ;
	    memcpy(tmpMessage, pBuffer + 42, 7) ;  //出生日期 (7)
	    tmpMessage[7] = '\0' ;
	    printf("出生日期:%s\n", tmpMessage) ;
	    memcpy(tmpMessage, pBuffer + 49, 1) ;  //性別 (1)
	    tmpMessage[1] = '\0' ;
	    printf("性別:%s\n", tmpMessage) ;
	    memcpy(tmpMessage, pBuffer + 50, 7) ;  //發卡日期 (7)
	    tmpMessage[7] = '\0' ;
	    printf("發卡日期:%s\n", tmpMessage) ;
	    memcpy(tmpMessage, pBuffer + 57, 1) ;  //卡片註銷註記 (1)
	    tmpMessage[1] = '\0' ;
	    printf("卡片註銷註記:%s\n", tmpMessage) ;
	    memcpy(tmpMessage, pBuffer + 58, 2) ;  //保險人代碼 (2)
	    tmpMessage[2] = '\0' ;
	    printf("保險人代碼:%s\n", tmpMessage) ;
	    memcpy(tmpMessage, pBuffer + 60, 1) ;  //保險對象身分註記 (1)
	    tmpMessage[1] = '\0' ;
	    printf("保險對象身分註記:%s\n", tmpMessage) ;
	    memcpy(tmpMessage, pBuffer + 61, 7) ;  //卡片有效期限 (7)
	    tmpMessage[7] = '\0' ;
	    printf("卡片有效期:%s\n", tmpMessage) ;
	    memcpy(tmpMessage, pBuffer + 68, 2) ;  //就醫可用次數 (2)
	    tmpMessage[2] = '\0' ;
	    printf("就醫可用次數:%s\n", tmpMessage) ;
	    memcpy(tmpMessage, pBuffer + 70, 7) ;  //新生兒出生日期 (7)
	    tmpMessage[7] = '\0' ;
	    printf("新生兒出生日期:%s\n", tmpMessage) ;
	    memcpy(tmpMessage, pBuffer + 77, 1) ;  //新生兒胞胎註記 (1)
	    tmpMessage[1] = '\0' ;
	    printf("新生兒胞胎註記:%s\n", tmpMessage) ;
	   	
	}
	else
	{
		printf("Read failuer\n");
	}
	CloseCom = (LP0)GetProcAddress(hDll,"csCloseCom");  //準備關閉COM埠
	if(CloseCom == NULL)
	{
		FreeLibrary(hDll);
		exit(0);
	}
    res = CloseCom();
	
	FreeLibrary(hDll);
}

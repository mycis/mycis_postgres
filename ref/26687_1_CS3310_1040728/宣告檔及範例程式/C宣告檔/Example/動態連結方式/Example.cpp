/*
*	Sample by Robin.
*   ���d�Ҭ�Ū�������γ���ɤ��򥻸��
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
	
	hDll = LoadLibrary("cshis.dll");           //���J cshis.dll��
	if(hDll == NULL)
	{
	   printf("Can't open cshis.dll\n") ;
	   exit(0);
	}
	OpenCom = (LP1)GetProcAddress(hDll,"csOpenCom");  // �ǳƶ}��Ū�d���s��PC��COM ��
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

	GetRegisterBasic = (LP2)GetProcAddress(hDll,"hisGetRegisterBasic");  //�ǳ�Ū����������ɤ��򥻸��
	if(GetRegisterBasic == NULL)
	{
		FreeLibrary(hDll);
		exit(0);
	}

	iBufferLen = 78 ;                          // �^�Ǫ��צ@78 Bytes
	res = GetRegisterBasic(pBuffer, &iBufferLen);
	if(res == 0)                               // ���\
	{
	    memcpy(tmpMessage, pBuffer, 12) ;      //�d�����X(12)
	    tmpMessage[12] = '\0' ;
	    printf("�d�����X:%s\n", tmpMessage) ;
	    memcpy(tmpMessage, pBuffer + 12, 20) ; //�m�W (20)
	    tmpMessage[20] = '\0' ;
	    printf("�m�W:%s\n", tmpMessage) ;
	    memcpy(tmpMessage, pBuffer + 32, 10) ; //�����Ҹ� (10)
	    tmpMessage[10] = '\0' ;
	    printf("�����Ҹ�:%s\n", tmpMessage) ;
	    memcpy(tmpMessage, pBuffer + 42, 7) ;  //�X�ͤ�� (7)
	    tmpMessage[7] = '\0' ;
	    printf("�X�ͤ��:%s\n", tmpMessage) ;
	    memcpy(tmpMessage, pBuffer + 49, 1) ;  //�ʧO (1)
	    tmpMessage[1] = '\0' ;
	    printf("�ʧO:%s\n", tmpMessage) ;
	    memcpy(tmpMessage, pBuffer + 50, 7) ;  //�o�d��� (7)
	    tmpMessage[7] = '\0' ;
	    printf("�o�d���:%s\n", tmpMessage) ;
	    memcpy(tmpMessage, pBuffer + 57, 1) ;  //�d�����P���O (1)
	    tmpMessage[1] = '\0' ;
	    printf("�d�����P���O:%s\n", tmpMessage) ;
	    memcpy(tmpMessage, pBuffer + 58, 2) ;  //�O�I�H�N�X (2)
	    tmpMessage[2] = '\0' ;
	    printf("�O�I�H�N�X:%s\n", tmpMessage) ;
	    memcpy(tmpMessage, pBuffer + 60, 1) ;  //�O�I��H�������O (1)
	    tmpMessage[1] = '\0' ;
	    printf("�O�I��H�������O:%s\n", tmpMessage) ;
	    memcpy(tmpMessage, pBuffer + 61, 7) ;  //�d�����Ĵ��� (7)
	    tmpMessage[7] = '\0' ;
	    printf("�d�����Ĵ�:%s\n", tmpMessage) ;
	    memcpy(tmpMessage, pBuffer + 68, 2) ;  //�N��i�Φ��� (2)
	    tmpMessage[2] = '\0' ;
	    printf("�N��i�Φ���:%s\n", tmpMessage) ;
	    memcpy(tmpMessage, pBuffer + 70, 7) ;  //�s�ͨ�X�ͤ�� (7)
	    tmpMessage[7] = '\0' ;
	    printf("�s�ͨ�X�ͤ��:%s\n", tmpMessage) ;
	    memcpy(tmpMessage, pBuffer + 77, 1) ;  //�s�ͨ�M�L���O (1)
	    tmpMessage[1] = '\0' ;
	    printf("�s�ͨ�M�L���O:%s\n", tmpMessage) ;
	   	
	}
	else
	{
		printf("Read failuer\n");
	}
	CloseCom = (LP0)GetProcAddress(hDll,"csCloseCom");  //�ǳ�����COM��
	if(CloseCom == NULL)
	{
		FreeLibrary(hDll);
		exit(0);
	}
    res = CloseCom();
	
	FreeLibrary(hDll);
}

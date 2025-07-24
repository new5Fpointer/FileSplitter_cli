
@echo off
setlocal
set "DIR=%~dp0"
set "OUT=%DIR%test_out"
set "EXE=%DIR%FileSplitter_cli.exe"

echo ===== FileSplitter CLI �Զ����� =====
if exist "%OUT%" rd /s /q "%OUT%"
md "%OUT%"

rem 1) ���ַ�
echo 1) ���ַ� utf8.txt ÿ 10000 �ֽ�
"%EXE%" -i "%DIR%utf8.txt" -o "%OUT%\chars" -m chars -s 10000
echo.

rem 2) ����
echo 2) ���� gbk.txt ÿ 500 ��
"%EXE%" -i "%DIR%gbk.txt" -o "%OUT%\lines" -m lines -s 500
echo.

rem 3) ������
echo 3) ������ utf8.txt �ֳ� 4 ��
"%EXE%" -i "%DIR%utf8.txt" -o "%OUT%\parts" -m parts -s 4
echo.

rem 4) ������
echo 4) ������ regex.txt �� ^##  �ָ�
"%EXE%" -i "%DIR%regex.txt" -o "%OUT%\regex" -m regex --regex "^## " --include-delimiter
echo.

echo ===== ������� =====
echo ����鿴: %OUT%

rem ---- ���㲢��ӡ�������� ----
powershell -NoProfile -Command ^
  "Write-Host '����������' -ForegroundColor Green; " ^
  "Write-Host ('utf8.txt �ַ�ģʽ 10000  : {0} ��' -f [math]::Ceiling((Get-Item '%DIR%utf8.txt').Length / 10000)); " ^
  "Write-Host ('gbk.txt   ��ģʽ 500��   : {0} ��' -f [math]::Ceiling((Get-Content '%DIR%gbk.txt' | Measure-Object -Line).Lines / 500)); " ^
  "Write-Host ('utf8.txt ����ģʽ 4��    : 4 ��'); " ^
  "Write-Host ('regex.txt ����ģʽ      : 3 ��')"

pause
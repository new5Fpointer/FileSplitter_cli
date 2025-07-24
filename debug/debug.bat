
@echo off
setlocal
set "DIR=%~dp0"
set "OUT=%DIR%test_out"
set "EXE=%DIR%FileSplitter_cli.exe"

echo ===== FileSplitter CLI 自动测试 =====
if exist "%OUT%" rd /s /q "%OUT%"
md "%OUT%"

rem 1) 按字符
echo 1) 按字符 utf8.txt 每 10000 字节
"%EXE%" -i "%DIR%utf8.txt" -o "%OUT%\chars" -m chars -s 10000
echo.

rem 2) 按行
echo 2) 按行 gbk.txt 每 500 行
"%EXE%" -i "%DIR%gbk.txt" -o "%OUT%\lines" -m lines -s 500
echo.

rem 3) 按份数
echo 3) 按份数 utf8.txt 分成 4 份
"%EXE%" -i "%DIR%utf8.txt" -o "%OUT%\parts" -m parts -s 4
echo.

rem 4) 按正则
echo 4) 按正则 regex.txt 按 ^##  分割
"%EXE%" -i "%DIR%regex.txt" -o "%OUT%\regex" -m regex --regex "^## " --include-delimiter
echo.

echo ===== 测试完成 =====
echo 结果查看: %OUT%

rem ---- 计算并打印期望份数 ----
powershell -NoProfile -Command ^
  "Write-Host '期望份数：' -ForegroundColor Green; " ^
  "Write-Host ('utf8.txt 字符模式 10000  : {0} 份' -f [math]::Ceiling((Get-Item '%DIR%utf8.txt').Length / 10000)); " ^
  "Write-Host ('gbk.txt   行模式 500行   : {0} 份' -f [math]::Ceiling((Get-Content '%DIR%gbk.txt' | Measure-Object -Line).Lines / 500)); " ^
  "Write-Host ('utf8.txt 份数模式 4份    : 4 份'); " ^
  "Write-Host ('regex.txt 正则模式      : 3 份')"

pause
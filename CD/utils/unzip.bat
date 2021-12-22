@echo off

set src=%1
set dst=%2
set server=%3

psexec -i -s -d \\%server% -u Administrator -p D3lft3chparkZuidH0llandNL powershell "Expand-Archive -LiteralPath %src% -DestinationPath %dst% "

exit
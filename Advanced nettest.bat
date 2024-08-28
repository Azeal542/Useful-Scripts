@echo off
set logfile=output.txt

ipconfig /all >> %logfile%

echo. >> %logfile%
ping kfvpn.oit.edu >> %logfile%

echo. >> %logfile%
nslookup kfvpn.oit.edu >> %logfile%

echo. >> %logfile%
for /f "tokens=1* delims=: " %%A in (
  'nslookup myip.opendns.com. resolver1.opendns.com 2^>NUL^|find "Address:"'
) Do set ExtIP=%%B
echo External IP is : %ExtIP% >> %logfile%

echo. >> %logfile%
echo Done!
pause
@echo off
set logfile=output.txt
 
ipconfig /all >> %logfile%
 
echo. >> %logfile%
ping google.com >> %logfile%
 
echo. >> %logfile%
nslookup google.com >> %logfile%
 
echo. >> %logfile%
echo Done!
pause
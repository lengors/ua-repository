@echo off
where /r . %1 > temp
set /p VAR=<temp
del temp
set _tail=%*
call set _tail=%%_tail:*%1=%%
call %VAR% %_tail%
@echo off
if "%~1"=="" (vendor\premake\windows\premake5.exe vs2019) else (vendor\premake\windows\premake5.exe %1)
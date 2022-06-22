@echo off
REM closes all VLC instances
wmic process where name='vlc.exe' delete
@echo off
REM	____________________________________
REM |DISPLAY |DISPLAY |DISPLAY |DISPLAY |
REM	|___10__ |___11___|___8____|___9____|
REM	|DISPLAY |DISPLAY |DISPLAY |DISPLAY |
REM	|   5    |    6   |   7    |   4    |
REM	____________________________________
REM |DISPLAY |DISPLAY |DISPLAY |DISPLAY |
REM	|___5____|___7____|___8____|___1____|
REM	|DISPLAY |DISPLAY |DISPLAY |DISPLAY |
REM	|   3    |    6   |   4    |   2    |


START "VLC media player - Instance" "%PROGRAMFILES%\VideoLAN\VLC\vlc.exe" %1 --fullscreen -R  --no-qt-privacy-ask --video-on-top --video-title-timeout=500 --qt-fullscreen-screennumber=%2 --no-qt-fs-controller --qt-auto-raise=0 --crop=16:9 --no-crashdump
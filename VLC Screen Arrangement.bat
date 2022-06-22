@echo off
REM	____________________________________
REM |DISPLAY |DISPLAY |DISPLAY |DISPLAY |
REM	|___10__ |___11___|___4____|___9____|
REM	|DISPLAY |DISPLAY |DISPLAY |DISPLAY |
REM	|   5    |    6   |   7    |   8    |
REM


START "VLC media player - Instance" "%PROGRAMFILES%\VideoLAN\VLC\vlc.exe" %1 --fullscreen -R  --no-qt-privacy-ask --video-on-top --video-title-timeout=500 --directx-device=%2 --no-embedded-video --no-qt-fs-controller --qt-auto-raise=0 --crop=16:9 --no-crashdump
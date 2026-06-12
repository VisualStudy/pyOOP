@echo off
title Aden's Needle Trial v6.2 Stable
py -m pip install pygame
py main.py
if exist error_log.txt (
    echo.
    echo error_log.txt was created. Please check it if the game closed unexpectedly.
)
pause

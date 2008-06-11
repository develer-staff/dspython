@echo off
REM rate: -r rate (samples per second eg. 11025, 44100)
REM data size: -b (8-bit), -w (16-bit)
REM data enconding: -a (ADPCM), signed linear (-s), GSM (-g)
REM channels: -c 1 (mono), -c 2 (stereo)
REM --------------------------------------------------------
ECHO %1 %2
sox -V %1 -r11025 -b -s -c 1 %2

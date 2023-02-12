@echo off
setlocal enabledelayedexpansion
set files=knightthrough_5x5.gdl knightthrough_6x6.gdl knightthrough_7x7.gdl knightthrough_8x8.gdl knightthrough_9x9.gdl knightthrough_10x10.gdl

for %%f in (%files%) do (
    java -jar gamecontroller-cli.jar testmatch %%f 10 10 1 -remote 1 Player1 localhost 4001 1 -remote 2 Player2 localhost 5001 1
)
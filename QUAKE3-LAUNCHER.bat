@ECHO OFF
CLS
COLOR 4E

cd bin\

FOR /F "tokens=* USEBACKQ" %%F IN (`findstr /C:"seta name" %APPDATA%\Quake3\baseq3\q3config.cfg`) DO (
    SET name_cmd=%%F
)

SET name=%name_cmd:~11,-1%

GOTO Menu

:Menu
TYPE banner.txt

if exist baseq3\fancy_graphics.cfg (
    SET gfx_mode=Fancy Graphics
) else (
    SET gfx_mode=Pretty Good Graphics
)

ECHO Current player name: %name%
ECHO Current graphics mode: %gfx_mode%

ECHO.

ECHO 1. Launch Quake 3
ECHO 2. Change player name
ECHO 3. Enable FANCY GRAPHICS mode
ECHO 4. Enable PRETTY GOOD GRAPHICS mode
ECHO 5. Generate randomized server.cfg (requires python3)
ECHO 6. Launch dedicated server
ECHO 7. Exit

ECHO.

CHOICE /C 1234567 /M "Enter your choice:"

:: Note - list ERRORLEVELS in decreasing order
IF ERRORLEVEL 7 GOTO End
IF ERRORLEVEL 6 GOTO LaunchServer
IF ERRORLEVEL 5 GOTO RandomizeServerCfg
IF ERRORLEVEL 4 GOTO PGGraphics
IF ERRORLEVEL 3 GOTO FancyGraphics
IF ERRORLEVEL 2 GOTO Name
IF ERRORLEVEL 1 GOTO LaunchGame

:Name
set /p name= Enter Player Name: 
GOTO Menu

:FancyGraphics
move baseq3\fancy_graphics.cfg_DISABLED baseq3\fancy_graphics.cfg
GOTO Menu

:PGGraphics
move baseq3\fancy_graphics.cfg baseq3\fancy_graphics.cfg_DISABLED
GOTO Menu

:RandomizeServerCfg
python3 build_server_cfg.py

:LaunchServer
start ioq3ded.x86_64.exe +exec server.cfg +set sv_dedicated 1
GOTO End

:LaunchGame
start ioquake3.x86_64.exe ^
 +seta name %name%
GOTO End

:End

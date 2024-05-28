@echo off
set mgit="%~dp0\REQUIRED_BY_INSTALLER_UPDATER\cmd\git.exe"
echo Current directory: %CD%
:: git init .
:: git remote add origin "https://github.com/NoamRothschild/infinitefusion-multiplayer.git"
:: git fetch origin releases
:: git reset --hard origin/releases
%mgit% clone "https://github.com/NoamRothschild/infinitefusion-multiplayer.git"

echo Done Installing Project!
pause
exit

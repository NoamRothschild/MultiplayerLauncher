@echo off
set mgit="%~dp0\REQUIRED_BY_INSTALLER_UPDATER\cmd\git.exe"
echo Current directory: %CD%

if not exist ".\infinitefusion-multiplayer" (
    echo Cloning the repository...
    %mgit% clone "https://github.com/NoamRothschild/infinitefusion-multiplayer.git"
) else (
    echo Updating the repository...
    cd infinitefusion-multiplayer
    %mgit% pull
    cd ..
)



echo Done Installing Project!
pause
exit

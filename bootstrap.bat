@echo off
echo Bumping version...
python bump_version.py --patch-only

echo Building executable...
pyinstaller RetroForge.spec --clean -y

if %ERRORLEVEL% NEQ 0 (
    echo Build failed.
    exit /b %ERRORLEVEL%
)

set /p VERSION=<VERSION
echo Build successful for %VERSION%.

echo Committing to Git...
git add .
git commit -m "Build %VERSION%"
git push
git tag "%VERSION%"
git push --tags

echo Done!

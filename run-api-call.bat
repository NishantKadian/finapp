@echo off
echo Attempting to run Python script...

REM Try common Python installation paths
set PYTHON_PATHS=python python3 py C:\Python311\python.exe C:\Python310\python.exe C:\Python39\python.exe C:\Users\kadiann\AppData\Local\Programs\Python\Python311\python.exe

for %%p in (%PYTHON_PATHS%) do (
    echo Trying: %%p
    %%p -c "import sys; print('Python found:', sys.executable)" > nul 2>&1
    if not errorlevel 1 (
        echo Python found: %%p
        %%p "c:\Users\kadiann\nk-worskpace\finapp\api-call.py"
        goto :eof
    )
)

echo Python not found in common locations.
echo Please install Python or provide the full path to your Python executable.
echo.
echo You can run your script by directly specifying the Python path:
echo [full-path-to-python] c:\Users\kadiann\nk-worskpace\finapp\api-call.py
echo.
echo For example:
echo C:\Users\kadiann\AppData\Local\Programs\Python\Python311\python.exe c:\Users\kadiann\nk-worskpace\finapp\api-call.py

pause

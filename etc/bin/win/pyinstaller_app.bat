cd ..\..\..\

rm -R build
rm -R dist

"%APPDATA%\Python\Python35\Scripts\pyinstaller.exe" ^
 --onefile ^
 --windowed ^
 --icon etc\bin\win\icon.ico ^
 --paths C:\%HOMEPATH%\AppData\Roaming\Python\Python35\site-packages\PyQt5 ^
 etc\bin\unix\alignak-app.py

pause

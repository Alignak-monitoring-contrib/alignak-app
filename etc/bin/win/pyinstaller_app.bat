cd ..\..\..\

rm -R build
rm -R dist

"%APPDATA%\Python\Python35\Scripts\pyinstaller.exe" ^
 --name alignak-app ^
 --onefile ^
 --windowed ^
 --icon etc\bin\win\icon.ico ^
 --paths C:\%HOMEPATH%\AppData\Roaming\Python\Python35\site-packages\PyQt5\Qt\bin ^
 --paths D:\INSTALL\alignak-app\alignak_app ^
 etc\bin\unix\alignak-app.py

pause

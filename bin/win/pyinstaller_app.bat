cd ..\..

rm -R build
rm -R dist

"%APPDATA%\Python\Python35\Scripts\pyinstaller.exe" ^
 --name alignak-app ^
 --onefile ^
 --windowed ^
 --icon bin\win\icon.ico ^
 --paths C:\%HOMEPATH%\AppData\Roaming\Python\Python35\site-packages\PyQt5\Qt\bin ^
 --paths D:\Repos\alignak-app\alignak_app ^
 bin\unix\alignak-app.py

cd bin\win
pause

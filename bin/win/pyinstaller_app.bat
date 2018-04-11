:: Copyright (c) 2015-2018:
::   Matthieu Estrada, ttamalfor@gmail.com
::
:: This file is part of (AlignakApp).
::
:: (AlignakApp) is free software: you can redistribute it and/or modify
:: it under the terms of the GNU Affero General Public License as published by
:: the Free Software Foundation, either version 3 of the License, or
:: (at your option) any later version.
::
:: (AlignakApp) is distributed in the hope that it will be useful,
:: but WITHOUT ANY WARRANTY; without even the implied warranty of
:: MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
:: GNU Affero General Public License for more details.
::
:: You should have received a copy of the GNU Affero General Public License
:: along with (AlignakApp).  If not, see <http://www.gnu.org/licenses/>.

cd ..\..

rm -R build
rm -R dist

"%APPDATA%\Python\Python35\Scripts\pyinstaller.exe" ^
 --name alignak-app ^
 --onefile ^
 --windowed ^
 --icon bin\win\icon_64.ico ^
 --paths C:\%HOMEPATH%\AppData\Roaming\Python\Python35\site-packages\PyQt5\Qt\bin ^
 --paths C:\%HOMEPATH%\AppData\Roaming\Python\Python35\site-packages\PyQt5\Qt\plugins ^
 --paths D:\Repos\alignak-app\alignak_app ^
 alignak_app\app.py

cd bin\win
pause

; INNO SETUP FILE
; Copyright (c) 2015-2017:
;   Matthieu Estrada, ttamalfor@gmail.com
;
; This file is part of (AlignakApp).
;
; (AlignakApp) is free software: you can redistribute it and/or modify
; it under the terms of the GNU Affero General Public License as published by
; the Free Software Foundation, either version 3 of the License, or
; (at your option) any later version.
;
; (AlignakApp) is distributed in the hope that it will be useful,
; but WITHOUT ANY WARRANTY; without even the implied warranty of
; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
; GNU Affero General Public License for more details.
;
; You should have received a copy of the GNU Affero General Public License
; along with (AlignakApp).  If not, see <http://www.gnu.org/licenses/>.

#define MyAppName "Alignak-app"
#define ShortVersion "0.6"
#define MinorVersion ".5"
#define MyAppVersion ShortVersion + MinorVersion
#define MyAppPublisher "Alignak (Estrada Matthieu)"
#define MyAppURL "https://github.com/Alignak-monitoring-contrib/alignak-app"
#define MyAppExeName "alignak-app.exe"
#define RootApp "D:\Repos"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{18B7B0EE-1FBA-4375-9236-8575674AB45B}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableDirPage=yes
LicenseFile={#RootApp}\alignak-app\LICENSE
OutputDir={#RootApp}\alignak-app\dist\setup
OutputBaseFilename=Setup {#MyAppName} {#MyAppVersion}-x64
SetupIconFile={#RootApp}\alignak-app\bin\win\icon_64.ico
UninstallDisplayIcon={app}\icon_64.ico
Compression=lzma
SolidCompression=yes
WizardImageFile={#RootApp}\alignak-app\bin\win\Wizard_App.bmp
WizardSmallImageFile={#RootApp}\alignak-app\bin\win\SmallWizard_App.bmp
ArchitecturesInstallIn64BitMode=x64
ArchitecturesAllowed=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"
Name: "german"; MessagesFile: "compiler:Languages\German.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}";

[Files]
Source: "{#RootApp}\alignak-app\dist\alignak-app.exe"; DestDir: "{app}"; Flags: ignoreversion; Permissions: users-full admins-full everyone-modify;
Source: "{#RootApp}\alignak-app\etc\css\*"; DestDir: "{app}\css"; Flags: ignoreversion; Permissions: users-full admins-full everyone-modify;
Source: "{#RootApp}\alignak-app\etc\images\*"; DestDir: "{app}\images"; Flags: ignoreversion; Permissions: users-full admins-full everyone-modify;
Source: "{#RootApp}\alignak-app\etc\settings.cfg"; DestDir: "{app}"; Flags: ignoreversion; Permissions: users-full admins-full everyone-modify;
Source: "{#RootApp}\alignak-app\etc\app_workdir.ini"; DestDir: "{app}"; Flags: ignoreversion isreadme; Permissions: users-full admins-full everyone-modify;
Source: "{#RootApp}\alignak-app\bin\win\vc_redist.x64.exe"; DestDir: {tmp}; Flags: deleteafterinstall;
Source: "{#RootApp}\alignak-app\bin\win\icon_64.ico"; DestDir: {app}; Flags: ignoreversion; Permissions: users-full admins-full everyone-modify;

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\icon_64.ico";
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\icon_64.ico"; Tasks: desktopicon

[Run]
Filename: "{cmd}"; Parameters: "/c icacls ""{app}"" /grant Everyone:(OI)(CI)F /T"; StatusMsg: Grant permissions; Languages: english;
Filename: "{cmd}"; Parameters: "/c icacls ""{app}"" /grant ""Tout le monde"":(OI)(CI)F /T"; StatusMsg: Grant permissions; Languages: french;
Filename: {tmp}\vc_redist.x64.exe; Parameters: "/q /passive /Q:a /c:""msiexec /q /i vcredist.msi"" "; Check: IsWin64; StatusMsg: Installing VC++ 64bits Redistributables...
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent unchecked

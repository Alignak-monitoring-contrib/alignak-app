; Script generated by the Inno Script Studio Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "Alignak-app"
#define ShortVersion "0.5"
#define MyAppVersion ShortVersion + ".1"
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
LicenseFile={#RootApp}\alignak-app\LICENSE
OutputDir={#RootApp}\alignak-app\dist\setup
OutputBaseFilename=Setup {#MyAppName} {#MyAppVersion}-x64-BETA
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
Source: "{#RootApp}\alignak-app\dist\alignak-app.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#RootApp}\alignak-app\etc\css\*"; DestDir: "{userappdata}\Python\alignak_app\css"; Flags: ignoreversion
Source: "{#RootApp}\alignak-app\etc\images\*"; DestDir: "{userappdata}\Python\alignak_app\images"; Flags: ignoreversion
Source: "{#RootApp}\alignak-app\etc\settings.cfg"; DestDir: "{app}"; Flags: ignoreversion; Permissions: everyone-full
Source: "{#RootApp}\alignak-app\bin\win\vc_redist.x64.exe"; DestDir: {tmp}; Flags: deleteafterinstall
Source: "{#RootApp}\alignak-app\bin\win\icon_64.ico"; DestDir: {app}; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName} v{#MyAppVersion}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\icon_64.ico";
Name: "{commondesktop}\{#MyAppName} v{#MyAppVersion}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\icon_64.ico"; Tasks: desktopicon

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    MsgBox(ExpandConstant(
      'Configuration file is located under folder'
      + #13#10 
      + ' [ {app} ] !' 
      + #13#10 
      + #13#10
      + 'For any assistance, please consult: https://github.com/Alignak-monitoring-contrib/alignak-app !'),
       mbInformation,
        MB_OK);
  end
end;

[Run]
Filename: {tmp}\vc_redist.x64.exe; Parameters: "/q /passive /Q:a /c:""msiexec /q /i vcredist.msi"" "; Check: IsWin64; StatusMsg: Installing VC++ 64bits Redistributables...
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent unchecked

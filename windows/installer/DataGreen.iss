#define MyAppName "DataGreen"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "DataGreen"
#define MyAppURL "http://127.0.0.1:8765"
; Raiz do repositório (pasta que contém backend/, dist/, windows/). ISPP: SourcePath = pasta do .iss.
#define RepoRoot SourcePath + "\..\.."

[Setup]
AppId={{A2F7EBDC-5A7E-4F99-9D04-1E4B8F03A4C8}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
DefaultDirName={autopf}\DataGreen
DefaultGroupName=DataGreen
DisableProgramGroupPage=yes
LicenseFile=
OutputDir={#RepoRoot}\release\installer
OutputBaseFilename=DataGreen_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog
UninstallDisplayIcon={app}\2-INICIAR-DATAGREEN.bat
SetupIconFile=

[Languages]
Name: "portuguesebrazil"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na área de trabalho"; GroupDescription: "Atalhos:"; Flags: unchecked

[Files]
Source: "{#RepoRoot}\1-INSTALAR-PRIMEIRA-VEZ.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#RepoRoot}\2-INICIAR-DATAGREEN.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#RepoRoot}\3-BACKUP-MANUAL.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#RepoRoot}\4-TROCAR-SENHA.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#RepoRoot}\LEIA-ME-PRIMEIRO.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#RepoRoot}\windows\*"; DestDir: "{app}\windows"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#RepoRoot}\backend\*"; DestDir: "{app}\backend"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#RepoRoot}\dist\public\*"; DestDir: "{app}\dist\public"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#RepoRoot}\Manuais\*"; DestDir: "{app}\Manuais"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\DataGreen"; Filename: "{app}\2-INICIAR-DATAGREEN.bat"; WorkingDir: "{app}"
Name: "{group}\DataGreen - primeira configuração"; Filename: "{app}\1-INSTALAR-PRIMEIRA-VEZ.bat"; WorkingDir: "{app}"
Name: "{group}\Backup manual"; Filename: "{app}\3-BACKUP-MANUAL.bat"; WorkingDir: "{app}"
Name: "{group}\Trocar senha"; Filename: "{app}\4-TROCAR-SENHA.bat"; WorkingDir: "{app}"
Name: "{group}\Desinstalar DataGreen"; Filename: "{uninstallexe}"
Name: "{autodesktop}\DataGreen"; Filename: "{app}\2-INICIAR-DATAGREEN.bat"; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
Filename: "{app}\1-INSTALAR-PRIMEIRA-VEZ.bat"; Description: "Executar primeira configuração agora (recomendado)"; Flags: nowait postinstall skipifsilent
Filename: "{app}\2-INICIAR-DATAGREEN.bat"; Description: "Iniciar DataGreen agora"; Flags: nowait postinstall skipifsilent unchecked

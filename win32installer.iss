[Setup]
AppName=Parrot Zik Tray
AppVerName=Parrot Zik Tray 0.3
AppPublisher=m0sia@m0sia.ru
AppPublisherURL=https://github.com/m0sia/pyParrotZik
DefaultDirName={pf}\ParrotZikTray
DefaultGroupName=ParrotZikTray
DisableProgramGroupPage=true
OutputBaseFilename=pyParrotZik-win32-installer
Compression=lzma
SolidCompression=true
AllowUNCPath=false
VersionInfoVersion=0.3
VersionInfoCompany=m0sia
VersionInfoDescription=ParrotZikTray
;PrivilegeRequired=admin

[Dirs]
Name: {app}; Flags: uninsalwaysuninstall;

[Files]
Source: dist\*; DestDir: {app}; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: {group}\Parrot Zik Tray; Filename: {app}\ParrotZikTray.exe; WorkingDir: {app}

[Run]
; If you are using GTK's built-in SVG support, uncomment the following line.
;Filename: {cmd}; WorkingDir: "{app}"; Parameters: "/C gdk-pixbuf-query-loaders.exe > lib/gdk-pixbuf-2.0/2.10.0/loaders.cache"; Description: "GDK Pixbuf Loader Cache Update"; Flags: nowait runhidden
Filename: {app}\ParrotZikTray.exe; Description: {cm:LaunchProgram,Parrot Zik Tray}; Flags: nowait postinstall skipifsilent

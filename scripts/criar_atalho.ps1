param(
    [Parameter(Mandatory = $true)][string]$InstallDir,
    [Parameter(Mandatory = $true)][string]$PythonExe,
    [string]$IconPath = ""
)

$ErrorActionPreference = "Stop"
$Desktop = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $Desktop "Simulador TRT4.lnk"
$Launcher = Join-Path $InstallDir "launcher.py"
$WScript = New-Object -ComObject WScript.Shell
$Shortcut = $WScript.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $PythonExe
$Shortcut.Arguments = "`"$Launcher`""
$Shortcut.WorkingDirectory = $InstallDir
$Shortcut.WindowStyle = 7
$Shortcut.Description = "Simulador TRT4 FCC - offline"
if ($IconPath -and (Test-Path $IconPath)) {
    $Shortcut.IconLocation = "$IconPath,0"
}
$Shortcut.Save()
Write-Output $ShortcutPath

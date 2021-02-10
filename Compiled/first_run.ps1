$principal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if($principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    $currentdir = $PSScriptRoot
    echo "Kopijuojami reikiami failai"
    Start-Sleep -s 1

try
{
    Copy-Item -Path "$currentdir\includes\avbin.dll" -Destination "C:\Windows\System32\avbin.dll" -Recurse
    Copy-Item -Path "$currentdir\includes\avbin64.dll" -Destination "C:\Windows\System32\avbin64.dll" -Recurse
    Copy-Item -Path "$currentdir\includes\libusb-1.0.dll" -Destination "C:\Windows\System32\libusb-1.0.dll" -Recurse
    Write-Host "Failai sėkmingai nukopijuoti"

}
catch
{
    Write-Host "Nutiko klaida keliant failus, pamėginkite dar kartą."
}
    Read-Host -Prompt "Failai nukopijuoti. Galite paleisti buzzer.exe iš  programa $currentdir"
}
else {
    Start-Process -FilePath "powershell" -ArgumentList "$('-File ""')$(Get-Location)$('\')$($MyInvocation.MyCommand.Name)$('""')" -Verb runAs
}

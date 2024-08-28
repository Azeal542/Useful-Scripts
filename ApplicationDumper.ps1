# This script requires administrative privileges to run
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Warning "This script must be run as an Administrator."
    Pause
    exit
}

#Grab the name of the file to be converted to PID
$name = Read-Host 'What is the name of the target process?'
$proc = Get-Process $name -ErrorAction SilentlyContinue | Select-Object Id,  ProcessName
$proclines = $proc | measure #(Get-Process $name | Select-Object Id,  ProcessName | Measure-Object -Line).Lines
$lines = $proclines.Count

if ($lines -gt 1) { 
    $proc | Format-Table -AutoSize | Out-Host    
    do {
        $selectedPid = Read-Host 'Please select a process ID from the list above'
        # Convert the input to an integer for comparison
        $selectedPid = [int]$selectedPid
        $validPid = Get-Process $name | Where-Object { $_.Id -eq $selectedPid }
        if ($validPid) {
            Write-Output "Valid PID selected: $selectedPid"
            break
        } else {
            Write-Output "Invalid PID, please select a valid process ID from the list."
        }
    } while ($true)
}
elseif ($lines -eq 1) {
    $selectedPid = $proc.Id
}
else {
    Write-Output "No process found with the name $name."
    $selectedPid = $null
}

# Set output folder and create it if it doesn't exist
$OutputFolder = "C:\ForensicOutput"
if (!(Test-Path $OutputFolder)) {
    New-Item -ItemType Directory -Force -Path $OutputFolder
}

# Download Sysinternals Suite if it doesn't exist
$SysinternalsPath = "C:\SysinternalsSuite"
if (!(Test-Path $SysinternalsPath)) {
    New-Item -ItemType Directory -Force -Path $SysinternalsPath
    Invoke-WebRequest -Uri "https://download.sysinternals.com/files/SysinternalsSuite.zip" -OutFile "$SysinternalsPath\SysinternalsSuite.zip"
    Expand-Archive -Path "$SysinternalsPath\SysinternalsSuite.zip" -DestinationPath $SysinternalsPath
}

# Capture memory using procdump
$ProcDumpPath = "$SysinternalsPath\procdump64.exe"
$MemoryDumpFile = "$OutputFolder\memorydump.raw"
& $ProcDumpPath -ma -accepteula $selectedPid $MemoryDumpFile

Write-Output "Memory capture completed."

param(
    [string]$Ref = "main"
)

$ErrorActionPreference = "Stop"
$SourceZipUrl = "https://github.com/samirhosninet/Hermes-Digital-Estate/archive/refs/heads/$Ref.zip"
$BootstrapRoot = Join-Path $env:LOCALAPPDATA "HermesDigitalState\bootstrap"
$RunId = "$(Get-Date -Format yyyyMMddHHmmss)-$([guid]::NewGuid().ToString('N'))"
$RunRoot = Join-Path $BootstrapRoot "runs\$RunId"
$DownloadPath = Join-Path $RunRoot "Hermes-Digital-Estate-$Ref.zip"
$ExtractRoot = Join-Path $RunRoot "extract"
$LogDir = Join-Path $env:TEMP "hermes-digital-state-bootstrap"
$LogPath = Join-Path $LogDir "install-windows.log"

New-Item -ItemType Directory -Force -Path $BootstrapRoot | Out-Null
New-Item -ItemType Directory -Force -Path $RunRoot | Out-Null
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

function Write-Step([string]$Message) {
    $line = "[$(Get-Date -Format o)] $Message"
    Write-Host $Message
    Add-Content -LiteralPath $LogPath -Value $line -Encoding UTF8
}

function Fail-WithLog([string]$Message) {
    Write-Step "FAILED: $Message"
    Write-Host ""
    Write-Host "Digital State bootstrap failed."
    Write-Host "Reason: $Message"
    Write-Host "Log: $LogPath"
    exit 1
}

try {
    Set-Content -LiteralPath $LogPath -Value "Digital State Windows bootstrap log" -Encoding UTF8
    Write-Step "Preparing bootstrap run directory: $RunRoot"
    New-Item -ItemType Directory -Force -Path $ExtractRoot | Out-Null

    Write-Step "Downloading Digital State bootstrap package from GitHub."
    Invoke-WebRequest -Uri $SourceZipUrl -OutFile $DownloadPath -UseBasicParsing

    Write-Step "Extracting package."
    Expand-Archive -LiteralPath $DownloadPath -DestinationPath $ExtractRoot -Force

    $startBat = Get-ChildItem -LiteralPath $ExtractRoot -Filter "START.bat" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
    if (-not $startBat) {
        Fail-WithLog "START.bat was not found in the downloaded package."
    }

    Write-Step "Launching local Digital State stack installer."
    $process = Start-Process -FilePath $startBat.FullName -WorkingDirectory $startBat.DirectoryName -PassThru
    Write-Step "START.bat launched with PID $($process.Id)."
    Write-Step "If anything fails, keep the launcher window open and review its log path."
} catch {
    Fail-WithLog $_.Exception.Message
}

param(
    [int]$Port = 8765
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Resolve-Path (Join-Path $ScriptDir "..\..")).Path
$UiPath = Join-Path $ScriptDir "bootstrap-ui.html"
$LogDir = Join-Path $env:TEMP "hermes-digital-state-bootstrap"
$WorkspaceRoot = Join-Path $env:LOCALAPPDATA "HermesDigitalState"
$WorkspaceDir = Join-Path $WorkspaceRoot "hermes-workspace"
$HermesRoot = Join-Path $env:LOCALAPPDATA "hermes"
$HermesCmdPath = Join-Path $HermesRoot "bin\hermes.cmd"
$DigitalStateSource = "github.com/samirhosninet/Hermes-Digital-Estate"
$WorkspaceSource = "https://github.com/outsourc-e/hermes-workspace.git"
$HermesInstallCommand = "irm https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.ps1 | iex"
$BootstrapNonce = [guid]::NewGuid().ToString("N")

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
New-Item -ItemType Directory -Force -Path $WorkspaceRoot | Out-Null

function Add-ProcessToolPaths {
    $candidateDirs = @(
        (Join-Path $HermesRoot "bin"),
        (Join-Path $HermesRoot "git\cmd"),
        (Join-Path $HermesRoot "git\bin"),
        (Join-Path $HermesRoot "git\usr\bin"),
        (Join-Path $HermesRoot "node"),
        (Join-Path $HermesRoot "node\bin"),
        (Join-Path $env:APPDATA "npm")
    )
    $existing = $env:PATH -split ";" | Where-Object { $_ }
    foreach ($dir in $candidateDirs) {
        if ((Test-Path -LiteralPath $dir) -and ($existing -notcontains $dir)) {
            $env:PATH = "$dir;$env:PATH"
        }
    }
}

function Find-Executable([string]$Name, [string[]]$KnownPaths = @()) {
    $cmd = Get-Command $Name -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    foreach ($path in $KnownPaths) {
        if (Test-Path -LiteralPath $path) { return $path }
    }
    return ""
}

function Find-Node {
    $node = Find-Executable "node" @(
        (Join-Path $HermesRoot "node\node.exe"),
        (Join-Path $HermesRoot "node\bin\node.exe")
    )
    if ($node) { return $node }
    $nodeRoot = Join-Path $HermesRoot "node"
    if (Test-Path -LiteralPath $nodeRoot) {
        $found = Get-ChildItem -LiteralPath $nodeRoot -Filter "node.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($found) { return $found.FullName }
    }
    return ""
}

function Get-HermesCommand {
    if (Test-Path -LiteralPath $HermesCmdPath) { return $HermesCmdPath }
    return Find-Executable "hermes" @()
}

function Get-GitCommand {
    return Find-Executable "git" @(
        (Join-Path $HermesRoot "git\cmd\git.exe"),
        (Join-Path $HermesRoot "git\bin\git.exe")
    )
}

function Get-NpmCommand {
    return Find-Executable "npm" @(
        (Join-Path $HermesRoot "node\npm.cmd"),
        (Join-Path $HermesRoot "node\bin\npm.cmd")
    )
}

function Get-PnpmCommand {
    return Find-Executable "pnpm" @(
        (Join-Path $env:APPDATA "npm\pnpm.cmd")
    )
}

function ConvertTo-JsonResponse($value) {
    return ($value | ConvertTo-Json -Depth 8 -Compress)
}

function Write-Response($Context, [int]$Status, [string]$Body, [string]$ContentType = "application/json; charset=utf-8") {
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($Body)
    $Context.Response.StatusCode = $Status
    $Context.Response.ContentType = $ContentType
    $Context.Response.Headers.Add("Cache-Control", "no-store")
    $Context.Response.ContentLength64 = $bytes.Length
    $Context.Response.OutputStream.Write($bytes, 0, $bytes.Length)
    $Context.Response.Close()
}

function Get-CommandVersion([string]$FileName, [string[]]$CommandArgs) {
    if (-not $FileName) { return "" }
    try {
        $output = & $FileName @CommandArgs 2>&1 | Select-Object -First 1
        if ($LASTEXITCODE -eq 0 -or $output) { return [string]$output }
    } catch {}
    return ""
}

function Test-Node22 {
    $node = Find-Node
    if (-not $node) { return $false }
    $version = Get-CommandVersion $node @("--version")
    if ($version -match "v(\d+)\.") { return ([int]$Matches[1] -ge 22) }
    return $false
}

function Test-DigitalStateProfile {
    $hermes = Get-HermesCommand
    if (-not $hermes) { return $false }
    try {
        $profiles = & $hermes profile list 2>&1
        return (($profiles -join "`n") -match "digital-state")
    } catch {
        return $false
    }
}

function Get-StackStatus {
    Add-ProcessToolPaths
    $hermes = Get-HermesCommand
    $git = Get-GitCommand
    $node = Find-Node
    $node22 = Test-Node22
    $pnpm = Get-PnpmCommand
    $workspace = Test-Path (Join-Path $WorkspaceDir "package.json")
    $profile = Test-DigitalStateProfile

    return [ordered]@{
        hermes = [ordered]@{
            status = $(if ($hermes) { "installed" } else { "missing" })
            detail = $(if ($hermes) { Get-CommandVersion $hermes @("--version") } else { "Hermes Agent is the first required component. Its Windows installer also provisions Python, Node.js 22, and PortableGit." })
            fix = $HermesInstallCommand
        }
        git = [ordered]@{
            status = $(if ($git) { "installed" } else { "missing" })
            detail = $(if ($git) { Get-CommandVersion $git @("--version") } else { "Git is checked after Hermes install. The official Hermes installer normally provisions PortableGit." })
            fix = "Install Hermes Agent first, then retry. If Git is still missing, rerun the Hermes installer."
        }
        node = [ordered]@{
            status = $(if ($node22) { "installed" } else { "missing" })
            detail = $(if ($node22) { Get-CommandVersion $node @("--version") } else { "Node.js 22+ is checked after Hermes install. The official Hermes installer normally provisions it." })
            fix = "Install Hermes Agent first, then retry. If Node is still missing, rerun the Hermes installer."
        }
        pnpm = [ordered]@{
            status = $(if ($pnpm) { "installed" } else { "missing" })
            detail = $(if ($pnpm) { Get-CommandVersion $pnpm @("--version") } else { "pnpm is installed with npm after Hermes makes Node available." })
            fix = "npm install -g pnpm"
        }
        workspace = [ordered]@{
            status = $(if ($workspace) { "installed" } else { "missing" })
            detail = $(if ($workspace) { $WorkspaceDir } else { "Hermes Workspace has not been cloned and installed yet." })
            fix = "git clone $WorkspaceSource"
        }
        digitalState = [ordered]@{
            status = $(if ($profile) { "installed" } else { "missing" })
            detail = $(if ($profile) { "Profile digital-state is installed." } else { "Digital State profile is not installed yet." })
            fix = "hermes profile install $DigitalStateSource --alias --yes"
        }
        paths = [ordered]@{
            logDir = $LogDir
            workspaceDir = $WorkspaceDir
            hermesCmd = $HermesCmdPath
        }
    }
}

function Invoke-FixedCommand($Name, [string]$FileName, [string[]]$Arguments, [string]$WorkingDirectory = $RepoRoot) {
    $logPath = Join-Path $LogDir "$Name.log"
    $outPath = Join-Path $LogDir "$Name.out.log"
    $errPath = Join-Path $LogDir "$Name.err.log"
    $header = "[$(Get-Date -Format o)] $FileName $($Arguments -join ' ')"
    Set-Content -LiteralPath $logPath -Value $header -Encoding UTF8
    try {
        $process = Start-Process -FilePath $FileName -ArgumentList $Arguments -WorkingDirectory $WorkingDirectory -RedirectStandardOutput $outPath -RedirectStandardError $errPath -Wait -PassThru -WindowStyle Hidden
        Add-Content -LiteralPath $logPath -Value "`n--- stdout ---" -Encoding UTF8
        if (Test-Path -LiteralPath $outPath) { Get-Content -LiteralPath $outPath -ErrorAction SilentlyContinue | Add-Content -LiteralPath $logPath -Encoding UTF8 }
        Add-Content -LiteralPath $logPath -Value "`n--- stderr ---" -Encoding UTF8
        if (Test-Path -LiteralPath $errPath) { Get-Content -LiteralPath $errPath -ErrorAction SilentlyContinue | Add-Content -LiteralPath $logPath -Encoding UTF8 }
        $ok = $process.ExitCode -eq 0
        Add-ProcessToolPaths
        return [ordered]@{
            ok = $ok
            exitCode = $process.ExitCode
            log = $logPath
            summary = $(Get-Content -LiteralPath $logPath -Tail 30 -ErrorAction SilentlyContinue)
        }
    } catch {
        Add-Content -LiteralPath $logPath -Value $_.Exception.Message -Encoding UTF8
        return [ordered]@{
            ok = $false
            exitCode = -1
            log = $logPath
            summary = @($_.Exception.Message)
        }
    }
}

function Install-Hermes {
    return Invoke-FixedCommand "install-hermes" "powershell" @("-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", $HermesInstallCommand)
}

function Install-Workspace {
    Add-ProcessToolPaths
    if (-not (Get-HermesCommand)) {
        return [ordered]@{ ok = $false; exitCode = -1; log = ""; summary = @("Hermes Agent is missing. Install Hermes first; it normally provisions Git and Node.js 22.") }
    }
    $git = Get-GitCommand
    if (-not $git) {
        return [ordered]@{ ok = $false; exitCode = -1; log = ""; summary = @("Git is still missing after Hermes install. Rerun the official Hermes installer or install Git manually.") }
    }
    if (-not (Test-Node22)) {
        return [ordered]@{ ok = $false; exitCode = -1; log = ""; summary = @("Node.js 22+ is still missing after Hermes install. Rerun the official Hermes installer.") }
    }
    $pnpm = Get-PnpmCommand
    if (-not $pnpm) {
        $npm = Get-NpmCommand
        if (-not $npm) {
            return [ordered]@{ ok = $false; exitCode = -1; log = ""; summary = @("npm is missing, so pnpm cannot be installed. Rerun the Hermes installer.") }
        }
        $pnpmInstall = Invoke-FixedCommand "install-pnpm" $npm @("install", "-g", "pnpm")
        if (-not $pnpmInstall.ok) { return $pnpmInstall }
        $pnpm = Get-PnpmCommand
    }
    if (-not (Test-Path $WorkspaceDir)) {
        $clone = Invoke-FixedCommand "clone-workspace" $git @("clone", $WorkspaceSource, $WorkspaceDir) $WorkspaceRoot
        if (-not $clone.ok) { return $clone }
    } else {
        $pull = Invoke-FixedCommand "update-workspace" $git @("-C", $WorkspaceDir, "pull", "--ff-only") $WorkspaceDir
        if (-not $pull.ok) { return $pull }
    }
    return Invoke-FixedCommand "install-workspace-deps" $pnpm @("install") $WorkspaceDir
}

function Install-DigitalState {
    Add-ProcessToolPaths
    $hermes = Get-HermesCommand
    if (-not $hermes) {
        return [ordered]@{ ok = $false; exitCode = -1; log = ""; summary = @("Hermes Agent is missing. Install Hermes Agent first.") }
    }
    return Invoke-FixedCommand "install-digital-state" $hermes @("profile", "install", $DigitalStateSource, "--alias", "-y")
}

function Start-Stack {
    Add-ProcessToolPaths
    $hermes = Get-HermesCommand
    $pnpm = Get-PnpmCommand
    if (-not $hermes) {
        return [ordered]@{ ok = $false; error = "Hermes Agent is not installed."; command = $HermesInstallCommand }
    }
    if (-not (Test-DigitalStateProfile)) {
        return [ordered]@{ ok = $false; error = "Digital State profile is not installed."; command = "hermes profile install $DigitalStateSource --alias --yes" }
    }
    if (-not (Test-Path (Join-Path $WorkspaceDir "package.json"))) {
        return [ordered]@{ ok = $false; error = "Hermes Workspace is not installed."; command = "git clone $WorkspaceSource" }
    }
    if (-not $pnpm) {
        return [ordered]@{ ok = $false; error = "pnpm is not installed."; command = "npm install -g pnpm" }
    }
    $gatewayCommand = "& '$hermes' gateway run"
    Start-Process -FilePath "powershell" -ArgumentList @("-NoExit", "-Command", $gatewayCommand) -WindowStyle Normal | Out-Null
    Start-Process -FilePath "powershell" -ArgumentList @("-NoExit", "-Command", "pnpm dev") -WorkingDirectory $WorkspaceDir -WindowStyle Normal | Out-Null
    Start-Process "http://localhost:3000" | Out-Null
    return [ordered]@{ ok = $true; url = "http://localhost:3000"; command = "hermes gateway run; pnpm dev" }
}

function Handle-Request($Context) {
    $path = $Context.Request.Url.AbsolutePath
    if ($Context.Request.HttpMethod -eq "GET" -and $path -eq "/") {
        $html = (Get-Content -LiteralPath $UiPath -Raw -Encoding UTF8).Replace("__BOOTSTRAP_NONCE__", $BootstrapNonce)
        return Write-Response $Context 200 $html "text/html; charset=utf-8"
    }
    if ($Context.Request.HttpMethod -eq "GET" -and $path -eq "/api/status") {
        return Write-Response $Context 200 (ConvertTo-JsonResponse (Get-StackStatus))
    }
    if ($Context.Request.HttpMethod -eq "POST" -and $Context.Request.Headers["X-Bootstrap-Token"] -ne $BootstrapNonce) {
        return Write-Response $Context 403 (ConvertTo-JsonResponse @{ error = "invalid bootstrap nonce" })
    }
    if ($Context.Request.HttpMethod -eq "POST" -and $path -eq "/api/install/hermes") {
        return Write-Response $Context 200 (ConvertTo-JsonResponse (Install-Hermes))
    }
    if ($Context.Request.HttpMethod -eq "POST" -and $path -eq "/api/install/workspace") {
        return Write-Response $Context 200 (ConvertTo-JsonResponse (Install-Workspace))
    }
    if ($Context.Request.HttpMethod -eq "POST" -and $path -eq "/api/install/digital-state") {
        return Write-Response $Context 200 (ConvertTo-JsonResponse (Install-DigitalState))
    }
    if ($Context.Request.HttpMethod -eq "POST" -and $path -eq "/api/start") {
        return Write-Response $Context 200 (ConvertTo-JsonResponse (Start-Stack))
    }
    return Write-Response $Context 404 (ConvertTo-JsonResponse @{ error = "not found" })
}

function New-Listener {
    for ($candidate = $Port; $candidate -lt ($Port + 50); $candidate++) {
        $listener = [System.Net.HttpListener]::new()
        $listener.Prefixes.Add("http://127.0.0.1:$candidate/")
        try {
            $listener.Start()
            return @{ listener = $listener; port = $candidate }
        } catch {
            $listener.Close()
        }
    }
    throw "No available localhost port found."
}

Add-ProcessToolPaths
$server = New-Listener
$listener = $server.listener
$url = "http://127.0.0.1:$($server.port)/"

Write-Host "Digital State Stack Installer"
Write-Host "URL: $url"
Write-Host "Logs: $LogDir"
Start-Process $url | Out-Null

try {
    while ($listener.IsListening) {
        $context = $listener.GetContext()
        try {
            Handle-Request $context
        } catch {
            Write-Response $context 500 (ConvertTo-JsonResponse @{ error = "request failed"; detail = $_.Exception.Message })
        }
    }
} finally {
    $listener.Close()
}

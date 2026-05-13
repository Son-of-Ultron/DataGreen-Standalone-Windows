param(
    [string]$AppVersion = "1.0.0"
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRootPath = (Resolve-Path (Join-Path $scriptDir "..")).Path
$issPath = Join-Path $scriptDir "installer\DataGreen.iss"
$releaseDir = Join-Path $repoRootPath "release\installer"

if (-not (Test-Path $issPath)) {
    throw "Arquivo Inno Setup não encontrado: $issPath"
}

New-Item -ItemType Directory -Force -Path $releaseDir | Out-Null

function Get-IsccPath {
    $candidates = @(
        "$env:ProgramFiles\Inno Setup 6\ISCC.exe",
        "$env:ProgramFiles(x86)\Inno Setup 6\ISCC.exe"
    )

    foreach ($candidate in $candidates) {
        if (Test-Path $candidate) {
            return $candidate
        }
    }

    $fromPath = Get-Command iscc.exe -ErrorAction SilentlyContinue
    if ($fromPath) {
        return $fromPath.Source
    }

    return $null
}

$iscc = Get-IsccPath
if (-not $iscc) {
    Write-Host "Inno Setup não encontrado. Tentando instalar via winget..." -ForegroundColor Yellow
    winget install -e --id JRSoftware.InnoSetup --accept-package-agreements --accept-source-agreements --disable-interactivity
    $iscc = Get-IsccPath
    if (-not $iscc) {
        throw "Não foi possível localizar o ISCC.exe após tentativa de instalação."
    }
}

$bootstrap = Join-Path $repoRootPath "1-INSTALAR-PRIMEIRA-VEZ.bat"
if (-not (Test-Path -LiteralPath $bootstrap)) {
    throw "Arquivo obrigatorio nao encontrado na raiz do repo: $bootstrap (repoRoot=$repoRootPath)"
}

Write-Host "Compilando instalador com: $iscc" -ForegroundColor Cyan
Write-Host "REPO_ROOT (Inno): $repoRootPath" -ForegroundColor DarkGray
$repoRootArg = '/DREPO_ROOT="' + $repoRootPath + '"'
& $iscc $repoRootArg "/DMyAppVersion=$AppVersion" $issPath

if ($LASTEXITCODE -ne 0) {
    throw "Falha ao compilar instalador (exit code $LASTEXITCODE)."
}

Write-Host "Instalador gerado em: $releaseDir" -ForegroundColor Green

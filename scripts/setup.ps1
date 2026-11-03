# One-time setup on Windows: Python venv + backend deps, frontend deps and build, .env from the example.
$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")
py -3.12 -m venv .venv
if (-not $?) { python -m venv .venv }
& .venv\Scripts\python.exe -m pip install -q --upgrade pip
& .venv\Scripts\python.exe -m pip install -q -r backend\requirements.txt
Push-Location frontend
npm ci --no-audit --no-fund
npm run build
Pop-Location
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
Write-Host ""
Write-Host "Setup done. Put your Meta Model API key in .env (MODEL_API_KEY=...), or leave it empty for DEMO_MODE replay."
Write-Host "Then run: .\scripts\dev.ps1   and open http://localhost:8765"

$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath (Split-Path -Parent $PSScriptRoot)
python -X utf8 cong_cu/scan_all.py --all-pages --workers 6
if ($LASTEXITCODE) { throw 'Scan interrupted. Re-run to resume saved pages.' }
python -X utf8 cong_cu/make_report.py
if ($LASTEXITCODE) { throw 'Report generation failed' }
Write-Output 'DONE: data/audit/review.html'

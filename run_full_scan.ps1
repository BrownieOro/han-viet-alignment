$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
python -X utf8 scan_all.py --workers 6
if ($LASTEXITCODE) { throw 'Scan interrupted. Re-run to resume saved pages.' }
python -X utf8 make_report.py
if ($LASTEXITCODE) { throw 'Report generation failed' }
Write-Output 'DONE: data/audit/review.html'

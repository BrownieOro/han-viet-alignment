"""Refresh the review page while a full scan is running; stop at full coverage."""
from pathlib import Path
import subprocess
import sys
import time
root=Path(__file__).resolve().parents[1]
last=-1
stalled=0
while True:
    result=subprocess.run([sys.executable,'-X','utf8',str(root/'cong_cu/make_report.py')],cwd=root)
    count=len([p for p in (root/'data/audit/pages').glob('*/*.json') if not p.name.endswith('.error.json')])
    print(f'{count}/2044 saved pages',flush=True)
    if count>=2044: break
    stalled=stalled+1 if count==last else 0
    if stalled>=20:
        print('No new saved page for 15 minutes. Re-run run_full_scan.ps1 to resume.',flush=True)
        break
    last=count
    time.sleep(45)

"""Refresh the review page while a full scan is running; stop at full coverage."""
from pathlib import Path
import subprocess
import sys
import time
root=Path(__file__).resolve().parent
while True:
    result=subprocess.run([sys.executable,'-X','utf8',str(root/'make_report.py')],cwd=root)
    count=len(list((root/'data/audit/pages').glob('*/*.json')))
    print(f'{count}/2044 saved pages',flush=True)
    if count>=2044: break
    time.sleep(45)

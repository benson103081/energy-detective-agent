"""Rebuild the proposal and validate its distributable artifacts."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
for script in ("assemble_proposal.py", "finish_slides.py", "build_deliverables.py", "verify_deliverables.py"):
    subprocess.run([sys.executable, str(ROOT / "scripts" / script)], cwd=ROOT, check=True)

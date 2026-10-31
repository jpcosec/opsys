"""Generate diagram projections through spec2viz; never author Mermaid by hand."""
from pathlib import Path
import subprocess
import sys
B = Path(__file__).resolve().parent
subprocess.run([sys.executable, str(B/'build_plan.py'), '--check'], check=True)
subprocess.run(['spec2viz','diagram','validate',str(B/'dag.diagram.yaml')],check=True)
for renderer in ['mermaid','graph']:
    subprocess.run(['spec2viz','diagram','render',str(B/'dag.diagram.yaml'),'--renderer',renderer,'--out',str(B)],check=True)

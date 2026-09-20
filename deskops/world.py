"""The single seam between deskops and sldb/kgdb.

Every sldb/kgdb contact in deskops goes through this module: `get_world`
opens a `pron.World`, and the rest of deskops imports `World`, `Store`,
`Graph`, `extract_model_data`, `render_model_markdown` and `GraphSnapshot`
from here — never directly from sldb/kgdb (docs/implementation-plan.md; seam rule).

Documented exceptions, allowed here only (each imports sldb/kgdb directly):

1. `sldb.runtime.validation.extract_model_data` / `render_model_markdown`:
   pron's own `docs_sync` imports these directly today; deskops mirrors that
   until pron re-exports them (gap-log: desk/pron-gap-log.md).
2. `kgdb.contracts.io.GraphSnapshot`: validates deskops' own snapshot
   artifact — the KGDB contract layer, not document access — until pron
   re-exports it (gap-log: desk/pron-gap-log.md).
"""

from __future__ import annotations

from pathlib import Path

from pron.world.doc_id import DocId
from pron.world.graph import Graph
from pron.world.store import Store
from pron.world.world import World

# Exception 1: document model rendering/extraction. sldb.runtime.validation is
# pron's own import path for these names too (pron/docs_sync/*); swap for a
# pron re-export when one exists.
from sldb.runtime.validation import extract_model_data
from sldb.runtime.validation import render_model_markdown

# Exception 2: KGDB contract validation of the deskops snapshot artifact.
from kgdb.contracts.io import GraphSnapshot

# Exception 3: the static Python scan. The code world (CommitDoc/ChangeDoc/
# TestCoverageDoc, and the PythonSymbolDoc documents they hang off) is derived
# from sldb's scan; `sldb selfdoc python-sync` cannot write it here because it
# requires AST-typed relation types (`contains`) that conflict with the document
# graph vocabulary (gap-log).
from sldb.selfdoc.python_source_scan import scan_source_facts

__all__ = [
    "scan_source_facts",
    "World",
    "Store",
    "Graph",
    "DocId",
    "get_world",
    "extract_model_data",
    "render_model_markdown",
    "GraphSnapshot",
]


def get_world(root: str | Path = ".") -> World:
    """Open the pron World at `root` with deskops models importable.

    `pythonpath` is the repo root directory (sldb prepends it to sys.path), so
    `deskops.models:XxxDoc` model references resolve from any working dir. The
    bare module name is not a valid search path for sldb's resolver.
    """
    repo_root = Path(root).resolve()
    return World(repo_root, pythonpath=str(repo_root))


def scan_python_facts(source_root: str | Path, package: str | None = None) -> list[dict]:
    """The static facts of every Python file below `source_root` (seam for sldb's scan).

    Read-only: `deskops.code` turns the facts into documents, the scan never
    imports the code it reads.
    """
    root = Path(source_root).resolve()
    return scan_source_facts(root, package)


def ensure_store_root(root: str | Path = ".") -> Path:
    """Create the `.sldb` store at `root` when it does not exist yet.

    A pron World only opens an existing store, so bootstrap must create one
    before `get_world` on a fresh repo (`deskops init`). Seam for
    `sldb.api.init_store` / `sldb.store.layout.store_exists`; no-op when the
    store is already there.
    """
    from sldb.api import init_store
    from sldb.store.layout import store_exists

    root_path = Path(root).resolve()
    if not store_exists(root_path / ".sldb"):
        init_store(root_path)
    return root_path
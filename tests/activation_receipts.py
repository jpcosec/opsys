"""Accepted, pinned review receipts for the tests that activate a task (CC32).

The activation gate of each factory task type is a ``RuleDoc`` seed of the desk
(``deskops/data/rules/``): a task leaves ``ritual-execution`` only with the review receipts
its type asks for, ``accepted`` and with an ``intact`` anchor on the task's contract, and its
dependencies closed. A test that advances a task writes those receipts first with this helper.

The receipts are written through ``sldb.api.transaction`` (TaskDoc precisión b8): ``create``
writes the ``ReviewDoc`` and ``update`` saves it again through ``save_document_payload``, the
step that pins ``subject`` with the task's contract hash (GO07). Before CC35a the write path
of ``deskops review`` (render + track, without that save) did not pin, so a receipt written
that way stayed ``lost``; the helper keeps writing through sldb directly. Nothing here
writes a file by hand or decides the receipts in Python: ``RECEIPTS`` mirrors the rules'
``kind`` clauses so a test can ask for "the receipts of this task's type".
"""

from __future__ import annotations

from datetime import datetime
from datetime import timezone
from pathlib import Path

from deskops.paths import package_pythonpath

#: Receipt kinds each factory activation rule requires (deskops/data/rules/rule-activation-*.md).
RECEIPTS: dict[str, tuple[str, ...]] = {
    "task.code": ("preflight", "bundle"),
    "task.docs": ("preflight",),
    "task.debug": ("preflight", "reproduction"),
    "task.refactor": ("preflight", "bundle", "goldens"),
    "task.decision": ("owner",),
    "task.aggregate": (),
    "task.external": ("preflight",),
}


def tracked_task(root: Path, task_id: str) -> tuple[str, str]:
    """``(model, task_type)`` of a tracked task: the store's model and the file's ``task_type``."""
    from sldb.api.stores.doc_status import doc_status
    from sldb.runtime.validation import extract_model_data

    from deskops.models import TaskDoc

    path = root / "desk" / "tasks" / f"{task_id}.md"
    status = doc_status(root / ".sldb", path.relative_to(root).as_posix())
    assert status.model, f"{task_id} is not tracked in {root / '.sldb'}"
    payload = extract_model_data(TaskDoc, path.read_text(encoding="utf-8"))
    return status.model, str(payload.get("task_type") or "")


def accept_receipts(root: Path, task_id: str, kinds: tuple[str, ...] | None = None, *, actor: str = "test") -> list[str]:
    """Write one accepted, pinned ``ReviewDoc`` per kind for ``task_id`` (its type's kinds by
    default); return the review ids. Each receipt is ``review-<task>-<kind>-<n>`` under
    ``desk/reviews/<task>/``, as ``deskops review`` names them."""
    from sldb.api import transaction

    model, task_type = tracked_task(root, task_id)
    if kinds is None:
        kinds = RECEIPTS.get(task_type, RECEIPTS["task.code"])
    now = datetime.now(timezone.utc).isoformat()
    review_dir = root / "desk" / "reviews" / task_id
    written: list[str] = []
    with transaction(root / ".sldb", pythonpath=package_pythonpath()) as tx:
        for kind in kinds:
            n = len(list(review_dir.glob(f"{kind}-*.md"))) + 1 if review_dir.exists() else 1
            review_id = f"review-{task_id}-{kind}-{n}"
            payload = {
                "id": review_id,
                "title": f"{kind.capitalize()} review of {task_id}",
                "kind": kind,
                "subject": f"doc:{model}:{task_id}",
                "subject_ref": "",
                "engine": "human",
                "actor": actor,
                "run_dir": "",
                "input_sha256": "",
                "output_sha256": "",
                "verdict": "accepted",
                "reason": "accepted by the test",
                "created_at": now,
                "disposed_at": now,
                "disposed_by": actor,
                "summary": f"{kind} review accepted by the test.",
                "disposition": "Verdict accepted: accepted by the test",
                "tags": ["workspace:desk"],
            }
            tx.create("ReviewDoc", review_id, payload, path=review_dir / f"{kind}-{n}.md")
            # The second save pins `subject` with the task's contract hash (create does not).
            tx.update(review_id, payload)
            written.append(review_id)
    return written

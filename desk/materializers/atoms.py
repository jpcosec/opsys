from __future__ import annotations


def _source_tag(atom_id: str) -> str:
    return f"source-atom:{atom_id}"


def build_architecture_doc_payload(atom: dict, *, title: str | None = None) -> dict:
    atom_id = atom["id"]
    atom_title = atom["title"]
    return {
        "title": title or f"{atom_title} Derivation",
        "body": "\n\n".join(
            [
                f"Derived from `{atom_id}`.",
                atom["what"],
                "## Why this matters\n\n" + atom["why"],
                "## Operational application\n\n" + atom["how"],
                "## Workflow lineage\n\n"
                + "\n".join(
                    [f"- {item}" for item in atom.get("materializes_into", [])]
                ),
            ]
        ),
    }


def build_feature_payload(
    atom: dict, *, feature_id: str, title: str | None = None
) -> dict:
    atom_id = atom["id"]
    return {
        "title": title or f"Materialize {atom['title']} as a deferred feature",
        "id": feature_id,
        "status": "proposed",
        "goal": atom["what"],
        "why": atom["why"],
        "scope": atom["where"],
        "proposed_shape": atom["how"],
        "adoption_path": f"Promote when `{atom_id}` needs deferred planning work.",
        "validation": [
            f"Traceability back to `{atom_id}` is explicit.",
            "The feature stays phase-appropriate and deferred.",
        ],
        "tags": [
            _source_tag(atom_id),
            "system:sldb",
            "workspace:drawer",
            "topic:atoms",
        ],
    }


def build_task_payload(atom: dict, *, task_id: str, title: str | None = None) -> dict:
    atom_id = atom["id"]
    return {
        "title": title or f"Apply {atom['title']} in active execution",
        "id": task_id,
        "status": "active",
        "goal": atom["what"],
        "scope": atom["where"],
        "references": [f"atom:{atom_id}"],
        "depends_on": [],
        "pills": [],
        "files": [],
        "implementation_path": atom["how"],
        "validation": [
            f"The task still reflects `{atom_id}` without semantic drift.",
        ],
        "done_when": f"The active work implements `{atom_id}` coherently.",
        "tags": [
            _source_tag(atom_id),
            "system:sldb",
            "workspace:desk",
            "topic:atoms",
        ],
    }


def build_pill_payload(atom: dict, *, pill_id: str, title: str | None = None) -> dict:
    atom_id = atom["id"]
    return {
        "title": title or f"Atom: {atom['title']}",
        "id": pill_id,
        "what": atom["what"],
        "why": atom["why"],
        "when": atom["when"],
        "where": atom["where"],
        "how": atom["how"],
        "how_not": atom["distinct_from_pills"],
        "tags": [
            _source_tag(atom_id),
            "system:sldb",
            "workspace:desk",
            "topic:atoms",
        ],
    }

from __future__ import annotations


def build_composed_doc_payload(
    atoms: list[dict], *, title: str, body_intro: str = ""
) -> dict:
    sections = [body_intro.strip()] if body_intro.strip() else []
    for atom in atoms:
        sections.append(
            "\n\n".join(
                [
                    f"## {atom['title']}",
                    f"Atom: `{atom['id']}`",
                    f"5WH1+: `{atom['five_wh_one_plus']}`",
                    atom["answer"],
                ]
            )
        )
    return {"title": title, "body": "\n\n".join(sections)}


def build_architecture_doc_payload(atom: dict, *, title: str | None = None) -> dict:
    return build_composed_doc_payload(
        [atom],
        title=title or f"{atom['title']} Composition",
        body_intro=f"Materialized from `{atom['id']}` through document composition.",
    )

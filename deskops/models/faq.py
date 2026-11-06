from pydantic import Field

from sldb import StructuredNLDoc


class DeskFAQDoc(StructuredNLDoc):
    # Artifact-level defaults `deskops add` applies (formerly one YAML spec per artifact):
    # the id built from the slug, the status a new document gets, and its default tags.
    __artifact__ = {
        "id_pattern": "faq-{slug}",
        "status_default": "active",
        "tags": ["workspace:docs", "artifact:faq"],
    }
    __semantics__ = {
        "type": ["documentation", "faq"],
        "workspace": ["docs", "faq"],
    }
    __template__ = """
# ⸢rev•title⸥

_Write the FAQ content, including questions, answers, command examples, and references._

⸢rev•body⸥
""".strip()

    title: str = Field(description="Primary H1 heading for the FAQ document.")
    body: str = Field(
        description="Full FAQ body after the H1, including questions, answers, command examples, and cross-references to atom docs."
    )

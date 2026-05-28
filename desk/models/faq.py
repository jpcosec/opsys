from pydantic import Field

from sldb import StructuredNLDoc


class FAQDoc(StructuredNLDoc):
    __semantics__ = {
        "type": ["documentation", "faq"],
        "workspace": ["docs", "faq"],
    }
    __template__ = """
# ⸢rev•title⸥

⸢rev•body⸥

## Field Refs

- ⸢rev,list•field_refs⸥
""".strip()

    title: str = Field(description="Primary H1 heading for the FAQ document.")
    body: str = Field(
        description="Full FAQ body after the H1, including questions, answers, command examples, and cross-references to atom docs."
    )
    field_refs: list[str] = Field(
        default_factory=list,
        description="Field instance identifiers composed into the FAQ artifact.",
    )

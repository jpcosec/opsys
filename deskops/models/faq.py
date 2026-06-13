from pydantic import Field

from sldb import StructuredNLDoc


class FAQDoc(StructuredNLDoc):
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

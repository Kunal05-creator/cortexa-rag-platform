"""
Core document models used throughout Cortexa.

Every parser, chunker, retriever and LLM module
works with these models instead of raw dictionaries.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class Table:
    """
    Represents a table extracted from a document.
    """

    page: int
    rows: List[List[str]] = field(default_factory=list)


@dataclass
class Image:
    """
    Represents an image inside a document.
    """

    page: int
    caption: str = ""
    image_index: int = 0


@dataclass
class Page:
    """
    Represents one page of a document.
    """

    page_number: int

    text: str

    headings: List[str] = field(default_factory=list)

    tables: List[Table] = field(default_factory=list)

    images: List[Image] = field(default_factory=list)

    metadata: Dict = field(default_factory=dict)


@dataclass
class Document:
    """
    High-level document object.

    This becomes the standard object
    passed throughout Cortexa.
    """

    filename: str

    title: str = ""

    author: str = ""

    subject: str = ""

    keywords: List[str] = field(default_factory=list)

    total_pages: int = 0

    pages: List[Page] = field(default_factory=list)

    metadata: Dict = field(default_factory=dict)

    def get_page(
        self,
        page_number: int
    ) -> Optional[Page]:

        for page in self.pages:

            if page.page_number == page_number:

                return page

        return None
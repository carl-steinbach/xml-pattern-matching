from typing import Self
from xml.etree.ElementTree import Element


class Match:
    """
    Represents a successful match, hold the extracted values, the found element, and child match objects recursively
    """
    children: list[Self]

    def __init__(self, extracted_values: dict[str, any], element: Element, set_id: str = None, children=None):
        self.element = element
        self.extracted_values = extracted_values
        if children is None:
            children = []
        self.children = children
        self.element = element
        self.set_id = set_id

    def fmt_lines(self):
        if self.set_id is None:
            return [f"{self.element.tag}"]

        fmt = [f"{self.element.tag} (set={self.set_id}) (extracted={self.extracted_values})"]
        for child in self.children:
            child_fmt_lines = child.fmt_lines()
            for line in child_fmt_lines:
                fmt.append("\t" + line)

        return fmt

    def __str__(self):
        return "\n".join(self.fmt_lines())

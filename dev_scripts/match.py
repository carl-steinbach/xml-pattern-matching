import logging

from xml_pattern_matching import load
from xml_pattern_matching.match_element import MatchElement

logging.basicConfig(level=logging.DEBUG)


def main():
    etree = load.etree_from_pyfile(__file__)
    root = etree.getroot()

    match_element = MatchElement(
        "div",
        required_attributes=["class", "id", ("value", "expected_value")],
        match_children_sets={
            "set-0": [
                MatchElement("span"),
                MatchElement(
                    "div",
                    text="text_1",
                    match_children_sets={
                        "set-1": [
                            MatchElement(
                                "div",
                                text="text_2"
                            )
                        ]
                    }
                )
            ]
        }
    )
    print("hello")
    match = match_element.match(element=root)
    if match is None:
        print("no match")
    else:
        print(match)


if __name__ == "__main__":
    main()

import logging
from xml.etree.ElementTree import Element

import defusedxml.ElementTree

from xml_pattern_matching.match_element import MatchElement

logging.basicConfig(level=logging.DEBUG)


def main():
    # etree = load.etree_from_pyfile(__file__)

    with open("account_information.xml", "r") as xmlfile:
        xmltree = defusedxml.ElementTree.parse(xmlfile)

    # Provide custom functions for extracting values from elements.
    def extract_account_number(element: Element) -> int:
        return int(element.text.strip().split(".")[0])

    # Construct the matching structure using a MatchElement.
    match_element = MatchElement(
        tag="div",
        children=[
            MatchElement(
                tag="span",
                text="Account Information"
            ),
            MatchElement(
                tag="div",
                children={  # Match either layout A or B from the subtree, by providing a dictionary instead of a list.
                    "layout_A": [
                        MatchElement("div"),
                        MatchElement(
                            tag="div",
                            children=[
                                MatchElement(
                                    tag="div",
                                    extract={
                                        "account_number": extract_account_number
                                    }
                                )
                            ]
                        )
                    ],
                    "layout_B": [
                        MatchElement(
                            tag="span",
                            extract={
                                "account_number": extract_account_number
                            }
                        ),
                        MatchElement("div")
                    ]
                }
            )
        ]
    )

    # Matching.
    match = match_element.match(xmltree.getroot())
    if match is None:
        print("no match")
        exit(1)

    account_number = match.extracted_values["account_number"]
    print(f"extracted account number: {account_number}")

    # Prints the full tree of the match, along with which sets where matched and where which information was extracted.
    print(match)


if __name__ == "__main__":
    main()

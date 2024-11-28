import logging
from xml.etree.ElementTree import Element

from test.match_test import MatchTestCase
from xml_pattern_matching.match_element import MatchElement

logging.basicConfig(level=logging.DEBUG)


class TestMatchChildren(MatchTestCase):
    def test_match_children_a(self):
        def extract_function(element: Element) -> any:
            return element.text

        match_element = MatchElement(
            tag="div", children={
                "set_0": [
                    MatchElement("div"),
                    MatchElement("div"),
                    MatchElement("div", children={
                        "set_0": [
                            MatchElement(
                                "div",
                                children={
                                    "set_0": [
                                        MatchElement("div"),
                                        MatchElement(
                                            "div",
                                            extract={
                                                "value": extract_function
                                            }),
                                        MatchElement("div")
                                    ]
                                }
                            )
                        ]
                    })
                ]
            }
        )
        match = match_element.match(self.xmltree.getroot())
        self.assertIsNotNone(match)
        self.assertEqual("expected_value", match.extracted_values["value"])

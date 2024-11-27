import logging

from test.match_test import MatchTestCase
from xml_pattern_matching.match_element import MatchElement

logging.basicConfig(level=logging.DEBUG)


class TestMatchChildren(MatchTestCase):
    def test_match_children_a(self):
        match_element = MatchElement(
            "div",required_attributes=["class", "id", ("value", "expected_value")],
            match_children_sets={
                "set-0": [
                    MatchElement("span"),
                    MatchElement("div", text="text_1", match_children_sets={
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
        match = match_element.match(element=self.xmltree.getroot())
        self.assertTrue(match)

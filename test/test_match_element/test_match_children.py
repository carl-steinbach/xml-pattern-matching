import logging

from test.match_test import MatchTestCase
from xml_pattern_matching.match_element import MatchElement

logging.basicConfig(level=logging.DEBUG)


class TestMatchChildren(MatchTestCase):
    def test_match_children_a(self):
        match_element = MatchElement(
            "div", required_attributes=["class", "id", ("value", "expected_value")],
            children={
                "set-0": [
                    MatchElement("span"),
                    MatchElement("div", text="text_1", children={
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
        match, reason = match_element.match(element=self.xmltree.getroot())
        self.assertIsNotNone(match)
        self.assertEqual(0, len(reason))

    def test_match_children_set(self):
        match_element = MatchElement(
            tag="div",
            required_attributes=["class", "id", ("value", "expected_value")],
            children={
                "unexpected_set": [
                    MatchElement("span"),
                    MatchElement("div", text="invalid_text")
                ],
                "expected_set": [
                    MatchElement("span"),
                    MatchElement(
                        "div", text="text_1", children={
                            "expected_set": [
                                MatchElement(
                                    "div",
                                    text="text_2"
                                )
                            ],
                            "unexpected_set": [
                                MatchElement("div"),
                                MatchElement("span")
                            ]
                        }
                    )
                ]
            }
        )
        match, reason = match_element.match(self.xmltree.getroot())
        self.assertIsNotNone(match)
        self.assertEqual(0, len(reason))
        self.assertEqual("expected_set", match.set_id)
        self.assertEqual("expected_set", match.children[1].set_id)

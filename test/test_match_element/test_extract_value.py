import logging
from xml.etree.ElementTree import Element

from test.match_test import MatchTestCase
from xml_pattern_matching.exceptions import ExtractionException
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
        match, reason = match_element.match(self.xmltree.getroot())
        if match is None:
            logging.error(reason)
        self.assertIsNotNone(match)
        self.assertEqual("expected_value", match.extracted_values["value"])
        logging.info(match)

    def test_match_using_extraction(self):
        expected_value = "expected_value"
        
        def extract_function(element: Element) -> str:
            if element.text != expected_value:
                raise ExtractionException(f"element.text is not {expected_value}")
            
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
                                        MatchElement(
                                            "div",
                                            extract={
                                                "value": extract_function   # should fail and not match
                                            }
                                        ),
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
        match, reason = match_element.match(self.xmltree.getroot())
        if match is not None:
            logging.error(f"match should be none: {match}")
        self.assertIsNone(match)
        self.assertIn("ExtractionException", reason)
        logging.info(reason)
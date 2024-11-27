from test.match_test import MatchTestCase
from xml_pattern_matching.match_element import MatchElement


class TestMatch(MatchTestCase):
    def test_match_a(self):
        match_element = MatchElement(
            "div",
            required_attributes=["class", "id", ("value", "100")]
        )
        match = match_element.match(element=self.xmltree.getroot())
        self.assertTrue(match)

    def test_match_b(self):
        match_element = MatchElement(
            "div",
            required_attributes=["class", "id", ("value", "200")]
        )
        match = match_element.match(self.xmltree.getroot())
        self.assertFalse(match)

    def test_match_c(self):
        match_element = MatchElement(
            "div",
            "extract_this_value",
            required_attributes=["class", "id", ("value", "200")],
        )
        match = match_element.match(self.xmltree.getroot())
        self.assertFalse(match)

from test.match_test import MatchTestCase
from xml_pattern_matching.match_element import MatchElement


class TestMatch(MatchTestCase):
    def test_match_a(self):
        match_element = MatchElement(
            "div",
            ["class", "id"],
            required_attribute_values=[("value", "100")]
        )
        match = match_element.match(element=self.xmltree.getroot())
        self.assertTrue(match)

    def test_match_b(self):
        match_element = MatchElement(
            "div",
            ["class", "id"],
            required_attribute_values=[("value", "200")]
        )
        match = match_element.match(self.xmltree.getroot())
        self.assertFalse(match)

    def test_match_c(self):
        match_element = MatchElement(
            "div",
            ["class", "id"],
            required_attribute_values=[("value", "200")],
            match_children_sets={
                "set 1": [
                    MatchElement()
                ]
            }
        )
        match = match_element.match(self.xmltree.getroot())
        self.assertFalse(match)

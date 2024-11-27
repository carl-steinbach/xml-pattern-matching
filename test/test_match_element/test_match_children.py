from test.match_test import MatchTestCase
from xml_pattern_matching.match_element import MatchElement


class TestMatchChildren(MatchTestCase):
    def test_match_children_a(self):
        match_element = MatchElement(
            "div",
            ["class", "id"],
            required_attribute_values=[("value", "100")]
        )
        match = match_element.match(element=self.xmltree.getroot())
        self.assertTrue(match)

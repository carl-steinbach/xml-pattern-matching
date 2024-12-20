import logging
from xml.etree.ElementTree import Element

from test.match_test import MatchTestCase
from xml_pattern_matching.match_element import MatchElement
from xml_pattern_matching.match_element_children import MatchElementChild, MatchElementSet

logging.basicConfig(level=logging.DEBUG)


class TestMatchElementChild(MatchTestCase):
    def test_match_children_a(self):
        def extract_user(element: Element) -> str:
            return element.text

        match_element = MatchElement(
            tag="users-parent",
            children=[
                MatchElement(
                    tag="span",
                    text="Users"
                ),
                MatchElement(
                    tag="list-parent",  # aggregate the matches to a list, and write to global "user" key
                    children=[
                        MatchElementChild(
                            MatchElement("span", text="list header")
                            # will be transformed to MatchElementChild -> MatchElementSet(MatchElement)
                        ),
                        MatchElementChild(
                            MatchElementSet(
                                MatchElement(
                                    tag="div",
                                    extract={
                                        "user": extract_user
                                    },
                                    children=[]
                                ),
                                MatchElement(
                                    tag="div",
                                    children=[
                                        MatchElement(
                                            tag={"span", "div"},
                                            extract={
                                                "user": extract_user
                                            },
                                            children=[]
                                        )
                                    ]
                                ),
                            ),
                            repeat=(1, 4)
                        ),
                    ],
                )
            ]
        )

        match, _ = match_element.match(element=self.xmltree.getroot())
        self.assertIsNotNone(match)
        expected_users = ["user_0", "user_1", "user_2", "user_3"]
        users = match.extracted_values["user"]
        self.assertEqual(expected_users, users)
        
    def test_match_element_child_no_match(self):
        def extract_user(element: Element) -> str:
            return element.text

        match_element = MatchElement(
            tag="users-parent",
            children=[
                MatchElement(
                    tag="span",
                    text="Users"
                ),
                MatchElement(
                    tag="list-parent",  # aggregate the matches to a list, and write to global "user" key
                    children=[
                        MatchElementChild(
                            MatchElement("span", text="list header")
                            # will be transformed to MatchElementChild -> MatchElementSet(MatchElement)
                        ),
                        MatchElementChild(
                            MatchElementSet(
                                MatchElement(
                                    tag="div",
                                    extract={
                                        "user": extract_user
                                    },
                                    children=[]
                                ),
                                MatchElement(
                                    tag="div",
                                    children=[
                                        MatchElement(
                                            tag={"span", "div"},
                                            extract={
                                                "user": extract_user
                                            },
                                            children=[]
                                        )
                                    ]
                                ),
                            ),
                            repeat=(1, 2)
                        ),
                    ],
                )
            ]
        )

        match, _ = match_element.match(element=self.xmltree.getroot())
        self.assertIsNone(match)

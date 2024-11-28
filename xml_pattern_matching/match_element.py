import logging
from typing import Callable, Self
from xml.etree.ElementTree import Element

from xml_pattern_matching.match import Match

logger = logging.getLogger(__name__)


def strip_whitespace_and_newlines(text: str):
    return text.removeprefix("\n").strip().removesuffix("\n")


class MatchElement:
    def __init__(
            self,
            tag: str,
            text: str = None,
            required_attributes: list[str | tuple[str, str]] = None,
            forbidden_attributes: list[str | tuple[str, str]] = None,
            children: dict[str, list[Self]] | list[Self] = None,
            extract: dict[str, Callable[[Element], any] | str] = None
    ):
        self.forbidden_attributes = forbidden_attributes
        self.text = text
        self.required_attributes = required_attributes
        self.tag = tag
        self.children = children
        self.extract = extract

    def match(self, element: Element, matched_path: str = "") -> Match | None:
        # Match tag.
        if self.tag != element.tag:
            logger.debug(f"Required tag: '{self.tag}' does not match actual tag: '{element.tag}'. ({matched_path})")
            return None

        # Match text.
        if self.text:
            required_text = strip_whitespace_and_newlines(self.text)
            actual_text = strip_whitespace_and_newlines(element.text)
            if actual_text != required_text:
                logger.debug(
                    f"Required text: '{required_text}' does not match actual text: '{actual_text}'. ({matched_path})"
                )
                return None

        # Match attributes.
        if self.required_attributes:
            for required_attribute in self.required_attributes:
                if isinstance(required_attribute, str):
                    if element.get(required_attribute) is None:
                        logger.debug(f"Required attribute: '{required_attribute}' is missing. ({matched_path})")
                        return None

                if isinstance(required_attribute, tuple):
                    actual_attribute_value = element.get(required_attribute[0])
                    if actual_attribute_value != required_attribute[1]:
                        logger.debug(
                            f"Required value {required_attribute[0]}='{required_attribute[1]}'"
                            f" does not match '{actual_attribute_value}'. ({matched_path})"
                        )
                        return None

        if self.forbidden_attributes:
            for forbidden_attribute in self.forbidden_attributes:
                if isinstance(forbidden_attribute, str):
                    if element.get(forbidden_attribute) is not None:
                        logger.debug(f"Forbidden attribute: '{forbidden_attribute}' is present. ({matched_path})")
                        return None

                if isinstance(forbidden_attribute, tuple):
                    actual_attribute_value = element.get(forbidden_attribute[0])
                    if actual_attribute_value == forbidden_attribute[1]:
                        logger.debug(
                            f"Forbidden attribute value {forbidden_attribute[0]}='{forbidden_attribute[1]}'"
                            f" is present '{actual_attribute_value}'. ({matched_path})"
                        )
                        return None

        # Extract values
        extracted_values = {}
        if self.extract:
            for key in self.extract.keys():
                extraction = self.extract[key]
                if isinstance(extraction, str):
                    extracted_values[key] = element.get(extraction)
                elif isinstance(extraction, Callable):
                    extracted_values[key] = extraction(element)
                else:
                    raise Exception(f"extraction {extraction} is neither a str nor a Callable. ({matched_path})")

        # Match Children.
        if self.children is not None:
            match = self.match_children(element, matched_path)
            if match is None:
                logger.debug(f"Could not match any set of children.")
                return None
            return match
        else:
            return Match(extracted_values=extracted_values, element=element)

    def match_children(self, element: Element, matched_path: str) -> Match | None:
        reason = ""
        if isinstance(self.children, dict):
            for match_children_set_id in self.children.keys():
                children_set = self.children[match_children_set_id]
                match, reason = match_children_set(
                    element=element, matched_path=matched_path, children_set=children_set, set_id=match_children_set_id
                )
                if match is not None:
                    return match

        elif isinstance(self.children, list):
            match, reason = match_children_set(
                element=element, matched_path=matched_path, children_set=self.children, set_id="_"
            )
            if match is not None:
                return match
        else:
            raise Exception("Attribute `children` is not of type 'list' or 'dict'.")

        logger.debug(f"Failed to match children: {reason}.")
        return None


def match_children_set(element: Element, matched_path: str, children_set: list[MatchElement],
                       set_id: str) -> (Match | None, str):
    """Compares a list of MatchElements with the children of a given XML Element.

    returns: A tuple consisting of a Match object and a string with an explanation, if no match was found.
    """
    if len(element) != len(children_set):
        reason = f"Expected {len(children_set)} children, found {len(element)}. ({matched_path})"
        return None, reason

    # has to match each child
    child_matches = []
    for child_index in range(len(element)):
        child_match = children_set[child_index].match(
            element=element[child_index], matched_path=matched_path + str(element[child_index].tag)
        )
        if not child_match:
            break

        child_matches.append(child_match)

    # check if matched
    if len(child_matches) == len(children_set):
        # build match from children
        extracted_values = {}
        for child_match in child_matches:
            extracted_values = {**extracted_values, **child_match.extracted_values}

        return Match(
            extracted_values=extracted_values,
            element=element,
            set_id=set_id,
            children=child_matches
        ), ""

    return None, f"Could not match all children. (matched {len(child_matches)} / {len(children_set)})"

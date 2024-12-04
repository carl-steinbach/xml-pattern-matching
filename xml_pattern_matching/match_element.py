import logging
import math
from typing import Any, Callable, Self
from xml.etree.ElementTree import Element

from xml_pattern_matching.match import Match

logger = logging.getLogger(__name__)


def strip_whitespace_and_newlines(text: str):
    return text.removeprefix("\n").strip().removesuffix("\n")


class MatchElement:
    """Defines a pattern matching a single XML element and potential children."""
    children: dict[str, list[Self]]
    repeat: tuple[int, int]

    def __init__(
            self,
            tag: str | set[str],
            text: str = None,
            required_attributes: list[str | tuple[str, str]] = None,
            forbidden_attributes: list[str | tuple[str, str]] = None,
            children: dict[str, list[Self]] | list[Self] = None,
            repeat: int | tuple[int, int | None] = 1,
            extract: dict[str, Callable[[Element], any] | str] = None
    ):
        self.forbidden_attributes = forbidden_attributes
        self.text = text
        self.required_attributes = required_attributes
        self.tag = tag
        if isinstance(children, list):
            children = {
                "_": children
            }
        self.children = children
        if isinstance(repeat, int):
            self.repeat = (repeat, repeat)
        elif isinstance(repeat, tuple) and isinstance(repeat[0], int):
            if repeat[1] is None:
                self.repeat = (repeat[0], int(math.inf))
            elif isinstance(repeat[1], int):
                repeat: tuple[int, int]
                self.repeat = repeat
            else:
                raise Exception("repeat[1] has to be an int or None")
        else:
            raise Exception("repeat has to be a tuple or an int")
        self.extract = extract

    def match(self, element: Element, matched_path: str = "") -> tuple[Match | None, str]:
        # Match tag.
        if self.tag:
            matched_tag: str | None = None
            if isinstance(self.tag, str):
                if self.tag == element.tag:
                    matched_tag = element.tag
            elif isinstance(self.tag, set):
                if any([element.tag == tag for tag in self.tag]):
                    matched_tag = element.tag
            else:
                raise Exception("expected tag is neither a set or str.")

            if not matched_tag:
                reason = f"Required tag: '{self.tag}' does not match actual tag: '{element.tag}'. ({matched_path})"
                return None, reason

        # Match text.
        if self.text:
            required_text = strip_whitespace_and_newlines(self.text)
            actual_text = strip_whitespace_and_newlines(element.text)
            if actual_text != required_text:
                reason = (f"Required text: '{required_text}' does not match actual text: '{actual_text}'. "
                          f"({matched_path})")
                return None, reason

        # Match attributes.
        if self.required_attributes:
            for required_attribute in self.required_attributes:
                if isinstance(required_attribute, str):
                    if element.get(required_attribute) is None:
                        reason = f"Required attribute: '{required_attribute}' is missing. ({matched_path})"
                        return None, reason

                if isinstance(required_attribute, tuple):
                    actual_attribute_value = element.get(required_attribute[0])
                    if actual_attribute_value != required_attribute[1]:
                        reason = (f"Required value {required_attribute[0]}='{required_attribute[1]}'"
                                  f" does not match '{actual_attribute_value}'. ({matched_path})")
                        return None, reason

        if self.forbidden_attributes:
            for forbidden_attribute in self.forbidden_attributes:
                if isinstance(forbidden_attribute, str):
                    if element.get(forbidden_attribute) is not None:
                        reason = f"Forbidden attribute: '{forbidden_attribute}' is present. ({matched_path})"
                        return None, reason

                if isinstance(forbidden_attribute, tuple):
                    actual_attribute_value = element.get(forbidden_attribute[0])
                    if actual_attribute_value == forbidden_attribute[1]:
                        reason = (f"Forbidden attribute value {forbidden_attribute[0]}='{forbidden_attribute[1]}'"
                                  f" is present '{actual_attribute_value}'. ({matched_path})")
                        return None, reason

        # Extract values -- extract values from yourself
        extracted_values = {}
        if self.extract:
            for key in self.extract.keys():
                extraction = self.extract[key]
                if isinstance(extraction, str):
                    extracted_values[key] = element.get(extraction)
                elif isinstance(extraction, Callable):
                    extracted_values[key] = extraction(element)
                else:
                    raise Exception(
                        f"extraction {extraction} is neither a str nor a Callable. ({matched_path})")

        # Match Children.
        if self.children is not None:
            # returns all the extractions of the children, needs to be combined
            reason = ""
            match, child_reason = self.match_children(element, matched_path, extracted_values)
            if match is None:
                reason = f"Could not match any set of children ({matched_path})" + ": " + child_reason
            return match, reason
        else:
            return Match(extracted_values=extracted_values, element=element), ""

    def match_children(
            self, element: Element, matched_path: str, extracted_values: dict[str, Any]
    ) -> tuple[Match | None, str]:
        reason = ""
        if isinstance(self.children, dict):
            for match_children_set_id in self.children.keys():
                children_set = self.children[match_children_set_id]
                match, reason = match_children_set(
                    element=element,
                    matched_path=matched_path,
                    children_set=children_set,
                    set_id=match_children_set_id,
                    extracted_values=extracted_values
                )
                if match is not None:
                    return match, reason
        else:
            raise Exception("Attribute `children` is not of type 'list' or 'dict'.")

        reason = f"Failed to match children: {reason}"
        return None, reason


def match_children_set(element: Element, matched_path: str, children_set: list[MatchElement],
                       set_id: str, extracted_values: dict[str, Any]) -> tuple[Match | None, str]:
    """Compares a list of MatchElements with the children of a given XML Element.

    returns: A tuple consisting of a Match object and a string with an explanation, if no match was found.
    """
    if len(element) != len(children_set):
        reason = f"Expected {len(children_set)} children, found {len(element)}. ({matched_path})"
        return None, reason

    # has to match each child
    child_matches = []
    child_index = 0
    match_index = 0
    while child_index < len(element) and match_index < len(children_set):
        match_element = children_set[match_index]
        repeat_index = 0
        # Match as many matches as possible, within the repeat range.
        while repeat_index < match_element.repeat[1]:
            child_match, child_reason = children_set[child_index].match(
                element=element[child_index], matched_path=matched_path + str(element[child_index].tag)
            )
            if child_match is None:
                if repeat_index < match_element.repeat[0]:
                    # Not enough matches in a rows.
                    reason = f"Expected at least {match_element.repeat[0]} repetitions, got {len(child_matches)}"
                    return None, reason + ": " + child_reason
                else:
                    # At least repeat[0] matches have been found, continue with the next match element.
                    break

            child_matches.append(child_match)
            # Append duplicate keys as list.
            for key, value in child_match.extracted_values.items():
                if key in extracted_values.keys():
                    if isinstance(extracted_values[key], list):
                        extracted_values[key].append(value)
                    else:
                        extracted_values[key] = [extracted_values[key], value]
                else:
                    extracted_values[key] = value

            repeat_index += 1
            child_index += 1

        match_index += 1

    # check if matched
    if len(child_matches) == len(children_set):
        # build match from children

        return Match(
            extracted_values=extracted_values,  # should be like this {"user": [list] if a child has "repeat" on
            element=element,
            set_id=set_id,
            children=child_matches
        ), ""

    return None, f"Could not match all children. (matched {len(child_matches)} / {len(children_set)})"

import logging
from typing import Self

from lxml.etree import _Element

logger = logging.getLogger(__name__)


class MatchElement:
    def __init__(
            self,
            tag: str,
            required_attributes: list[str] = None,
            required_attribute_values: list[tuple[str, any]] = None,
            forbidden_attributes: list[str] = None,
            match_children_sets: dict[str, list[Self]] = None
    ):
        self.forbidden_attributes = forbidden_attributes
        self.required_attribute_values = required_attribute_values
        self.required_attributes = required_attributes
        self.tag = tag
        self.match_children_sets = match_children_sets

    def match(self, element, matched_path: str = "") -> bool:
        # Match tag.
        if self.tag != element.tag:
            logger.debug(f"Required tag: '{self.tag}' does not match actual tag: '{element.tag}'. ({matched_path})")
            return False

        # Match attributes.
        if self.required_attributes:
            for required_attribute in self.required_attributes:
                if element.get(required_attribute) is None:
                    logger.debug(f"Required attribute: '{required_attribute}' is missing. ({matched_path})")
                    return False

        if self.forbidden_attributes:
            for forbidden_attribute in self.forbidden_attributes:
                if element.get(forbidden_attribute) is not None:
                    logger.debug(f"Forbidden attribute: '{forbidden_attribute}' is present. ({matched_path})")
                    return False

        if self.required_attributes:
            for required_attribute, required_attribute_value in self.required_attribute_values:
                actual_attribute_value = element.get(required_attribute)
                if actual_attribute_value != required_attribute_value:
                    logger.debug(
                        f"Required value {required_attribute}='{required_attribute_value}'"
                        f" does not match '{actual_attribute_value}'. ({matched_path})"
                    )
                    return False

        # Match Children.
        if self.match_children_sets is not None:
            matched_set = self.match_children(element, matched_path)
            if matched_set is None:
                logger.debug(f"Could not match any set of children.")
                return False

        return True

    def match_children(self, element: any, matched_path: str) -> str | None:
        reason = ""
        for match_children_set_id in self.match_children_sets.keys():
            children_set = self.match_children_sets[match_children_set_id]
            matched_children_set = True
            if len(element) != len(children_set):
                reason = f"Expected {len(children_set)} children, found {len(element)}. ({matched_path})"
                continue
            for child_index in range(len(element)):
                matched_children_set &= children_set[child_index].match(
                    element=element[child_index], matched_path=matched_path + str(element[child_index].tag)
                )

            if matched_children_set:
                return match_children_set_id

        logger.debug(f"Failed to match children: {reason}.")
        return None

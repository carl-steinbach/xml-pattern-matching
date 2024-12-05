


import math
from xml.etree.ElementTree import Element

from xml_pattern_matching.match import Match


class MatchElementList:
    repeat: tuple[int, int | float] 
    def __init__(
            self,
            *match_elements,
            repeat: int | tuple[int, int | None] = (0, None)
            ):
        """
        Matches a list of elements, using any of the elements from the given set.

        Args:
            match_elements (tuple): The set of elements matched in the list.
            repeat (int | tuple[int, int  |  None], optional): The range defining the required length of the list. Defaults to 1.

        Raises:
            TypeError: Wront type for repet 
            TypeError: Wrong type for match_elements
        """
        self.match_elements = match_elements
        if not isinstance(self.match_elements, tuple):
            raise TypeError("self.match_elements should be a tuple.")
        if isinstance(repeat, int):
            self.repeat = (repeat, repeat)
        elif isinstance(repeat, tuple) and isinstance(repeat[0], int):
            if repeat[1] is None:
                self.repeat = (repeat[0], math.inf)
            elif isinstance(repeat[1], int | float):
                repeat: tuple[int, int | float]
                self.repeat = repeat
            else:
                raise TypeError("repeat[1] has to be an int or None")
        else:
            raise TypeError("repeat has to be a tuple or an int")
        
    def match(self, element: Element, matched_path: str) -> tuple[Match, str]:
        reason: str = "empty set of match_elements"
        for match_element in self.match_elements:
            match, reason = match_element.match(element, matched_path)
            if match is not None:
                return match, ""
            
        return None, reason
    
        
    
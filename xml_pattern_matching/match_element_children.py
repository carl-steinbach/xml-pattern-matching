import math
from xml.etree.ElementTree import Element
from xml_pattern_matching.match import Match
from xml_pattern_matching.signature import SingleMatch, MultiMatch

"""
matchElem:
    repeat(match-element, match-element-set),
    repeat(match-)
    
    
each child has to have a "repeat value"
within each child is a list of atomic match elements
atomic child match elements: match-element, match-element-set RETURN A SINGLE MATCH
"""


class MatchElementSet(SingleMatch):
    """Matches any element from the provided set."""
    def __init__(self, *match_element_set: SingleMatch):
        self.match_element_set = match_element_set
    
    def match(self, element, matched_path: str) -> tuple[Match | None, str]:
        for match_element in self.match_element_set:
            match, last_reason = match_element.match(element, matched_path) # can increase the child index, and consume a number of children, returns the final match index
            if match is not None:
                return match, last_reason

        return None, last_reason
    
    
class MatchElementSequence(MultiMatch):
    """
    Matches an exact sequence of MatchElements and MatchElementSets, by iterating over the children. 
    Returns the incremented child index, if successfull.
    """
    match_element_sequence: list[SingleMatch]
    def __init__(self, *match_element_sequence: SingleMatch):
        self.match_element_sequence = list(match_element_sequence)
    
    def match(self, element: Element, index: int, matched_path: str) -> tuple[list[Match] | None, str, int]:
        start_index = index
        matches = []
        for match_element in self.match_element_sequence:
            match, last_reason = match_element.match(element=element[index], matched_path=matched_path + f"[{index}]") # can increase the child index, and consume a number of children, returns the final match index
            if match is None:
                return None, last_reason, start_index # return start index, because nothing was matched

            matches.append(match)
            # Values are extracted one layer above
            index += 1
            
        return matches, last_reason, index


class MatchElementChild(MultiMatch):
    """
    Matches repetitions of a sequence that may contain any amount of match elements and match element sets.
    A single match element would be represented by setting repeat to (1,1), and only providing one element for the match_element_sequence argument.
    """
    repeat: tuple[int, int | float] 
    match_element_sequence: MatchElementSequence
    
    def __init__(self, *match_element_sequence: SingleMatch, repeat: int | tuple[int, int | None] = (1, 1)):   
        self.match_element_sequence = MatchElementSequence(*match_element_sequence)
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
        

    def match(self, element: Element, index: int, matched_path: str) -> tuple[list[Match] | None, str, int]:
        """Match the element's children, starting at the given index."""
        start_index = index
        repetitions = 0
        matches = []
        while repetitions < self.repeat[1]:
            sequence_matches, last_reason, index = self.match_element_sequence.match(element, index, matched_path + f"[{index}]") # can increase the child index, and consume a number of children, returns the final match index
            if sequence_matches is None:
                if repetitions < self.repeat[0]:
                    # Not enough matches in a rows.
                    reason = f"Expected at least {self.repeat[0]} repetitions, got {repetitions}"
                    return None, reason + ": " + last_reason, start_index
                else:
                    # At least repeat[0] matches have been found, continue with the next match element.
                    break
                
            matches.extend(sequence_matches) 
            repetitions += 1
            
        return matches, "", index
    



from xml.etree.ElementTree import Element

from xml_pattern_matching.match import Match


class MultiMatch:
    def match(self, element: Element, index: int) -> tuple[list[Match] | None, str, int]:
        raise NotImplementedError
    
    
class SingleMatch:
    def match(self, element: Element) -> tuple[Match | None, str]:
        raise NotImplementedError
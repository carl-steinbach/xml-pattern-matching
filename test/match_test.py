import inspect
import sys
import unittest
from xml.etree.ElementTree import ElementTree

from defusedxml.ElementTree import parse


class MatchTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # loads xml from filename of the child instance (only works for direct children)
        file_name = sys.modules[self.__class__.__module__].__file__
        xml_filename = f"{file_name.split(".")[0]}.xml"
        with (open(xml_filename, "r") as xmlfile):
            self.xmltree: ElementTree = parse(xmlfile)

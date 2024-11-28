from xml.etree.ElementTree import ElementTree

from defusedxml.ElementTree import parse


def etree_from_pyfile(pyfile: str) -> ElementTree:
    """
    Loads an XML etree given a python file path.
    Assumes the file is in the same directory and shares the same filename.
    """
    xml_filename = f"{pyfile.split(".")[0]}.xml"
    with (open(xml_filename, "r") as xmlfile):
        return parse(xmlfile)

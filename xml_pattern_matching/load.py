from xml.etree.ElementTree import ElementTree
from defusedxml.ElementTree import parse


def etree_from_pyfile(pyfile: str) -> ElementTree:
    xml_filename = f"{pyfile.split(".")[0]}.xml"
    with (open(xml_filename, "r") as xmlfile):
        return parse(xmlfile)

from xml_pattern_matching.match_element import MatchElement
from xml.etree.ElementTree import Element
from xml_pattern_matching import load, utils


def main():
    etree = load.etree_from_pyfile(__file__)
    root = etree.getroot()

    print("hey")
    print(root.get("class"))
    print(len(root))
    print(root.text)

    print(utils.format_element(element=root))


if __name__ == "__main__":
    main()

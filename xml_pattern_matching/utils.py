from xml.etree.ElementTree import Element


def format_element(element: Element):
    """Returns a shortened string format of the element, with children info up to depth 2."""
    fmt = f"<{element.tag}"
    for attribute in element.keys():
        fmt += f" {attribute}='{element.get(attribute)}'"
    fmt += ">"
    fmt += element.text
    for child, index in enumerate(element):
        child: Element
        print(f"\tchild [{index}]: {child}")

        for sub_index, sub_child in enumerate(child.getchildren()):
            print(f"\t\tsub_child [{sub_index}]: {sub_child}")

    fmt += f"<{element.tag}/>"
    return fmt

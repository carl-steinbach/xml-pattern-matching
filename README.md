# XML Pattern Matching

Matching conditional XML patterns using minimal input.
Allows selecting required tags, attributes & values, and matching children recursively in a conditional
branched based format.

Uses the standard [Python XML library](https://docs.python.org/3/library/xml.html#module-xml)
and the [defusedxml](https://pypi.org/project/defusedxml/) package.

## Installation

`pip install git+https://github.com/carl-steinbach/xml-pattern-matching.git`

## Usage

Assume we would like to extract a value from a users account information that is represented in either of two formats, A
and B.

```xml
<!-- Layout A -->
<div>
    <span>Account Information</span>
    <div>
        <div>user@example.com</div>
        <div>
            <div>
                129429.2931 <!-- target data -->
            </div>
        </div>
    </div>
</div>
```

```xml
<!-- Layout B -->
<div>
    <span>Account Information</span>
    <div>
        <span>129429.2931</span> <!-- target data -->
        <div>user@example.com</div>
    </div>
</div>
```

The target can be extracted like so

```python
from xml.etree.ElementTree import Element

import defusedxml.ElementTree

from xml_pattern_matching.match_element import MatchElement

with open("account_information.xml", "r") as xmlfile:
    xmltree = defusedxml.ElementTree.parse(xmlfile)


# Provide custom functions for extracting values from elements.
def extract_account_number(element: Element) -> int:
    return int(element.text.strip().split(".")[0])


# Construct the matching structure using a MatchElement.
match_element = MatchElement(
    tag="div",
    children=[
        MatchElement(
            tag="span",
            text="Account Information"
        ),
        MatchElement(
            tag="div",
            children={  # Match either layout A or B from the subtree, by providing a dictionary instead of a list.
                "layout_A": [
                    MatchElement("div"),
                    MatchElement(
                        tag="div",
                        children=[
                            MatchElement(
                                tag="div",
                                extract={
                                    "account_number": extract_account_number
                                }
                            )
                        ]
                    )
                ],
                "layout_B": [
                    MatchElement(
                        tag="span",
                        extract={
                            "account_number": extract_account_number
                        }
                    ),
                    MatchElement("div")
                ]
            }
        )
    ]
)

# Matching.
match = match_element.match(xmltree.getroot())

account_number = match.extracted_values["account_number"]
print(f"extracted account number: {account_number}")

# Prints the full tree of the match, along with which sets where matched and where which information was extracted.
print(match)


```

---

_version_ 0.0.3

_author_ Carl Steinbach

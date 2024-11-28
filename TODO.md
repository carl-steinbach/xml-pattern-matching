# TODO

## Planned Work

- [x] Extracting values directly from the xml structure
- [x] Children could be list or dict
- [ ] combine forbidden attributes with required attributes using ("forbidden_attribute", None)
- [ ] make children matching more flexible (ordered, unordered, required / forbidden)
  solution could be to include "flat" children sets within a children list directly, rather than nesting them

## Future Work

- consider replacing or at least augmenting the matching with Xpath
- consider providing the match config as a flavour of xml like so, but: how to do conditional branches in here?

attributes would be replaced by a json string
attribute={"exact_value": "value"} or {"regex":".*"} or {"type": "float"}, but this approach can not use custom
matching functions easily.

extraction, optional matching and conditionals could be done via reserved tags and attributes.

MatchXML:
```xml
<div>
    <div class='{"type": "string"}' num='{"type": "int"}' wild='{"exists": true}'>
        <span match-extract='{"label": "attribute", "label2": "attribute2"}'>
            <match-extract label="extracted_value"/> <!-- custom extract tag -->
        </span>
    </div>
    <div>
        <match-set label="A"> <!-- custom tag to define conditionals -->
            <div/>
            <span/>
        </match-set>
        <match-set label="B">
            <div/>
            <span/>
        </match-set>
    </div>
</div>
```

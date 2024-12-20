# TODO


## Planned Work
- [ ] make the extraction dict typeable, so that parsers can provide a type for how its supposed to look, that could be enforced an used for type hints on the extraction result.
- [ ] Add a forbidden child to the "Set"
- [ ] Convenience class for representing an optional MatchElement or MatchElementSet, 
- [ ] Let an element have multiple extractions, or let an extraction return multiple values
- [ ] Improve the signatures for SingleMatch and MultiMatch


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

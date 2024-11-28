# TODO

## Planned Work
- [x] Extracting values directly from the xml structure 
- [ ] make children matching more flexible (ordered, unordered, required / forbidden)
Like so:
```
[ 
    child
    child
    optional: child
    child
    (set:
        tag attr children
        child
        child
    ) 
        OR 
    (set:
        tag, attr, children
        child 
        child
    )
    
```
solution could be to include "flat" children sets within a children list directly, rather than nesting them


## Future Work
- consider replacing or at least augmenting the matching with Xpath
- consider providing the match config as a flavour of xml like so, but: how to do conditional branches in here?

```
    <div class: string = any num: int = any wild: any = any>
      <span>${EXTRACT_VALUE}</span>
    </div>
    
    with conditional:
    <div> 
        <div></div> 
        $OR
        <span></span>
    </div>
```

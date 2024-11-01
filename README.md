# Magazine

Let your code take comprehensive notes and publish notes and figures as a beautiful consolidated PDF document.

## Idea

The magazine package helps you to create beautiful PDF reports of what has been done during the execution of your app. 
1. Your scripts or submodules can write *Stories* in plain human-readable text, which could also include numerical results or figures, for instance.  
2. The collection of stories can be used to *Publish* a glossy PDF document.

## Example

```python
from magazine import Story, Publish

E = 42
Story.report("Experiment", "The analysis found that energy equals {} Joule.", E)

with Publish("Report.pdf", "My physics report", info="Version 0.1") as M:
    M.add_story("Experiment")
```


## Install

```bash
pip install magazine
```

Requires:
- loguru
- fpdf2


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
Story.cite("10.1002/andp.19163540702")

with Publish("Report.pdf", "My physics report", info="Version 0.1") as M:
    M.add_story("Experiment")
    M.add_references()
```

- View the resulting magazine in [output/Report.pdf](https://github.com/mschroen/magazine/blob/main/output/Report.pdf).
- Check also `example.py` for more examples.

## Install

```bash
pip install magazine
```

Requires:
- fpdf2
- habanero (for academic citations)
- neatlogger (wrapper for loguru)

## Acknowledgements

- Uses the Google font [Roboto](https://fonts.google.com/specimen/Roboto) as it just looks great in PDFs.
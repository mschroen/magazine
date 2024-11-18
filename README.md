# Magazine
[![PyPi Version](https://img.shields.io/pypi/v/magazine.svg)](https://pypi.python.org/pypi/magazine/)
[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/mschroen/magazine/blob/main/LICENSE)
[![Read the Docs](https://readthedocs.org/projects/magazine/badge/?version=latest)](https://magazine.readthedocs.io/en/latest/?badge=latest)
[![Issues](https://img.shields.io/github/issues-raw/mschroen/magazine.svg?maxAge=25000)](https://github.com/mschroen/magazine/issues)  
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
- Check also [example.py](https://github.com/mschroen/magazine/blob/main/example.py) and [output/Magazine.pdf](https://github.com/mschroen/magazine/blob/main/output/Magazine.pdf) for more examples.

![Example output PDF report](https://github.com/mschroen/magazine/blob/main/docs/magazin-preview.png)


## Documentation

A documentation and API reference can be found on [ReadTheDocs](https://magazine.readthedocs.io/en/latest):
- [Story](https://magazine.readthedocs.io/en/latest/#magazine.story.Story) (class)
- [Publish](https://magazine.readthedocs.io/en/latest/#magazine.publish.Publish) (context manager)
- [PDF commands](https://magazine.readthedocs.io/en/latest/#magazine.publish.PDF) (class)

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
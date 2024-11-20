# Magazine
[![PyPi Version](https://img.shields.io/pypi/v/magazine.svg)](https://pypi.python.org/pypi/magazine/)
[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/mschroen/magazine/blob/main/LICENSE)
[![Read the Docs](https://readthedocs.org/projects/magazine/badge/?version=latest)](https://magazine.readthedocs.io/en/latest/?badge=latest)
[![Issues](https://img.shields.io/github/issues-raw/mschroen/magazine.svg?maxAge=25000)](https://github.com/mschroen/magazine/issues)  
Let your code take comprehensive notes and publish notes and figures as a beautiful consolidated PDF document.

## Idea

The magazine package helps you to create beautiful PDF reports of what has been done during the execution of your app. 
1. Your scripts or submodules can write topical reports in plain human-readable text, which could also include numerical results, data tables, figures, or citations.
2. The collection of topics can be used to publish a glossy PDF document.

## Example

```python
from magazine import Magazine, Publish

E = 42
Magazine.report("Experiment", "The analysis found that energy equals {} Joule.", E)
Magazine.cite("10.1002/andp.19163540702")

with Publish("Report.pdf", "My physics report", info="Version 0.1") as M:
    M.add_topic("Experiment")
    M.add_references()
```

- View the resulting magazine in [output/Report.pdf](https://github.com/mschroen/magazine/blob/main/output/Report.pdf).

Instead of inline commands, you can also use a *decorator* to automatically write and format the content of the docstring section "Report" and its "References" section into the report.

```python
@Magazine.reporting("Physics")
def Method_A(a, b, c=3):
    """
    A complex method to calculate the sum of numbers.

    Report
    ------
    The method "{function}" used input parameters {args}, and c={c}.
    Calculations have been performed following Einstein et al. (1935).
    The result was: {return}. During the process, the magic number {magic} appeared.

    References
    ----------
    Einstein, A., Podolsky, B., & Rosen, N. (1935). Can Quantum-Mechanical Description of Physical Reality Be Considered Complete? Physical Review, 47(10), 777–780. https://doi.org/10.1103/physrev.47.777

    """
    result = a + b + c

    # Function "_report" is provided by the decorator to communicate more variables
    _report["magic"] = 42

    return result

# When the function is called, it is automatically reported.
Method_A(2, 3, c=4)
```
Output in the PDF:
> The method "Method_A" used input parameters (2, 3), and c=4. Calculations have been performed following Einstein et
al. (1935). The result was: 9. During the process, the magic number 42 appeared.

Check also [example.py](https://github.com/mschroen/magazine/blob/main/example.py) and [output/Magazine.pdf](https://github.com/mschroen/magazine/blob/main/output/Magazine.pdf) for more full examples.

![Example output PDF report](https://github.com/mschroen/magazine/blob/main/docs/magazine-preview.png)


## Documentation

A documentation and API reference can be found on [ReadTheDocs](https://magazine.readthedocs.io/en/latest):
- [Magazine](https://magazine.readthedocs.io/en/latest/#magazine.magazine.Magazine) (class)
- [Publish](https://magazine.readthedocs.io/en/latest/#magazine.publish.Publish) (context manager)
- [PDF commands](https://magazine.readthedocs.io/en/latest/#magazine.publish.PDF) (class)

## Install

```bash
pip install magazine
```

Requires:
- fpdf2
- habanero (optional, for academic citations)
- neatlogger (wrapper for loguru)

## Acknowledgements

- Uses the Google font [Roboto](https://fonts.google.com/specimen/Roboto) as it just looks great in PDFs.
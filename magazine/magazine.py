import io
import sys
import numpy as np
import re
from functools import wraps
from textwrap import dedent

from neatlogger import log


class SafeDict(dict):
    """
    A variant of dict that does not raise an error for missing keys.
    Thanks to: https://stackoverflow.com/a/17215533/2575273

    Example
    -------
    >>> parameters = SafeDict(a=1, b=2)
    ... print(parameters["a"], parameters["c"])
    1 {c}

    """

    def __missing__(self, key):
        return "{" + key + "}"


class Magazine:
    """
    Can be used to log information in a human-readable way.
    Supports different report topics.
    The list of topics can be later posted as a composite string.
    Useful for writing reports with class Publish().

    Examples
    --------
    >>> Magazine.report("observations", "Temperature today was {:.2f}.", None)
    ... Magazine.report("observations", "Data was corrected following {:}, only {:d} points remained.", "Brown et al. (1979)", 42)
    ... Magazine.post("observations")
    Temperature today was nan. Data was corrected following Brown et al. (1979), only 42 points remained.

    """

    topics = dict()
    figures = dict()
    references = []
    dois = []
    active = False

    def __init__(self):
        pass

    @staticmethod
    def turn_on():
        """Turns on Magazine reporting"""
        Magazine.active = True

    @staticmethod
    def turn_off():
        """Truns off Magazine reporting"""
        Magazine.active = False

    @staticmethod
    def assert_topic(topic: str):
        """
        Makes sure that the topic exists in dict before appending.
        Intialized as empty list per topic.

        Parameters
        ----------
        topic: str
            Name of an existing or new topic

        Examples
        --------
        >>> Magazine.assert_topic("Experiments")
        ... Magazine.topics["Experiments"]
        []

        """
        if not topic in Magazine.topics:
            Magazine.topics[topic] = []
            Magazine.figures[topic] = []

    @staticmethod
    def report(topic="default", message="", *values):
        """
        Appends a text or image to the topic's list.
        The text is checked for Nonetype values before.

        Parameters
        ----------
        topic: str
            Name of an existing or new topic
        message: str | io.BytesIO
            Text or bytes object (to store figures)
        *values
            Any number of values to be inserted into the formatted message

        Examples
        --------
        >>> Magazine.report("Experiments", "Today is {}.", "Monday")

        """
        if not Magazine.active:
            return

        Magazine.assert_topic(topic)

        if isinstance(message, str):
            # normal text
            if values:
                # Replace all None by np.nan to avoid NoneType Error on formatting
                values = [np.nan if v is None else v for v in values]
                message = message.format(*values)

            Magazine.topics[topic].append(message)

        elif isinstance(message, io.BytesIO):
            # figure object
            Magazine.figures[topic].append(message)

        else:
            log.warning("Nothing to report: message is neither text nor image.")

    @staticmethod
    def cite(*refs):
        """
        Appends a reference to the Magazine that can be later converted to a reference list.

        Parameters
        ----------
        *refs: str
            Any number of reference texts.
            If it looks like a doi, it will be stored in a separate list which is used to download full texts by collect_references().

        Examples
        --------
        >>> Magazine.cite("10.5194/hess-27-723-2023", "10.1029/2021gl093924")
        >>> Magazine.cite("Einstein, A. (1916). Die Grundlage der allgemeinen Relativitätstheorie. Annalen Der Physik, 354(7), 769–822. Portico")

        """
        if not Magazine.active:
            return

        doi_pattern = r"^10[.][0-9]{4,}"

        for ref in refs:
            if re.search(doi_pattern, ref):
                Magazine.dois.append(ref)
            else:
                Magazine.references.append(ref)

    @staticmethod
    def post(*topics) -> str:
        """
        Joins the topic's list on a single space.

        Parameters
        ----------
        *topics: str
            Any number of existing topics

        Returns
        -------
        str
            Merged topic texts.

        Examples
        --------
        >>> paragraph = Magazine.post("Experiments", "Methods")
        """
        # if isinstance(topic, str):
        #     topic = [ topic ]
        text = []
        for topic in topics:
            Magazine.assert_topic(topic)
            text.append(" ".join(Magazine.topics[topic]))

        return " ".join(text)

    @staticmethod
    def figure(*topics) -> list:
        """
        Joins the topic's figures to a combined flat list.

        Parameters
        ----------
        *topics: str
            Any number of existing topics

        Returns
        -------
        list
            Merged topic figures.

        Examples
        --------
        >>> all_figures = Magazine.figure("Experiments", "Methods")

        """
        # if isinstance(topic, str):
        #     topic = [ topic ]
        figures = []
        for topic in topics:
            Magazine.assert_topic(topic)
            for figure in Magazine.figures[topic]:
                figures.append(figure)

        return figures

    @staticmethod
    def collect_references() -> list:
        """
        Lists all items in Magazine.references.
        Downloads the full reference text for all items in Magazine.dois

        Returns
        -------
        list
            List of reference texts, sorted by name.

        Examples
        --------
        >>> for item in Magazine.collect_references():
        ...     print(item)

        """
        reflist = Magazine.references

        if len(Magazine.dois) > 0:

            Magazine.dois = list(set(Magazine.dois))  # remove duplicates
            log.progress("Collecting {} citations from CrossRef...", len(Magazine.dois))
            from habanero import cn

            reflist2 = cn.content_negotiation(ids=Magazine.dois, format="text")
            if isinstance(reflist2, str):
                reflist2 = [reflist2]
            reflist2 = [ref.rstrip() for ref in reflist2 if ref is not None]
            reflist += reflist2

        reflist.sort()
        return reflist

    @staticmethod
    def clean():
        """
        Cleans topics, figures, references, and dois to make space for a new Magazine.
        """
        Magazine.topics = dict()
        Magazine.figures = dict()
        Magazine.references = []
        Magazine.dois = []
        return

    new = clean

    class reporting:
        def __init__(
            self,
            topic,
        ):
            """
            Decorator to report input, output, and other variables.

            Parameters
            ----------
            topic (str): The topic (i.e., story title) in the Magazine under which the content will be printed.

            """
            self.topic = topic
            self.parameters = SafeDict()

        def __call__(self, func):
            @wraps(func)
            def wrapper(*args, **kwargs):

                if not Magazine.active:
                    result = func(*args, **kwargs)
                    return result

                local_vars = {}

                def trace_calls(frame, event, arg):
                    if event == "return":
                        # Capture locals when function is returning
                        local_vars.update(frame.f_locals)
                    return trace_calls

                # Set up the trace
                old_trace = sys.gettrace()
                sys.settrace(trace_calls)

                try:
                    result = func(*args, **kwargs)
                finally:
                    sys.settrace(old_trace)

                self.parameters.update(
                    {
                        "function": func.__name__,
                        "return": result,
                    }
                )

                for key, val in local_vars.items():
                    self.parameters[key] = val

                self._parse_docstring(func.__doc__)
                return result

            return wrapper

        def _parse_docstring(self, docstring):
            """Parses the docstring for Report and References sections."""

            if docstring:
                # Report
                # ------
                report_pattern = r"Report\s+\-+\n(.*?)(?:\n\n|\Z)"
                report_match = re.search(report_pattern, docstring, re.DOTALL)
                if report_match:
                    report_text = report_match.group(1)
                    report_text = report_text.format_map(self.parameters)
                    report_text = dedent(report_text)
                    # remove single newlines
                    report_text = re.sub(r"(?<!\n)\n(?!\n)", " ", report_text)
                    Magazine.report(self.topic, report_text)

                # References
                # ----------
                refs_pattern = r"References\s+\-+\n(.*?)(?:\n\n|\Z)"
                refs_match = re.search(refs_pattern, docstring, re.DOTALL)
                if refs_match:
                    refs_text = refs_match.group(1)
                    refs_text = dedent(refs_text)
                    # Create list from lines
                    refs_list = refs_text.split("\n")
                    Magazine.cite(*refs_list)

            else:
                log.warning(
                    "No docstring provided for function {}.",
                    self.parameters["function"],
                )

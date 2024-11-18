import io
import numpy as np
from neatlogger import log


class Story:
    """
    Can be used to log information in a human-readable way.
    Supports different story categories.
    The list of reports can be later posted as a composite string.
    Useful for writing reports with class Publish().
    
    Examples
    --------
    >>> J = Story()
    ... J.report("observations", "Temperature today was {:.2f}.", None)
    ... J.report("observations", "Data was corrected following {:}, only {:d} points remained.",
    ...     "Brown et al. (1979)", 42)
    ... J.post("observations")
    Temperature today was nan. Data was corrected following Brown et al. (1979), only 42 points remained.

    """

    stories = dict()
    figures = dict()
    references = []

    def __init__(self):
        # self.story = dict()
        # self.figures = dict()
        pass

    @staticmethod
    def assert_category(category: str):
        """
        Makes sure that the category exists in dict before appending.
        Intialized as empty list per category.

        Parameters
        ----------
        category: str
            Name of an existing or new category

        Examples
        --------
        >>> Story.assert_category("Experiments")
        ... Story.stories["Experiments"]
        []

        """
        if not category in Story.stories:
            Story.stories[category] = []
            Story.figures[category] = []

    @staticmethod
    def report(category="default", message="", *values):
        """
        Appends a text or image to the category's list.
        The text is checked for Nonetype values before.

        Parameters
        ----------
        category: str
            Name of an existing or new category
        message: str | io.BytesIO
            Text or bytes object (to store figures)
        *values
            Any number of values to be inserted into the formatted message

        Examples
        --------
        >>> Story.report("Experiments", "Today is {}.", "Monday")

        """
        Story.assert_category(category)

        if isinstance(message, str):
            # normal text
            if values:
                # Replace all None by np.nan to avoid NoneType Error on formatting
                values = [np.nan if v is None else v for v in values]
                message = message.format(*values)

            Story.stories[category].append(message)

        elif isinstance(message, io.BytesIO):
            # figure object
            Story.figures[category].append(message)

        else:
            log.warning("Nothing to report: message is neither text nor image.")

    @staticmethod
    def cite(*dois):
        """
        Appends a DOI to the story that canbe later converted to a reference list.

        Parameters
        ----------
        *dois: str
            Any number of DOIs

        Examples
        --------
        >>> Story.cite("10.5194/hess-27-723-2023", "10.1029/2021gl093924")

        """
        for doi in dois:
            Story.references.append(doi)

    @staticmethod
    def post(*categories) -> str:
        """
        Joins the category's list on a single space.

        Parameters
        ----------
        *categories: str
            Any number of existing categories
        
        Returns
        -------
        str
            Merged category texts.

        Examples
        --------
        >>> paragraph = Story.post("Experiments", "Methods")
        """
        # if isinstance(category, str):
        #     category = [ category ]
        text = []
        for category in categories:
            Story.assert_category(category)
            text.append(" ".join(Story.stories[category]))

        return " ".join(text)

    @staticmethod
    def figure(*categories) -> list:
        """
        Joins the category's figures to a combined flat list.

        Parameters
        ----------
        *categories: str
            Any number of existing categories
        
        Returns
        -------
        list
            Merged category figures.

        Examples
        --------
        >>> all_figures = Story.figure("Experiments", "Methods")

        """
        # if isinstance(category, str):
        #     category = [ category ]
        figures = []
        for category in categories:
            Story.assert_category(category)
            for figure in Story.figures[category]:
                figures.append(figure)

        return figures

    @staticmethod
    def collect_references() -> list:
        """
        Looks up the reference text for all items in Story.references.

        Returns
        -------
        list
            List of reference texts, sorted by name.
        
        Examples
        --------
        >>> for item in Story.collect_references():
        ...     print(item)

        """
        log.progress("Collecting {} citations from CrossRef...", len(Story.references))
        from habanero import cn

        reftexts = cn.content_negotiation(ids=Story.references, format="text")
        if isinstance(reftexts, str):
            reftexts = [reftexts]
        reftexts = [ref.rstrip() for ref in reftexts if ref is not None]
        reftexts.sort()
        return reftexts

    @staticmethod
    def clean():
        """
        Cleans stories, figures, and references to make space for a new story.
        """
        Story.stories = dict()
        Story.figures = dict()
        Story.references = []
        return

    new = clean

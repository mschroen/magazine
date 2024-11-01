import io
import numpy as np
from neatlogger import log


class Story:
    """
    Scope:
        Can be used to log information during the processing.
        Supports different story categories.
        The list of reports can be later posted as a composite string.
        Useful for writing reports with class Report().
    Feature:
        Supports Nonetype values to be formatted gracefully.
    Usage:
        J = Story()
        ...
        J.report("observations",
            "Temperature today was {:.2f}.",
            None)
        ...
        J.report("observations",
            "Data was corrected following {:}, only {:d} points remained.",
            ("Brown et al. (1979)", 42))
        ...
        J.post("observations")

    Returns:
        Temperature today was nan. Data was corrected
        following Brown et al. (1979), only 42 points remained.
        #return("%s%.0f" % (x.f_code, x.f_lineno))
    """

    stories = dict()
    figures = dict()

    def __init__(self):
        # self.story = dict()
        # self.figures = dict()
        pass

    @staticmethod
    def assert_category(category):
        """
        Makes sure that the category exists in dict before appending.
        Intialized as empty list per category.
        """
        if not category in Story.stories:
            Story.stories[category] = []
            Story.figures[category] = []

    @staticmethod
    def report(category="default", message="", *values):
        """
        Appends a text or image to the category's list.
        The text is checked for Nonetype values before.
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
    def post(*categories) -> str:
        """
        Joins the category's list on a single space.
        """
        # if isinstance(category, str):
        #     category = [ category ]
        text = []
        for category in categories:
            Story.assert_category(category)
            text.append(" ".join(Story.stories[category]))

        return " ".join(text)

    @staticmethod
    def figure(*categories) -> str:
        """
        Joins the category's list on a single space.
        """
        # if isinstance(category, str):
        #     category = [ category ]
        figures = []
        for category in categories:
            Story.assert_category(category)
            for figure in Story.figures[category]:
                figures.append(figure)

        return figures

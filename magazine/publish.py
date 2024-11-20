from datetime import datetime
import pandas as pd
from neatlogger import log

from magazine import Magazine
from magazine.io import get_file_size, assert_directory, get_script_directory


# Requires FPDF, https://py-pdf.github.io/fpdf2/
import fpdf

# log.getLogger("fpdf.svg").propagate = False


class Publish:
    """
    Context manager to write all reports, figures, and references into a PDF file.
    Uses FPDF2 to return a PDF class.

    Parameters
    ----------
    filename : str
        Full path and name of the PDF file.
    title : str, optional
        Title to be written in the header, by default ""
    info : str, optional
        Any info to be written in the header, e.g. a version number, by default ""
    datetime_fmt : str, optional
        How to format the datetime in the header, by default "%Y-%m-%d %H:%M"
    page_numbers : bool, optional
        Whether or not to show page numbers, by default True

    Returns
    -------
    PDF
        An instance that inherits from fpdf.FPDF to provide commands to add content to the PDF.

    Examples
    --------
    >>> with Magazine.Publish("example.pdf", "My Title") as M:
    ...     M.add_page()
    ...     M.add_title("Chapter 1)
    ...     M.add_paragraph("Long text")
    ...     M.add_image(figure)
    ...     M.add_table(data)

    """

    def __init__(
        self,
        filename: str,
        title: str = "",
        info: str = "",
        datetime_fmt: str = "%Y-%m-%d %H:%M",
        page_numbers: bool = True,
    ):
        self.filename = filename
        self.file_format = filename[filename.rindex(".") + 1 :].lower()
        self.title = title
        self.info = info
        self.page_numbers = page_numbers
        self.datetime_fmt = datetime_fmt
        self.magazine = None

    def __enter__(self):
        if self.file_format == "pdf":
            self.magazine = PDF(
                self.title, self.info, self.datetime_fmt, self.page_numbers
            )
            return self.magazine
        else:
            log.error(
                "The requested magazine format is not supported: {}", self.file_format
            )
            return None

    def __exit__(self, type, value, traceback):
        if self.magazine is None:
            pass
        else:
            assert_directory(self.filename)
            self.magazine.output(self.filename)
            log.success(
                "Magazine published: {} ({})",
                self.filename,
                get_file_size(self.filename, human_readable=True),
            )


######################
class PDF(fpdf.FPDF):
    """
    PDF writer and wrapper for FPDF

    Examples
    --------
    >>> pdf = PDF()
    ... pdf.header_text = "My title"
    ... pdf.add_page()
    ... pdf.output("my_title.pdf")

    Notes
    -----
    Thanks to: https://py-pdf.github.io/fpdf2/Maths.html

    """

    # These variables can be changed individually if necessary
    cell_height = 8
    header_text = ""
    font = "Roboto"
    font_mono = "RobotoM"  # "Courier" # Helvetica
    font_size = 10
    ln0 = dict(new_x=fpdf.enums.XPos.RIGHT, new_y=fpdf.enums.YPos.TOP)
    ln1 = dict(new_x=fpdf.enums.XPos.LMARGIN, new_y=fpdf.enums.YPos.NEXT)

    def __init__(
        self,
        title: str = "",
        info: str = "",
        datetime_fmt: str = "",
        page_numbers: bool = True,
    ):
        super().__init__()

        self.title = title
        self.info = info
        self.datetime_fmt = datetime_fmt
        self.page_numbers = page_numbers

        self.header_text = self.title

        # fonts
        font_folder = get_script_directory() + "/fonts/"
        # font_folder = os.path.dirname(os.path.abspath(__file__)) + "/../app/_ui/fonts/"
        self.add_font("Roboto", "", font_folder + "Roboto-Regular.ttf")
        self.add_font("Roboto", "B", font_folder + "Roboto-Bold.ttf")
        self.add_font("RobotoM", "", font_folder + "RobotoMono-Regular.ttf")
        self.add_font("RobotoM", "B", font_folder + "RobotoMono-Bold.ttf")

    def header(self):
        """
        Overwrites the FPDF's header function with a table:
        | %title | %info | %datetime | %page |
        """

        # title
        self.set_font(self.font, "B", self.font_size)
        self.cell(
            self.epw - 35 - 45 - 15,
            8,
            " %s" % self.header_text,
            border=True,
            align="L",
            **self.ln0
        )

        # info
        self.set_font(self.font_mono, "", self.font_size)
        self.cell(35, 8, self.info, border=True, align="C", **self.ln0)

        # datetime
        datetime_str = (
            "" if not self.datetime_fmt else datetime.now().strftime(self.datetime_fmt)
        )
        self.cell(45, 8, datetime_str, border=True, align="C", **self.ln0)

        # page
        page_str = "" if not self.page_numbers else "%2s " % str(self.page_no())
        self.cell(15, 8, page_str, border=True, align="R", **self.ln1)
        self.ln(self.cell_height)

    # def footer(self):
    #     self.set_y(-15)
    #     self.set_font('Courier', '', 12)
    #     self.cell(0, 8, f'Page {self.page_no()}', True, align='C', **ln0)

    def add_title(self, title: str = None, style: str = "B"):
        """
        Add a chapter title.

        Parameters
        ----------
        title: str
            Title of the page, can be empty.
        style: str, optional
            Font style, is "B" for bold by default.

        Examples
        --------
        >>> with Publish("example.pdf") as M:
        ...     M.add_title("My title")

        """
        if title is None:
            title = self.header_text
        self.set_font(self.font, style=style, size=24)
        self.cell(w=0, h=20, text=title, **self.ln1)
        self.set_font(style="", size=self.font_size)
        # self.ln(self.cell_height)

    add_head = add_title

    def add_paragraph(self, text: str = None):
        """
        Add a multiline paragraph.

        Parameters
        ----------
        text: str
            Text to be written.

        Examples
        --------
        >>> with Publish("example.pdf") as M:
        ...     M.add_paragraph("Very long text.")

        """
        if text is None:
            text = ""
        self.multi_cell(w=0, h=5, text=text)
        self.ln(self.cell_height)

    add_text = add_paragraph

    def add_topic(self, topic: str = None, headers: bool = True, new_page: bool = True):
        """
        Shortcut to add a page, title, and topic text.

        Parameters
        ----------
        topic : str
            Topic to take the report from.
        headers : bool, optional
            Write a headline, by default True
        new_page : bool, optional
            Create a new page, by default True

        Examples
        --------
        >>> with Publish("example.pdf") as M:
        ...     M.add_topic("Experiments")
        """
        if new_page:
            self.add_page()
        if headers:
            self.add_title(topic)
        self.add_paragraph(Magazine.post(topic))

    def add_image(
        self,
        source=None,
        x: float = None,
        y: float = None,
        w: float = None,
        h: float = 0,
        link: str = "",
    ):
        """
        Write an image to PDF.

        Parameters
        ----------
        source : string or object or list of objects, optional
            Can be a file path (png, jpg) or an image buffer or a list of them., by default None
        x : float, optional
            x coords of image, by default None
        y : float, optional
            y coords of image, by default None
        w : float, optional
            width of image, by default None
        h : float, optional
            height of image, scales automatically with width, by default 0
        link : str, optional
            link for the image, by default ""

        Examples
        --------
        >>> image_object = io.BytesIO()
        ... plt.savefig(image_object, format="svg")
        ... with Publish("example.pdf") as M:
        ...     M.add_image(image_object)
        ...     M.add_image("image_file.png")

        """

        if w is None:
            w = self.epw

        if not isinstance(source, list):
            source = [source]

        for obj in source:
            if obj:
                self.image(obj, x=x, y=y, w=w, h=h, link=link)
                self.ln(self.cell_height)

    def add_figure(
        self, topic: str = None, headers: bool = False, new_page: bool = False
    ):
        """
        Write all figures of a topic to the PDF.

        Parameters
        ----------
        topic : str, optional
            Existing topic, by default None
        headers : bool, optional
            Add a topic headline before the figure, by default False
        new_page : bool, optional
            Create a new page, by default False

        Examples
        --------
        >>> image_object = io.BytesIO()
        ... plt.savefig(image_object, format="svg")
        ... Magazine.report("Experiments", image_object)
        ... with Publish("example.pdf") as M:
        ...     M.add_figure("Experiments")

        """
        if new_page:
            self.add_page()
        if headers:
            self.add_title(topic)
        self.add_image(Magazine.figure(topic))

    def add_table(
        self, data: pd.DataFrame = None, align: str = "RIGHT", index: bool = False
    ):
        """
        Add a table for a pandas DataFrame.

        Parameters
        ----------
        data : pd.DataFrame, optional
            DataFrame to print to the PDF, by default None
        align : str, optional
            Alignment of the cell text, by default "RIGHT"
        index : bool, optional
            Whether or not to display the index column, by default False

        Examples
        --------
        >>> data = pd.DataFrame({"name":["Tim", "Tom"], "age":[12,13]})
        ... with Publish("example.pdf") as M:
        ...     M.add_table(data, index=True)

        """
        self.set_font(self.font_mono, size=7)

        if "Date" in data.columns:
            data["Date"] = data.index.strftime("%Y-%m-%d")
        if index:
            data[data.index.name] = data.index

        cols = list(data.columns)
        cols = [cols[-1]] + cols[:-1]
        data = data[cols]

        data = data.astype(str)
        columns = [list(data)]  # Get list of dataframe columns
        rows = data.values.tolist()  # Get list of dataframe rows
        data = columns + rows  # Combine columns and rows in one list

        with self.table(
            borders_layout="SINGLE_TOP_LINE",
            cell_fill_color=245,
            cell_fill_mode="ROWS",
            line_height=self.font_size * 0.5,
            text_align=align,
            width=self.epw,
        ) as table:
            for data_row in data:
                row = table.row()
                for datum in data_row:
                    row.cell(datum)

        self.set_font(self.font, style="", size=self.font_size)
        self.ln(self.cell_height)

    def add_references(self, headers: str = "References", new_page: bool = True):
        """
        Create a list of references that were previously added by Magazine.cite()
        This function will look up the full citations text using the habanero package.

        Parameters
        ----------
        headers : str, optional
            Title of the references page, by default "References"
        new_page : bool, optional
            Whether or not to add a new page, by default True

        Examples
        --------
        >>> Magazine.cite("10.1029/2021gl093924")
        ... with Publish("example.pdf") as M:
        ...     M.add_references()

        """

        if new_page:
            self.add_page()
        if headers:
            self.add_title("References")

        reftexts = Magazine.collect_references()

        # for ref in reftexts:
        #   self.add_paragraph(ref)
        self.add_paragraph("\n\n".join(reftexts))

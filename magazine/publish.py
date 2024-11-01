from datetime import datetime
from neatlogger import log

from magazine import Story
from magazine.io import get_file_size, assert_directory, get_script_directory


# Requires FPDF
# https://py-pdf.github.io/fpdf2/
# Todo: Update to PyPdf 3.*
# https://pypdf.readthedocs.io/en/latest/search.html?q=&check_keywords=yes&area=default
import fpdf

# log.getLogger("fpdf.svg").propagate = False


class Publish:
    """
    Usage:
        with magazine.Publish("example.pdf", "My Title") as M:
            M.add_page()
            M.add_title("Chapter 1)
            M.add_paragraph("Long text")
            M.add_image(figure)
            M.add_table(data)
            ...
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
    Usage:
        pdf = PDF()
        pdf.header_text = "My title"
        pdf.add_page()
        ...
        pdf.output("my_title.pdf")

    Credits:
        Thanks to https://py-pdf.github.io/fpdf2/Maths.html
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
        Overwrites FPDF's header function.
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

    def add_title(self, title=None, style="B"):
        """
        Add a chapter title
        """
        if title is None:
            title = self.header_text
        self.set_font(self.font, style=style, size=24)
        self.cell(w=0, h=20, text=title, **self.ln1)
        self.set_font(style="", size=self.font_size)
        # self.ln(self.cell_height)

    add_head = add_title

    def add_paragraph(self, text=None):
        """
        Add a multiline paragraph.
        """
        if text is None:
            text = ""
        self.multi_cell(w=0, h=5, text=text)
        self.ln(self.cell_height)

    add_text = add_paragraph

    def add_story(self, category=None, headers=True, new_page=True):
        if new_page:
            self.add_page()
        if headers:
            self.add_title(category)
        self.add_paragraph(Story.post(category))

    def add_image(self, source=None, x=None, y=None, w=None, h=0, link=""):
        """
        Can be a file path (png, jpg) or an image buffer or a list of them.
        For image buffers use before:
            img_buf = BytesIO()
            plt.savefig(img_buf, format="svg")
        Or use Corny:
            from corny.figures import Figure
            with Figure(size=(5,5), save="buff") as F:
                ax = F.axes
                ax.scatter(data=df)
            img_buf = F.buff
        """
        if w is None:
            w = self.epw

        if not isinstance(source, list):
            source = [source]

        for obj in source:
            if obj:
                self.image(obj, x=x, y=y, w=w, h=h, link=link)
                self.ln(self.cell_height)

    def add_figure(self, category=None, headers=False, new_page=False):
        if new_page:
            self.add_page()
        if headers:
            self.add_title(category)
        self.add_image(Story.figure(category))

    def add_table(self, data=None, align="RIGHT", index=False):
        """
        Add a table, just provide a pandas DataFrame
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

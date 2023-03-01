from datetime import date
from io import BytesIO
from pathlib import Path

import fitz
import httpx

NYT_FRONTPAGE_URL = "https://static01.nyt.com/images/{year_month_day}/nytfrontpage/scan.pdf"
OUTPUT_LOCATION = "frontpage"
OUTPUT_NAME = "nyt.png"
DPI = 800


class FrontPageProcessor:
    def __call__(self):
        today = date.today()

        self.assure_output_location()
        stream: BytesIO = self.fetch_frontpage(today)
        self.save_frontpage(stream)

    def assure_output_location(self) -> None:
        output_path = Path(OUTPUT_LOCATION)
        if not output_path.exists():
            output_path.mkdir()

    def fetch_frontpage(self, date: date) -> BytesIO:
        year_month_day = date.strftime(r"%Y/%m/%d")  # YYYY/MM/DD
        url = NYT_FRONTPAGE_URL.format(year_month_day=year_month_day)

        response = httpx.get(url)
        response.raise_for_status()

        return BytesIO(response.content)

    def save_frontpage(self, stream: BytesIO) -> None:
        with fitz.open(stream=stream, filetype="pdf") as pdf_doc:
            frontpage = pdf_doc[0]  # there is only one page
            image = frontpage.get_pixmap(dpi=DPI)  # grayscale desired.
            image.save(f"{OUTPUT_LOCATION}/{OUTPUT_NAME}")


processor = FrontPageProcessor()

processor()

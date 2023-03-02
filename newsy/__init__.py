from datetime import date
from io import BytesIO
from pathlib import Path

import fitz
import httpx

NYT_FRONTPAGE_URL = "https://static01.nyt.com/images/{year_month_day}/nytfrontpage/scan.pdf"
OUTPUT_LOCATION = "frontpage"
OUTPUT_NAME = "nyt.png"
DPI = 300


class FrontPageProcessor:
    def __call__(self):
        today = date.today()

        print("assuring output location.")
        self.assure_output_location()

        print("fetching frontpage")
        stream: BytesIO = self.fetch_frontpage(today)

        print("saving frontpage")
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
            image = pdf_doc.get_page_pixmap(0, matrix=fitz.Matrix(1.75, 1.75))
            image.save(f"{OUTPUT_LOCATION}/{OUTPUT_NAME}")


processor = FrontPageProcessor()

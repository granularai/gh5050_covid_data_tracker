import requests
from bs4 import BeautifulSoup
import pandas as pd
from googletrans import Translator
from io import StringIO

import re

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

from covid_data_tracker.plugins.base import BasePlugin

class RomaniaPlugin(BasePlugin):

    COUNTRY = "Romania"
    BASE_URL = "https://www.cnscbt.ro/"
    BASE_SOURCE = "https://www.cnscbt.ro/index.php/analiza-cazuri-confirmate-covid19/"
    TYPE = "PDF"

    def fetch(self):
        self.local_filename = '/tmp/Romania.pdf'
        with requests.get(self.BASE_SOURCE, stream=True) as r:
            r.raise_for_status()
            with open(self.local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        self.parsed_text = self.parse_text()

    def parse_text(self):
        output_string = StringIO()
        with open(self.local_filename, 'rb') as in_file:
            parser = PDFParser(in_file)
            doc = PDFDocument(parser)
            rsrcmgr = PDFResourceManager()
            laparams = LAParams(word_margin=0.1, detect_vertical=True,
                                all_texts=True)
            device = TextConverter(rsrcmgr, output_string, laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)

        return output_string.getvalue()

    def download(self):
        print (self.parsed_text)
        identifier = 'Caracteristici\n\nn\n\n%\n\n'
        loc = self.parsed_text.find(identifier) + len(identifier)
        next_identifier = '\n\nVarsta'
        next_loc = self.parsed_text.find(next_identifier)
        columns = self.parsed_text[loc:next_loc].split('\n\n')
        all = []
        for column in columns:
            column_splitted = list(map(str, column.split('\n')))
            cleaned = []
            for row in column_splitted:
                if '(' not in row:
                    if row.isdigit():
                        cleaned.append(int(row))
                    else:
                        cleaned.append(float(row))
            all.append(cleaned)

        self.sex_table['absolute_cases']['male'] = all[0][0]
        self.sex_table['percent_cases']['male'] = all[3][0]
        self.sex_table['absolute_healthcare_workers_infected']['total'] = all[0][-1]
        self.sex_table['percent_healthcare_workers_infected']['total'] = all[3][-1]
        self.sex_table['absolute_deaths']['male'] = all[1][0]
        self.sex_table['absolute_deaths']['male'] = all[4][0]

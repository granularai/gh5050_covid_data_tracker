import requests
from urllib.parse import urljoin
from io import StringIO
from bs4 import BeautifulSoup
import re

import pandas as pd
import numpy as np

from googletrans import Translator

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
    UNIQUE_SOURCE = "https://www.cnscbt.ro/index.php/analiza-cazuri-confirmate-covid19/1804-raport-saptamanal-episaptamana23"
    TYPE = "PDF"
    AUTHOR = "Sagar Verma"
    FREQUENCY = "weekly"
    ARCHIVE_AVAILABLE = "True"

    def fetch(self):
        self.get_dates()
        self.local_filename = './Romania.pdf'
        self.DATE = self.dates[0][0]
        with requests.get(self.dates[0][1], stream=True) as r:
            r.raise_for_status()
            with open(self.local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        self.parsed_text =  "\n".join([ll.rstrip() for ll in self.parse_text().splitlines() if ll.strip()])
        identifier = 'Caracteristici\nn\n%\n'
        loc = self.parsed_text.find(identifier) + len(identifier)
        next_identifier = '\nVarsta'
        next_loc = self.parsed_text.find(next_identifier)
        values = self.parsed_text[loc:next_loc].split('\n')
        self.sex_table['absolute_cases']['male'] = int(values[1])
        self.sex_table['percent_cases']['male'] = float(values[15])
        self.sex_table['absolute_healthcare_workers_infected']['total'] = int(values[4])
        self.sex_table['percent_healthcare_workers_infected']['total'] = float(values[18])
        self.sex_table['absolute_deaths']['male'] = int(values[6])
        self.sex_table['percent_deaths']['male'] = float(values[20])


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

    def get_dates(self):
        archive = requests.get(self.BASE_SOURCE)
        archive_parsed = BeautifulSoup(archive.text)
        table = archive_parsed.find_all('table')[0]
        hrefs = []
        for tag in zip(table.find_all('a', attrs={'class':'docman_download__button'}),
                       table.find_all('time', attrs={'itemprop':'datePublished'})):

            link = np.where(tag[0].has_attr('href'), tag[0].get('href'), "no link")
            date = np.where(tag[1].has_attr('datetime'), tag[1].get('datetime'), "date")

            if 'raport-saptamanal-episaptamana' in str(link):
                hrefs.append([date, str(link)])
        self.dates = [[a[0], urljoin(self.BASE_URL, str(a[1]))] for a in hrefs]

import importlib
import pandas as pd


class BasePlugin:

    COUNTRY : str = ""

    def __init__(self):
        self.tables = []

    def fetch(self):
        raise NotImplementedError

    def download(self):
        if not self.COUNTRY:
            raise NotImplementedError
        else:
            count = 0
            for table in self.tables:
                count += 1
                table.to_csv(f"./{self.COUNTRY}_{count}.csv")

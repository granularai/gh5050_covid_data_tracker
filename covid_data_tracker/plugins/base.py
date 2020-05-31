import importlib
import pandas as pd


CLASS_MAP = {
    'Germany': 'GermanyPlugin'
}

def class_selector(selected_country : str):
    if selected_country in CLASS_MAP.keys():
        class_name = CLASS_MAP[selected_country]
        module_name = f"covid_data_tracker.plugins.countries.{class_name}"
        print(module_name)
        module = importlib.import_module(module_name)
        class_ = getattr(module, class_name)
        instance = class_()
        # class_name = CLASS_MAP[selected_country]
        # module = __import__(f"covid_data_tracker.plugins.countries.{class_name}")
        # print(module)
        # class_ = getattr(module, class_name)
        # instance = class_()
        return instance
    else:
        print('nope')


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

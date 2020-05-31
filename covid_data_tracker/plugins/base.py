class BasePlugin:
    """A base plugin that serves as a template for country-specific plugins.

    Attributes
    ----------
    tables: [pandas.DataFrame]

    COUNTRY: str
        Country definition
    SOURCE: str
        The source being evaluated
    TYPE: str
        The source type (pdf, )

    """

    COUNTRY: str = ""
    SOURCE: str = ""
    TYPE: str = ""
    PluginRegistry = {}

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.PluginRegistry[cls.COUNTRY] = cls

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

    def get_info(self):
        return [['Country Information'],["COUNTRY", self.COUNTRY],
                ["SOURCE", self.SOURCE],
                ["TYPE", self.TYPE]]

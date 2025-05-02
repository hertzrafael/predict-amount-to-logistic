import pandas as pd
import os

class Conversor:

    def __init__(self, file, default=False):
        self.file = file
        self.needed_cols = [
            'CODPROD', 'NUMOS', 'DTINICIOOS'
        ]
        self.default = default

    def convert(self):
        extension = self.file.name.split('.')[-1]

        conversors = {
            'xlsx': self.__read_excel__,
            'csv': self.__read_csv__
        }

        if not extension in conversors:
            return None
        
        return self.__transform__(conversors[extension]())

    def __transform__(self, frame):
        return frame.astype({
            'CODPROD': str
        })

    def __get_path__(self):
        return os.path.join("files", "PCMOVENDPEND_FILTERED.csv") if self.default else self.file

    def __read_excel__(self):
        return pd.read_excel(self.__get_path__(), usecols=self.needed_cols, engine='openpyxl')
    
    def __read_csv__(self):
        return pd.concat(pd.read_csv(self.__get_path__(), usecols=self.needed_cols, chunksize=5000))
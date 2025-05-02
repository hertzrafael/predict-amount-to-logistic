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
        print('p1')
        extension = 'csv'

        if self.file:
            extension = self.file.name.split('.')[-1]
            print('p2')

        conversors = {
            'xlsx': self.__read_excel__,
            'csv': self.__read_csv__
        }
        print('p3')

        if not extension in conversors:
            return None
        
        print('p4')
        
        frame = self.__transform__(conversors[extension]())
        print(frame)

        return frame

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
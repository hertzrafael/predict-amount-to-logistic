import pandas as pd

class Conversor:

    def __init__(self, file):
        self.file = file
        self.needed_cols = [
            'CODPROD', 'NUMOS', 'DTINICIOOS'
        ]

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

    def __read_excel__(self):
        return pd.read_excel(self.file, usecols=self.needed_cols, engine='openpyxl')
    
    def __read_csv__(self):
        return pd.concat(pd.read_csv(self.file, usecols=self.needed_cols, chunksize=5000))
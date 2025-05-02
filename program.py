import pandas as pd

class Program:

    def __init__(self, streamlit):
        self.st = streamlit

    def __get_uploaded_frame__(self):
        return self.st.session_state.get('uploaded_frame')
    
    def get_best_sellers_in_seasons(self):
        frame = self.__get_uploaded_frame__()
        season = (frame
            .filter(items=['CODPROD', 'NUMOS', 'DTINICIOOS'])
            .assign(
                DTINICIOOS=lambda x: pd.to_datetime(x['DTINICIOOS'], errors='coerce'),
                TEMPORADA=lambda x: x['DTINICIOOS'].dt.month.map({
                    12: 'Verão', 1: 'Verão', 2: 'Verão',
                    3: 'Outono', 4: 'Outono', 5: 'Outono',
                    6: 'Inverno', 7: 'Inverno', 8: 'Inverno',
                    9: 'Primavera', 10: 'Primavera', 11: 'Primavera'
                })
            )
        )

        return (season
            .groupby(['TEMPORADA', 'CODPROD'])
            .size()
            .reset_index(name='QUANTIDADE')
            .sort_values(['TEMPORADA', 'QUANTIDADE'], ascending=[True, False])
        )
    
    def get_best_sellers(self):
        frame = self.get_best_sellers_in_seasons()

        idx = frame.groupby('TEMPORADA')['QUANTIDADE'].idxmax()
        return frame.loc[idx].reset_index(drop=True)
    
    def filter_frame_by_season(self, frame, season):
        return frame.query(f'TEMPORADA == "{season}"')
        

import streamlit as st
import pandas as pd

from types import ModuleType
from program import Program
from conversor import Conversor
from predict import PredictProducts

class Pages:

    def __init__(self, streamlit: ModuleType, program: ModuleType):
        self.st: st = streamlit
        self.program: Program = program

    def __get_uploaded_frame__(self):
        return self.st.session_state.get('uploaded_frame')

    def main(self):
        self.st.title('Produtos Mais Vendidos')
        frame = self.__get_uploaded_frame__()

        if frame is None:
            self.st.header('Nenhum arquivo foi upado.')
            self.st.text('Faça o upload na nossa aba "Dados".')
            return
        
        with st.expander('🛈 Informações sobre a tabela', expanded=False):
            st.markdown(r"""
                
                Na tabela abaixo, é possível visualizar o produto que é mais vendido em cada uma das estações do ano. É levado em consideração
                os dados carregados na aba 'Dados' da nossa página.
                        
                Dessa forma, o gestor pode ter alguma ideia de quais produtos são mais vendidos em determinada época e se preparar para a
                compra destes produtos, como, por exemplo, a busca de um fornecedor mais acessível e que ofereça um maior conforto financeiro.
                
                ## Glossário:
                - TEMPORADA: Estação do ano.
                - CODPROD: Código do produto.
                - QUANTIDADE: Quantidade distríbuida do produto.
            """)
        
        dataframe = self.program.get_best_sellers()
        self.st.dataframe(dataframe, hide_index=True, use_container_width=True)
        self.st.divider()

        first_col, second_col = self.st.columns(2)

        with first_col:
            season = st.selectbox(
                "Estação do ano",
                self.program.get_best_sellers_in_seasons()['TEMPORADA'].unique(),
            )

        with second_col:
            amount = st.number_input("Insira a quantidade de registros:", value=10, min_value=0, step=1)

        best_sellers_in_season = self.program.filter_frame_by_season(
            self.program.get_best_sellers_in_seasons(),
            season
        )

        st.dataframe(best_sellers_in_season.head(amount), hide_index=True, use_container_width=True,)

    def upload(self):
        self.st.title('Insira aqui os seus dados')

        default = 'uploaded_frame' not in st.session_state
        conversor = Conversor(file, default=default)

        file = self.st.file_uploader('Faça o upload aqui:', type=['csv'], )
        file_name = None
        if file:
            file_name = file.name

            with self.st.spinner("Aguarde enquanto o arquivo é carregado..."):
                self.program.__save_session_frame__(conversor, file_name)
                
        else:
            if 'file_name' in self.st.session_state:
                file_name = self.st.session_state['file_name']
            else:
                self.program.__save_session_frame__(conversor)

        self.st.text(f'Arquivo upado atualmente: {file_name or 'Nenhum'}')
    
    def predict(self):
        self.st.title('Preveja as quantidades')
        frame = self.__get_uploaded_frame__()

        if frame is None:
            self.st.header('Nenhum arquivo foi upado.')
            self.st.text('Faça o upload na nossa aba "Dados".')
            return
        
        with st.expander('🛈 Informações sobre a predição', expanded=False):
            st.markdown(r"""
                
                Para realizar a predição da quantidade necessária de produtos, utilizamos o modelo Random Forest Regression e treinamos este
                com os dados fornecidos pelo usuário em nossa aba 'Dados'. Dessa forma, conseguimos prever uma quantidade estimada de produtos
                para determinada estação do ano para que o gestor se prepare. Lembre-se que, quantos mais dados o modelo tiver, mais precisa 
                deve ser a previsão.
                
                ## Glossário:
                - CODPROD: Código do produto.
                - PRED_QUANTIDADE: Quantidade estimada de produtos a serem distribuídos.
            """)
        
        first_col, second_col = self.st.columns(2)

        with first_col:
            season = st.selectbox(
                "Estação do ano",
                self.program.get_best_sellers_in_seasons()['TEMPORADA'].unique(),
            )

        with second_col:
            amount = st.number_input("Insira a quantidade de registros:", value=10, min_value=0, step=1)

        predict = PredictProducts(self.program.get_best_sellers_in_seasons())
        st.dataframe(predict.predict_best_sellers(season).head(amount), hide_index=True, use_container_width=True)

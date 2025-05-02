import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

class PredictProducts:

    def __init__(self, df):
        self.df_original = df
        self.df = df.copy()

        self.season_encoder = LabelEncoder()
        self.product_encoder = LabelEncoder()

        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.preprocess()
        self.train_model()

    def preprocess(self):
        self.df['TEMPORADA_ENC'] = self.season_encoder.fit_transform(self.df['TEMPORADA'])
        self.df['CODPROD_ENC'] = self.product_encoder.fit_transform(self.df['CODPROD'])

        self.X = self.df[['TEMPORADA_ENC', 'CODPROD_ENC']]
        self.y = self.df['QUANTIDADE']

    def train_model(self):
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)

    def predict_best_sellers(self, season):
        temporada_enc = self.season_encoder.transform([season])[0]

        codprods = self.df_original['CODPROD'].unique()
        codprods_enc = self.product_encoder.transform(codprods)

        entrada = pd.DataFrame({
            'TEMPORADA_ENC': [temporada_enc] * len(codprods),
            'CODPROD_ENC': codprods_enc
        })

        predicoes = self.model.predict(entrada)
        resultados = pd.DataFrame({
            'CODPROD': codprods,
            'PRED_QUANTIDADE': predicoes
        }).sort_values(by='PRED_QUANTIDADE', ascending=False)

        return resultados
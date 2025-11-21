from .base import Lottery
from .data_manager import DataManager
import pandas as pd

class MegaSena(Lottery):
    def __init__(self):
        super().__init__(
            name="Mega Sena",
            data_url="https://raw.githubusercontent.com/aretw0/loterias-caixa-db/refs/heads/main/data/megasena.csv",
            slug="megasena"
        )

    def load_data(self) -> pd.DataFrame:
        self.data = DataManager.load_csv(self.data_url)
        return self.data

    def preprocess_data(self) -> pd.DataFrame:
        if self.data is None:
            self.load_data()
            
        df = self.data.copy()
        
        # Rename columns
        column_mapping = {
            'Data do Sorteio': 'data',
        }
        df = df.rename(columns=column_mapping)
        
        # Convert to datetime
        df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
        
        # Combine balls into a list
        bola_cols = [f'Bola{i}' for i in range(1, 7)]
        df['dezenas'] = df[bola_cols].values.tolist()
        
        self.data = df
        return df

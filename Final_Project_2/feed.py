import pandas as pd
from sqlalchemy import create_engine
from catboost import CatBoostClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import pickle

SQLALCHEMY_DATABASE_URL = "postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml"
CHUNKSIZE = 30000


# Функция для получения данных из базы данных
def get_data_from_db(url):
    engine = create_engine(url)
    DATA_GB = f"""SELECT pg_size_pretty(pg_total_relation_size('feed_action')) AS table_size;
            """
    DATA = f"""SELECT COUNT(*) AS row_count FROM feed_action;
                """

    DF_size = pd.read_sql(DATA, engine)
    DATA_G = pd.read_sql(DATA_GB, engine)

    return DATA_G, DF_size

if __name__ == "__main__":
    DATA_G, DF_size = get_data_from_db(SQLALCHEMY_DATABASE_URL)
    print("feed_action")
    print(DATA_G)
    print(DF_size)

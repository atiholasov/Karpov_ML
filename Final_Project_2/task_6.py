import pandas as pd
from sqlalchemy import create_engine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

SQLALCHEMY_DATABASE_URL = "postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml"
CHUNKSIZE = 10000
engine = create_engine(SQLALCHEMY_DATABASE_URL)


# def get_data_from_db(url, chunksize):
#     engine = create_engine(url)
#     DATA = f"""SELECT user_id
#                 FROM feed_action
#                 """
#     return pd.read_sql(DATA, engine, chunksize=chunksize)
#
#
# for DF_chunk in get_data_from_db(SQLALCHEMY_DATABASE_URL, CHUNKSIZE):
#
#     DF_chunk.to_sql('alexey_tiholasov_features_lesson_22', con=engine, if_exists='replace', index=False)


def batch_load_sql(query: str) -> pd.DataFrame:
    CHUNKSIZE = 20000

    SQLALCHEMY_DATABASE_URL = "postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    conn = engine.connect().execution_options(stream_results=True)
    chunks = []

    for chunk_dataframe in pd.read_sql(query, conn, chunksize=CHUNKSIZE):
        chunks.append(chunk_dataframe)
    conn.close()
    return pd.concat(chunks, ignore_index=True)


def load_features() -> pd.DataFrame:
    query = "SELECT * FROM alexey_tiholasov_features_lesson_22"
    return batch_load_sql(query)

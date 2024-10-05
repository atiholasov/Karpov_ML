import pandas as pd
from sqlalchemy import create_engine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

SQLALCHEMY_DATABASE_URL = "postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml"
CHUNKSIZE = 200000


def get_data_from_db(url, chunksize):
    engine = create_engine(url)
    DATA = f"""SELECT *
            FROM feed_action f
            JOIN post p on f.user_id = p.id
            JOIN "user" u on f.user_id = u.id
            """
    DF = pd.read_sql(DATA, engine, chunksize=chunksize)
    return DF

def prepare_data(DF_chunk):
    DF_chunk.drop(columns=["post_id", "id"], inplace=True)
    new_column_order = ["user_id", "gender", "age", "country", "city", "exp_group", "os", "source", "text", "topic",
                        "time", "action"]
    DF_chunk = DF_chunk.reindex(columns=new_column_order)

    DF_chunk['time'] = pd.to_datetime(DF_chunk['time'])
    DF_chunk['year'] = DF_chunk['time'].dt.year
    DF_chunk['month'] = DF_chunk['time'].dt.month
    DF_chunk['day'] = DF_chunk['time'].dt.day
    DF_chunk['hour'] = DF_chunk['time'].dt.hour
    DF_chunk = DF_chunk.drop(columns=['time'])

    return DF_chunk

DF = get_data_from_db(SQLALCHEMY_DATABASE_URL, CHUNKSIZE)


text_features = ['text']
categorical_features = ['country', 'city', 'os', 'source', 'topic']
numeric_features = ['gender', 'age', 'exp_group', 'year', 'month', 'day', 'hour']


preprocessor = ColumnTransformer(
    transformers=[
        ('text', TfidfVectorizer(max_features=500), 'text'),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
        ('num', StandardScaler(), numeric_features)
    ]
)

# Применение препроцессора (преобразуем текстовые, категориальные и числовые данные)
df_preprocessed = preprocessor.fit_transform(DF)

# Преобразуем предобработанные данные в DataFrame
df_preprocessed = pd.DataFrame(df_preprocessed)

# Добавляем user_id к предобработанным данным
df_final = pd.concat([user_ids.reset_index(drop=True), df_preprocessed], axis=1)

# Запись признаков в таблицу базы данных
df_final.to_sql('alexey_tiholasov_features_lesson_22', con=engine, if_exists='replace', index=False)






def batch_load_sql(query: str) -> pd.DataFrame:
    CHUNKSIZE = 200000

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

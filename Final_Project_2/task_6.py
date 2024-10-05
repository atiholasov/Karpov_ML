import pandas as pd
from sqlalchemy import create_engine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder


SQLALCHEMY_DATABASE_URL = "postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml"
engine = create_engine(SQLALCHEMY_DATABASE_URL)


df_features = pd.DataFrame({
    'user_id': [1, 2, 3],
    'text': ['text1', 'text2', 'text3'],
    'country': ['country1', 'country2', 'country3'],
    'city': ['city1', 'city2', 'city3'],
    'os': ['os1', 'os2', 'os3'],
    'source': ['source1', 'source2', 'source3'],
    'topic': ['topic1', 'topic2', 'topic3'],
    'gender': [0, 1, 0],
    'age': [23, 45, 31],
    'exp_group': [1, 2, 1],
    'year': [2023, 2023, 2023],
    'month': [9, 9, 9],
    'day': [1, 2, 3],
    'hour': [12, 14, 16]
})


user_ids = df_features[['user_id']]


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
df_preprocessed = preprocessor.fit_transform(df_features)

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

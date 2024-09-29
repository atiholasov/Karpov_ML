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
def get_data_from_db(url, chunksize):
    engine = create_engine(url)
    DATA = f"""SELECT *
            FROM feed_action f
            JOIN post p on f.user_id = p.id
            JOIN "user" u on f.user_id = u.id
            """
    DF = pd.read_sql(DATA, engine, chunksize=chunksize)
    return DF


# Функция для подготовки данных
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


# Функция для разбиения данных на X и y
def split_X_Y(DF_chunk):
    X = DF_chunk[[col for col in DF_chunk.columns if col != 'action']]
    y = DF_chunk["action"]
    return X, y


# Основной код для обучения модели
if __name__ == "__main__":
    DF = get_data_from_db(SQLALCHEMY_DATABASE_URL, CHUNKSIZE)

    # Определение текстовых, категориальных и числовых признаков
    text_features = ['text']
    categorical_features = ['country', 'city', 'os', 'source', 'topic']
    numeric_features = ["user_id", 'gender', 'age', 'exp_group', 'year', 'month', 'day', 'hour']

    # Создание пайплайна для обработки данных
    preprocessor = ColumnTransformer(
        transformers=[
            ('text', TfidfVectorizer(max_features=500), 'text'),  # Обработка текстов через TF-IDF
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),  # Категориальные через OneHotEncoder
            ('num', StandardScaler(), numeric_features)  # Числовые признаки через StandardScaler
        ]
    )

    # Создаем общий пайплайн с обработкой признаков и обучением модели
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('catboost', CatBoostClassifier(learning_rate=0.02, iterations=1000))
    ])

    all_data = []
    all_labels = []

    # Собираем все данные и метки для обучения
    for df_chunk in DF:
        df_chunk_prepared = prepare_data(df_chunk)
        X_chunk, y_chunk = split_X_Y(df_chunk_prepared)
        all_data.append(X_chunk)
        all_labels.append(y_chunk)

    # Конкатенируем все чанки данных
    all_data = pd.concat(all_data, ignore_index=True)
    all_labels = pd.concat(all_labels, ignore_index=True)

    # Обучение модели на всех данных
    pipeline.fit(all_data, all_labels)

    # Сохранение модели
    with open('models/pipeline_with_tfidf.pkl', 'wb') as f:
        pickle.dump(pipeline, f)

    print("Модель с TF-IDF и дополнительными признаками сохранена.")

import pandas as pd
from sqlalchemy import create_engine
from catboost import CatBoostClassifier, Pool
from sklearn.feature_extraction.text import TfidfVectorizer

SQLALCHEMY_DATABASE_URL = "postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml"
CHUNKSIZE = 30000

# BD_tables = ['post', 'user', 'feed_action']

def get_data_from_db(url, chunksize):
    engine = create_engine(url)
    DATA = f"""SELECT *
            FROM feed_action f
            JOIN post p on f.user_id = p.id
            JOIN "user" u on f.user_id = u.id
            LIMIT 100000
            """
    DF = pd.read_sql(DATA, engine, chunksize=chunksize)
    return DF


def prepare_data(DF_chunk, tfidf):
    DF_chunk.drop(columns=["post_id"], inplace=True)
    DF_chunk.drop(columns=["id"], inplace=True)
    new_column_order = ["user_id", "gender", "age", "country", "city", "exp_group", "os", "source", "text", "topic",
                        "time", "action"]
    DF_chunk = DF_chunk.reindex(columns=new_column_order)
    DF_chunk['time'] = pd.to_datetime(DF_chunk['time'])
    DF_chunk['year'] = DF_chunk['time'].dt.year
    DF_chunk['month'] = DF_chunk['time'].dt.month
    DF_chunk['day'] = DF_chunk['time'].dt.day
    DF_chunk['hour'] = DF_chunk['time'].dt.hour
    DF_chunk = DF_chunk.drop(columns=['time'])

    # Преобразуем текст в признаки TF-IDF с использованием ранее обученного tfidf
    tfidf_matrix = tfidf.transform(DF_chunk['text']).toarray()
    tfidf_df = pd.DataFrame(tfidf_matrix, columns=[f'tfidf_{i}' for i in range(tfidf_matrix.shape[1])])

    # Соединяем TF-IDF столбцы с исходными данными
    DF_chunk = pd.concat([DF_chunk.drop(columns=['text']), tfidf_df], axis=1)

    return DF_chunk


def info_about_ind_for_text_and_cat(columns):
    #ind_text = [columns.index('text')]
    category_fitch = ["country", "city", "os", "source", "topic"]
    ind_cat = [index for index, value in enumerate(columns) if value in category_fitch]
    #return ind_text, ind_cat
    return ind_cat


def spliting_X_Y(DF_chunk):
    X = DF_chunk[[col for col in DF_chunk.columns if col != 'action']]
    y = DF_chunk["action"]

    X_train = X
    y_train = y
    X_test = 1
    y_test = 2

    # train_test_border = int(-CHUNKSIZE / 4)
    # X_train = X.iloc[:train_test_border].copy()
    # y_train = y.iloc[:train_test_border].copy()
    # X_test = X.iloc[train_test_border:].copy()
    # y_test = y.iloc[train_test_border:].copy()

    return X_train, y_train, X_test, y_test

if __name__ == "__main__":

    DF = get_data_from_db(SQLALCHEMY_DATABASE_URL, CHUNKSIZE)

    # Собираем все тексты для тренировки TF-IDF на всех данных
    all_texts = []
    for df_chunk in DF:
        all_texts.extend(df_chunk['text'].tolist())

    # Инициализируем и тренируем TF-IDF на всех данных
    tfidf = TfidfVectorizer(max_features=500)
    tfidf.fit(all_texts)

    model = None

    # Повторный проход по чанкам данных для обучения модели
    for df_chunk in get_data_from_db(SQLALCHEMY_DATABASE_URL, CHUNKSIZE):
        DF_chunk = prepare_data(df_chunk, tfidf)
        X_train, y_train, X_test, y_test = spliting_X_Y(DF_chunk)
        ind_cat = info_about_ind_for_text_and_cat(X_train.columns.tolist())

        pool = Pool(X_train, label=y_train, cat_features=ind_cat)

        if model is None:
            model = CatBoostClassifier(learning_rate=0.02, iterations=5000)
            model.fit(pool)
        else:
            model.fit(pool, init_model=model)

    if model is not None:
        model.save_model('models/catboost_model_300', format="cbm")
    else:
        print("Model was not trained.")


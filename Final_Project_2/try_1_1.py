import pandas as pd
from sqlalchemy import create_engine
from catboost import CatBoostClassifier, Pool
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, roc_auc_score, confusion_matrix)

from task_1_1 import (SQLALCHEMY_DATABASE_URL, CHUNKSIZE,
                      get_data_from_db, prepare_data, info_about_ind_for_text_and_cat, spliting_X_Y)

CHUNKSIZE = 40000

DF = get_data_from_db(SQLALCHEMY_DATABASE_URL, CHUNKSIZE)

# Инициализируем списки для накопления предсказаний и истинных меток
all_y_true = []
all_y_pred = []
all_y_pred_proba = []

CHUNK_IND = 1

# Загрузка модели один раз
from_file = CatBoostClassifier()
from_file.load_model("models/catboost_model_300_unlimited")

for df_chunk in DF:
    # Подготовка данных
    DF_chunk = prepare_data(df_chunk)
    X_train, y_train, X_test, y_test = spliting_X_Y(DF_chunk)
    ind_cat = info_about_ind_for_text_and_cat(X_train.columns.tolist())

    # Создание пула для тестирования
    test_pool = Pool(X_test, cat_features=ind_cat)

    # Предсказания и вероятности
    y_pred = from_file.predict(test_pool)
    y_pred_proba = from_file.predict_proba(test_pool)

    # Накопление предсказаний и истинных значений
    all_y_true.extend(y_test)
    all_y_pred.extend(y_pred)
    all_y_pred_proba.extend(y_pred_proba)

    # Печать статистики для текущего чанка
    # accuracy = accuracy_score(y_test, y_pred)
    # precision = precision_score(y_test, y_pred, average='weighted', zero_division=1)
    # recall = recall_score(y_test, y_pred, average='weighted')
    # f1 = f1_score(y_test, y_pred, average='weighted')
    # roc_auc = roc_auc_score(pd.get_dummies(y_test), y_pred_proba, multi_class='ovr')
    # cm = confusion_matrix(y_test, y_pred)

    # print()
    # print(f"Chunk {CHUNK_IND}")
    # print(f"Accuracy: {accuracy}")
    # print(f"Precision: {precision}")
    # print(f"Recall: {recall}")
    # print(f"F1-score: {f1}")
    # print(f"ROC AUC: {roc_auc}")
    # print(f"Confusion Matrix: \n{cm}")
    #
    # CHUNK_IND += 1

# Финальные метрики на всем датасете
all_y_true = pd.Series(all_y_true)
all_y_pred = pd.Series(all_y_pred)
all_y_pred_proba = pd.DataFrame(all_y_pred_proba)

final_accuracy = accuracy_score(all_y_true, all_y_pred)
final_precision = precision_score(all_y_true, all_y_pred, average='weighted', zero_division=1)
final_recall = recall_score(all_y_true, all_y_pred, average='weighted')
final_f1 = f1_score(all_y_true, all_y_pred, average='weighted')
final_roc_auc = roc_auc_score(pd.get_dummies(all_y_true), all_y_pred_proba, multi_class='ovr')
final_cm = confusion_matrix(all_y_true, all_y_pred)

print("\nFinal Metrics on the whole dataset:")
print(f"Accuracy: {final_accuracy}")
print(f"Precision: {final_precision}")
print(f"Recall: {final_recall}")
print(f"F1-score: {final_f1}")
print(f"ROC AUC: {final_roc_auc}")
print(f"Confusion Matrix: \n{final_cm}")

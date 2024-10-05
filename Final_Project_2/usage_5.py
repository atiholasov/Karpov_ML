import os
import pickle


def get_model_path(path: str) -> str:
    if os.environ.get("IS_LMS") == "1":
        MODEL_PATH = '/workdir/user_input/model'
    else:
        MODEL_PATH = path
    return MODEL_PATH


def load_models():
    model_path = get_model_path("./models/pipeline_with_tfidf.pkl")

    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    return model


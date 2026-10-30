import sys
import os
import joblib
from sklearn.metrics import r2_score

from src.expction import CustomException


def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        joblib.dump(obj, file_path)

    except Exception as e:
        raise CustomException(e, sys)


def load_object(file_path):
    try:
        return joblib.load(file_path)
    except Exception as e:
        raise CustomException(e, sys)


def evaluate_models(X_train, y_train, X_test, y_test, models) -> dict[str, float]:
    try:
        report = {}
        for model_name, model in models.items():
            model.fit(X_train, y_train)
            y_test_pred = model.predict(X_test)
            report[model_name] = float(r2_score(y_test, y_test_pred))

        return report

    except Exception as e:
        raise CustomException(e, sys)
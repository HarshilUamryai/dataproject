import sys
from collections.abc import Mapping
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.compoments.data_transformtion import FEATURE_COLUMNS
from src.unilts import load_object

ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"


class PredictionPipeline:
    def __init__(self, model_path=None, preprocessor_path=None):
        self.model = load_object(model_path or ARTIFACTS_DIR / "model.pkl")
        self.preprocessor = load_object(
            preprocessor_path or ARTIFACTS_DIR / "preprocessor.pkl"
        )

    def predict(self, data: pd.DataFrame | Mapping[str, object]) -> np.ndarray:
        if isinstance(data, pd.DataFrame):
            input_data = data.copy()
        elif isinstance(data, Mapping):
            input_data = pd.DataFrame([data])
        else:
            raise TypeError("Prediction input must be a DataFrame or feature mapping.")

        missing_columns = [
            column for column in FEATURE_COLUMNS if column not in input_data.columns
        ]
        if missing_columns:
            raise ValueError(
                f"Missing required prediction features: {', '.join(missing_columns)}"
            )

        transformed_data = self.preprocessor.transform(input_data[FEATURE_COLUMNS])
        return np.asarray(self.model.predict(transformed_data))


def main():
    print("Enter the student's details to predict their math score.")
    student = {
        "gender": input("Gender (female/male): ").strip(),
        "race/ethnicity": input("Race/ethnicity (for example, group C): ").strip(),
        "parental level of education": input(
            "Parent education (for example, some college): "
        ).strip(),
        "lunch": input("Lunch (standard/free/reduced): ").strip(),
        "test preparation course": input("Test preparation (completed/none): ").strip(),
    }

    for column in ("reading score", "writing score"):
        raw_score = input(f"{column.title()} (0-100): ").strip()
        try:
            score = float(raw_score)
        except ValueError as error:
            raise ValueError(f"{column.title()} must be a number from 0 to 100.") from error
        if not 0 <= score <= 100:
            raise ValueError(f"{column.title()} must be between 0 and 100.")
        student[column] = score

    prediction = PredictionPipeline().predict(student)
    print(f"Predicted math score: {prediction[0]:.1f}")


if __name__ == "__main__":
    main()
import glob
import os
import sys
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.expction import CustomException
from src.Logger import logging


@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    test_data_path: str = os.path.join('artifacts', 'test.csv')
    raw_data_path: str = os.path.join('artifacts', 'data.csv')


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def _resolve_dataset_path(self):
        candidates = [
            PROJECT_ROOT / 'notebook' / 'students.csv',
            PROJECT_ROOT / 'notebook' / 'Students.csv',
            PROJECT_ROOT / 'notebook' / 'student.csv',
            PROJECT_ROOT / 'notebook' / 'Student.csv',
        ]

        for candidate in candidates:
            if candidate.exists():
                return str(candidate)

        matches = [
            Path(path)
            for path in glob.glob(str(PROJECT_ROOT / 'notebook' / '*.csv'), recursive=True)
            + glob.glob(str(PROJECT_ROOT / '**' / '*.csv'), recursive=True)
        ]

        for candidate in matches:
            if 'student' in candidate.name.lower():
                return str(candidate)

        if matches:
            return str(matches[0])

        raise FileNotFoundError(f"Dataset not found under project root: {PROJECT_ROOT}")

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            dataset_path = self._resolve_dataset_path()
            df = pd.read_csv(dataset_path)
            logging.info('Read the dataset as dataframe')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path) or '.', exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info("Train test split initiated")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Ingestion of the data is completed")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    obj = DataIngestion()
    obj.initiate_data_ingestion()


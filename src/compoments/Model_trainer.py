import sys
from dataclasses import dataclass
from pathlib import Path

from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.tree import DecisionTreeRegressor

from src.expction import CustomException
from src.Logger import logging
from src.unilts import evaluate_models, save_object

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = str(
        Path(__file__).resolve().parents[2] / "artifacts" / "model.pkl"
    )

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()


    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info("Split training and test input data")
            X_train,y_train,X_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )
            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "AdaBoost Regressor": AdaBoostRegressor(),
            }
            model_report = evaluate_models(
                X_train=X_train,
                y_train=y_train,
                X_test=X_test,
                y_test=y_test,
                models=models,
            )
            logging.info(f"Model Report: {model_report}")

            ## To get best model score from dict
            best_model_score = max(model_report.values())

            ## To get best model name from dict

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]

            if best_model_score<0.6:
                raise CustomException(
                    f"No model met the minimum R2 score of 0.6; best score was "
                    f"{best_model_score:.4f}"
                )
            logging.info(
                f"Best model found: {best_model_name} with R2 score: "
                f"{best_model_score:.4f}"
            )

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted=best_model.predict(X_test)

            r2_square = r2_score(y_test, predicted)
            logging.info(f"Final test R2 score: {r2_square:.4f}")
            return r2_square

        except Exception as e:
            raise CustomException(e,sys)
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from pathlib import Path
from src.components.data_transformation import DataTransformation,DataTransformationConfig
from src.components.model_trainer import ModelTrainer,ModelTrainerConfig

@dataclass
class DataIngestionConfig:
    train_data_path: str =os.path.join('artifact','train.csv')
    test_data_path: str =os.path.join('artifact','test.csv')
    raw_data_path: str =os.path.join('artifact','data.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()
    
    def intiate_data_ingestion(self):
        logging.info("Entered into data ingestion stage!")
        try:
            #MLProjects/noteboook/data/StudentsPerformance.csv
            data_path=Path('noteboook/data/StudentsPerformance.csv')
            #print('Curent CWD',os.getcwd())
            df=pd.read_csv(data_path)
            logging.info(f'Dataframe is created from dataset : {data_path}')
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path, index=False,header=True)
            logging.info("Train test split intiated")
            train_set,test_set = train_test_split(df,test_size=0.2, random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path, index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False,header=True)

            logging.info("Ingestion os the data is completed")
            

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )

        except Exception as e:
            raise CustomException(e, sys)

if __name__=='__main__':


    obj=DataIngestion()
    train_data,test_data=obj.intiate_data_ingestion()

    data_transformation=DataTransformation()
    train_array,test_array,_=data_transformation.intiate_data_transformation(train_data,test_data)

    model_trainer=ModelTrainer()
    r2_score_value= model_trainer.intiate_model_trainer(train_array=train_array,test_array=test_array)
    print(r2_score_value)

import sys,os
from dataclasses import dataclass
import numpy as np
import pandas as pd

from src.utils.main_utils import save_object
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

from src.exception import CustomException
from src.logger import logging




@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifact','preprocessor.pkl')


class DataTransformation:

    def __init__(self):
        self.data_transformaition_config=DataTransformationConfig()

    def get_data_transfomer_object(self):
        '''
        Fucntion is used to transform data: Data Transformation
        '''
        try:
            numerical_columns=['reading score', 'writing score']
            categorical_columns=['gender', 'race/ethnicity', 'parental level of education', 'lunch', 'test preparation course']

            numerical_pipeline=Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler())
                ]
            )
            cat_pipeline=Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder",OneHotEncoder()),
                    ("scaler",StandardScaler(with_mean=False))
                ]
            )

            logging.info("Numerical columns standard saling completed")
            logging.info("Categorical columns encoding completed!!")

            preprocessor=ColumnTransformer([
                ("numericalPipeline", numerical_pipeline, numerical_columns),
                ("CatPipeline",cat_pipeline,categorical_columns)
            ])

            return preprocessor
        
        except Exception as e:
            raise(e,sys)

    def intiate_data_transformation(self, train_path, test_path):

        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("Read train and test data completed")
            logging.info("Obtaining preprocessing object")


            preprocessing_obj=self.get_data_transfomer_object()

            target_column_name="math score"
            numerical_columns=['reading score', 'writing score']
            categorical_columns=['gender', 'race/ethnicity', 'parental level of education', 'lunch', 'test preparation course']

            input_train_feature_df=train_df.drop(columns=[target_column_name], axis=1)
            target_train_feature_df=train_df[target_column_name]

            input_test_feature_df=test_df.drop(columns=[target_column_name], axis=1)
            target_test_feature_df=test_df[target_column_name]

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )
            
            input_train_feature_arr=preprocessing_obj.fit_transform(input_train_feature_df)
            input_test_feature_arr=preprocessing_obj.transform(input_test_feature_df)


            train_arr= np.c_[
                input_train_feature_arr,np.array(target_train_feature_df)
            ]
            test_arr= np.c_[
                input_test_feature_arr,np.array(target_test_feature_df)
            ]

            logging.info("Saved preprocessing object")
            save_object(file_path=self.data_transformaition_config.preprocessor_obj_file_path,
                     obj=preprocessing_obj)

            return (train_arr,test_arr,self.data_transformaition_config.preprocessor_obj_file_path)

        except Exception as e:
            raise CustomException(e, sys)
        

if __name__=="__main__":

    obj=DataTransformation()

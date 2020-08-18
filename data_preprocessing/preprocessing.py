import pandas as pd
import numpy as np
#from sklearn_pandas import CategoricalImputer
from sklearn.preprocessing import RobustScaler
from imblearn.over_sampling import RandomOverSampler
from imblearn.combine import SMOTETomek
from sklearn.ensemble import ExtraTreesClassifier

class Preprocessor:
    """
        This class shall  be used to clean and transform the data before training.

    """

    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object
        
        
        
        
    
    def is_null_present(self,data):
        """
         Method Name: is_null_present
         Description: This method checks whether there are null values present in the pandas Dataframe or not.
                                
        """
        self.logger_object.log(self.file_object, 'Entered the is_null_present method of the Preprocessor class')
        self.null_present = False
        self.cols_with_missing_values=[]
        self.cols = data.columns
        try:
            self.null_counts=data.isna().sum() # check for the count of null values per column
            for i in range(len(self.null_counts)):
                if self.null_counts[i]>0:
                    self.null_present=True
                    self.cols_with_missing_values.append(self.cols[i])
            if(self.null_present): # write the logs to see which columns have null values
                self.dataframe_with_null = pd.DataFrame()
                self.dataframe_with_null['columns'] = data.columns
                self.dataframe_with_null['missing values count'] = np.asarray(data.isna().sum())
                self.dataframe_with_null.to_csv('preprocessing_data/null_values.csv') # storing the null column information to file
            self.logger_object.log(self.file_object,'Finding missing values is a success.Data written to the null values file. Exited the is_null_present method of the Preprocessor class')
            return self.null_present, self.cols_with_missing_values
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in is_null_present method of the Preprocessor class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,'Finding missing values failed. Exited the is_null_present method of the Preprocessor class')
            raise Exception()
    
    
    def impute_missing_values(self, data, cols_with_missing_values):
        """
        Method Name: impute_missing_values
        Description: This method replaces all the missing values in the Dataframe using KNN Imputer.
        Output: A Dataframe which has all the missing values imputed.
        On Failure: Raise Exception

                                       
        """
        self.logger_object.log(self.file_object, 'Entered the impute_missing_values method of the Preprocessor class')
        self.data= data
        self.cols_with_missing_values=cols_with_missing_values
        try:
            self.imputer = CategoricalImputer()
            for col in self.cols_with_missing_values:
                self.data[col] = self.imputer.fit_transform(self.data[col])
            self.logger_object.log(self.file_object, 'Imputing missing values Successful. Exited the impute_missing_values method of the Preprocessor class')
            return self.data
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in impute_missing_values method of the Preprocessor class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,'Imputing missing values failed. Exited the impute_missing_values method of the Preprocessor class')
            raise Exception()
    
    def transform_column(self,data):
        self.categorical_col=['Wilderness_Area1',
       'Wilderness_Area2', 'Wilderness_Area3', 'Wilderness_Area4',
       'Soil_Type1', 'Soil_Type2', 'Soil_Type3', 'Soil_Type4', 'Soil_Type5',
       'Soil_Type6', 'Soil_Type7', 'Soil_Type8', 'Soil_Type9', 'Soil_Type10',
       'Soil_Type11', 'Soil_Type12', 'Soil_Type13', 'Soil_Type14',
       'Soil_Type15', 'Soil_Type16', 'Soil_Type17', 'Soil_Type18',
       'Soil_Type19', 'Soil_Type20', 'Soil_Type21', 'Soil_Type22',
       'Soil_Type23', 'Soil_Type24', 'Soil_Type25', 'Soil_Type26',
       'Soil_Type27', 'Soil_Type28', 'Soil_Type29', 'Soil_Type30',
       'Soil_Type31', 'Soil_Type32', 'Soil_Type33', 'Soil_Type34',
       'Soil_Type35', 'Soil_Type36', 'Soil_Type37', 'Soil_Type38',
       'Soil_Type39', 'Soil_Type40',]
        self.numerical_col=['Elevation', 'Aspect', 'Slope', 'Horizontal_Distance_To_Hydrology',
       'Vertical_Distance_To_Hydrology', 'Horizontal_Distance_To_Roadways',
       'Hillshade_9am ', 'Hillshade_Noon', 'Hillshade_3pm',
       'Horizontal_Distance_To_Fire_Points']
       
        self.categorical_data=data[self.categorical_col]
        self.numerical_data=data[self.numerical_col]
        self.target=data['Cover_Type']
        
        try:
            for col in self.numerical_data:
                if col!='Vertical_Distance_To_Hydrology':
                    self.numerical_data['boxcox_value'+col], self.param = stats.boxcox(self.numerical_data[col]+1) # you can vary the exponent as needed
            #this is for that variable which have very less minimum value
            self.numerical_data['boxcox_value'+'Vertical_Distance_To_Hydrology'],self.param = stats.boxcox(self.numerical_data['Vertical_Distance_To_Hydrology']+174) # you can vary the exponent as needed

            self.data_transform=self.numerical_data[[ 'boxcox_valueElevation',
             'boxcox_valueAspect', 'boxcox_valueSlope',
             'boxcox_valueHorizontal_Distance_To_Hydrology',
             'boxcox_valueHorizontal_Distance_To_Roadways',
             'boxcox_valueHillshade_9am ', 'boxcox_valueHillshade_Noon',
             'boxcox_valueHillshade_3pm',
             'boxcox_valueHorizontal_Distance_To_Fire_Points',
             'boxcox_valueVertical_Distance_To_Hydrology']]
        
            self.transform_df=pd.concat([self.data_transform,self.categorical_data,self.target],axis=1)
            return self.transform_df
        
            self.logger_object.log(self.file_object, 'transforming the numerical features')
        
        except Exception as e :
             self.logger_object.log(self.file_object,'Exception occured in scale_numerical_columns method of the Preprocessor class. Exception message:  ' + str(e))
             self.logger_object.log(self.file_object, 'scaling for numerical columns Failed. Exited the scale_numerical_columns method of the Preprocessor class')
             raise Exception()



   

   
    def scale_columns(self,data):
        """
        Method Name: scale_numerical_columns
        Description: This method scales the numerical values using the Standard scaler.
                                               
        """
        self.logger_object.log(self.file_object,
                               'Entered the scale_numerical_columns method of the Preprocessor class')

        self.data=data
        self.X=data.iloc[:,:-1]
        self.y=data.iloc['Cover_type']
        self.column=['Elevation', 'Aspect', 'Slope', 'Horizontal_Distance_To_Hydrology',
       'Vertical_Distance_To_Hydrology', 'Horizontal_Distance_To_Roadways',
       'Hillshade_9am ', 'Hillshade_Noon', 'Hillshade_3pm',
       'Horizontal_Distance_To_Fire_Points']
       

        try:

            self.scaler = RobustScaler()
            self.scaled_data = self.scaler.fit_transform(self.X)
            self.scaled_df = pd.DataFrame(data=self.scaled_data, columns=self.columns)
            
            self.scaled_data = pd.concat([self.scaled_df, self.y], axis=1)

            self.logger_object.log(self.file_object, 'scaling for numerical values successful. Exited the scale_numerical_columns method of the Preprocessor class')
            return self.scaled_data

        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in scale_numerical_columns method of the Preprocessor class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object, 'scaling for numerical columns Failed. Exited the scale_numerical_columns method of the Preprocessor class')
            raise Exception()
    

    def handle_imbalanced_dataset(self,data):
        """
        Method Name: handle_imbalanced_dataset
        Description: This method handles the imbalanced dataset to make it a balanced one.
        Output: new balanced feature and target columns

                  """
        self.logger_object.log(self.file_object,'Entered the handle_imbalanced_dataset method of the Preprocessor class')
        self.X=data[:,:-1]
        self.y=data['Cover_type']

        try:
            self.os=SMOTETomek('not majority')
            self.X_upsample,self.y_upsample=self.os.fit_sample(self.X,self.y)
            self.X_upsample_df=pd.DataFrame(self.X_upsample,columns=X.columns)
            self.y_upsample_df=pd.DataFrame(self.y_upsample,columns=['Cover_Type'])
            self.balanced_df=pd.concat([self.X_upsample_df,self.y_upsample_df],axis=1)
            self.logger_object.log(self.file_object,
                                   'dataset balancing successful. Exited the handle_imbalanced_dataset method of the Preprocessor class')
          
            return self.balanced_df 

        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in handle_imbalanced_dataset method of the Preprocessor class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'dataset balancing Failed. Exited the handle_imbalanced_dataset method of the Preprocessor class')
            raise Exception()
    def feature_selection(self,data):
       try:
           # passing the model
           model = ExtraTreesClassifier(random_state = 53)
           # feeding all our features to var 'X'
           self.X = data.iloc[:,:-1]
           # feeding our target variable to var 'y'
           self.y = data['Cover_Type']
           # training the model
           model.fit(self.X,self. y)
           # extracting feature importance from model and making a dataframe of it in descending order
           ETC_feature_importances = pd.DataFrame(model.feature_importances_, index = self.X.columns, columns=['ETC']).sort_values('ETC', ascending=False)
           list=[]
           for i,col in enumerate(ETC_feature_importances.index):
               if i!=20:
                   list.append(str(col))
               else:
                   break
           self.data=self.X[list]
           self.top_20fea_data=pd.concat([self.data,self.y],axis=1)
           return self.top_20fea_data
       except:
           print("Error Occure")
           
           
    def separate_label_feature(self, data, label_column_name):
        self.logger_object.log(self.file_object, 'Entered the separate_label_feature method of the Preprocessor class')
        try:
            self.X=data.drop(labels=label_column_name,axis=1) # drop the columns specified and separate the feature column
            self.Y=data[label_column_name] # Filter the Label columns
            self.logger_object.log(self.file_object,'Label Separation Successful. Exited the separate_label_feature method of the Preprocessor class')
            return self.X,self.Y
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in separate_label_feature method of the Preprocessor class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object, 'Label Separation Unsuccessful. Exited the separate_label_feature method of the Preprocessor class')
            raise Exception()      
           
           
    
 
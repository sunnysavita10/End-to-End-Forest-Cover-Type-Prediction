import pandas as pd
import numpy as np
#from sklearn_pandas import CategoricalImputer
from sklearn.preprocessing import RobustScaler
from sklearn.ensemble import ExtraTreesClassifier
import scipy.stats as stats
import traceback

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
              
            self.data_transform.columns=self.numerical_col
            self.transform_df=pd.concat([self.data_transform,self.categorical_data],axis=1)
            return self.transform_df
        
            self.logger_object.log(self.file_object, 'transforming the numerical features')
        
        except Exception as e :
             print(traceback.format_exc())
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

        try:

            self.scaler = RobustScaler()
            self.scaled_data = self.scaler.fit_transform(self.data)
            self.scaled_df = pd.DataFrame(data=self.scaled_data,columns=data.columns)
            self.logger_object.log(self.file_object, 'scaling for numerical values successful. Exited the scale_numerical_columns method of the Preprocessor class')
            return self.scaled_df

        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in scale_numerical_columns method of the Preprocessor class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object, 'scaling for numerical columns Failed. Exited the scale_numerical_columns method of the Preprocessor class')
            raise Exception()
    

   
    def feature_selection(self,data):
       #we have got this feature via model training you can see my EDA notebook because i trained my model in google colab
        try:
            self.top_20fea_data=data[["Elevation","Aspect","Slope","Horizontal_Distance_To_Roadways" ,"Horizontal_Distance_To_Fire_Points",
                     "Horizontal_Distance_To_Hydrology" ,"Vertical_Distance_To_Hydrology" ,"Hillshade_Noon" ,"Hillshade_9am ","Hillshade_3pm" ,"Soil_Type4","Soil_Type12"
                     ,"Soil_Type10" ,"Soil_Type22","Soil_Type23" ,"Soil_Type38" ,"Soil_Type39" ,"Wilderness_Area1","Wilderness_Area3","Wilderness_Area4"]]
            print(self.top_20fea_data.head())
            return self.top_20fea_data
        except:
            print("Error Occure")
           
          
    
 
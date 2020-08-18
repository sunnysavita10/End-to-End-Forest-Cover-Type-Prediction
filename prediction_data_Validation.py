from datetime import datetime
from Prediction_Raw_Data_Validation.predictionDataValidation import Prediction_Data_validation
from MongodbOpration_Insertion_Prediction.DataBaseOperationPrediction import dBOperation
from application_logging import logger

class pred_validation:
    def __init__(self,path):
        self.raw_data = Prediction_Data_validation(path)
        
        self.dBOperation = dBOperation()
        self.file_object = open("Prediction_Logs/Prediction_Log.txt", 'a+')
        self.log_writer = logger.App_Logger()

    def prediction_validation(self):

        try:

            self.log_writer.log(self.file_object,'Start of Validation on files for prediction!!')
            #extracting values from prediction schema
            column_names,noofcolumns = self.raw_data.valuesFromSchema()
            
            #getting the regex defined to validate filename
            #regex = self.raw_data.manualRegexCreation()
            
            #validating filename of prediction files
            #self.raw_data.validationFileNameRaw(regex)
            
            #validating number of columns
            self.raw_data.validateColumnLength(noofcolumns)
            
            #validating if any column has all values missing
            #self.raw_data.validateMissingValuesInWholeColumn()
            self.log_writer.log(self.file_object,"Raw Data Validation Complete!!")


            self.log_writer.log(self.file_object,"Creating Prediction_Database and collection on the basis of given schema!!!")
            # create database with given name, if present open the connection! Create table with columns given in schema
            collection=self.dBOperation.createCollection()
            self.log_writer.log(self.file_object, "collection creation Completed!!")
            self.log_writer.log(self.file_object, "Insertion of Data into collection started!!!!")
            
            # insert csv files in the collection
            self.dBOperation.GoodDatainsertIntoCollection(collection)
            self.log_writer.log(self.file_object, "Insertion in collection completed!!!")
            self.log_writer.log(self.file_object, "Deleting Good Data Folder!!!")
            
            # Delete the good data folder after loading files in table
            self.raw_data.deleteExistingGoodDataPredictionFolder()
            self.log_writer.log(self.file_object, "Good_Data folder deleted!!!")
            self.log_writer.log(self.file_object, "Moving bad files to Archive and deleting Bad_Data folder!!!")
            
            # Move the bad files to archive folder
            self.raw_data.moveBadFilesToArchive()
            self.log_writer.log(self.file_object, "Bad files moved to archive!! Bad folder Deleted!!")
            self.log_writer.log(self.file_object, "Validation Operation completed!!")
            self.log_writer.log(self.file_object, "Extracting csv file from table")
            
            # export data in table to csvfile
            self.dBOperation.selectingDatafromCollectionintocsv(collection)
            self.file_object.close()

        except Exception as e:
            raise e
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
           
           










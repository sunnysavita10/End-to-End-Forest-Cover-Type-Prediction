from application_logging import logger
from datetime import datetime
from Training_Raw_data_validation.rawValidation import Raw_Data_validation
from MongoDbOperations_Insertion_Training.DataBaseOperations import dBOperation



class train_validation:
    def __init__(self,path):
        self.raw_data = Raw_Data_validation(path)
        self.dBOperation = dBOperation()
        self.file_object = open("Training_Logs/Training_Main_Log.txt", 'a+')
        self.log_writer = logger.App_Logger()

    def train_validation(self):
        try:
            self.log_writer.log(self.file_object, 'Start of Validation on files!!')
            # extracting values from prediction schema
            column_names,noofcolumns = self.raw_data.valuesFromSchema()
            # getting the regex defined to validate filename
            regex = self.raw_data.manualRegexCreation()
            # validating filename of prediction files
            self.raw_data.validationFileNameRaw(regex)
            # vNo documentation avaialidating column length in the file
            self.raw_data.validateColumnLength(noofcolumns)
           
            self.log_writer.log(self.file_object, "Raw Data Validation Complete!!")

            

            self.log_writer.log(self.file_object,"Creating Training_Database and collection on the basis of given schema!!!")
            # create database with given name, if present open the connection! Create table with columns given in schema
            collection=self.dBOperation.createCollection()
            self.log_writer.log(self.file_object, "collection creation Completed!!")
            self.log_writer.log(self.file_object, "Insertion of Data into collection started!!!!")
            # insert csv files in the collection
            self.dBOperation.GoodDatainsertIntoCollection(collection)
            self.log_writer.log(self.file_object, "Insertion in Table completed!!!")
            self.log_writer.log(self.file_object, "Deleting Good Data Folder!!!")
            # Delete the good data folder after loading files in table
            self.raw_data.deleteExistingGoodDataTrainingFolder()
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










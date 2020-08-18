import shutil
import pymongo
from os import listdir
import os
#import csv
from application_logging.logger import App_Logger
import pandas as pd
import traceback


class dBOperation:
    """
      This class shall be used for handling all the SQL operations.


      """
    def __init__(self):
        self.path = 'Training_Database/'
        self.badFilePath = "Training_Raw_files_validated/Bad_Raw"
        self.goodFilePath = "Training_Raw_files_validated/Good_Raw"
        self.logger = App_Logger()


    def dataBaseConnection(self):

        """
                Method Name: dataBaseConnection
                Description: This method creates the database with the given name and if Database already exists then opens the connection to the DB.
                Output: Connection to the DB
                On Failure: Raise ConnectionError
        """
        try:
            dbConn = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
           
            dbname="training"
            db = dbConn[dbname]
            print(dbConn.list_database_names())
           
            file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Opened %s database successfully" % dbname)
            file.close()
        except ConnectionError:
            file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Error while connecting to database: %s" %ConnectionError)
            file.close()
            raise ConnectionError
        return db

    def createCollection(self):
        """
        Method Name: createTableDb
        Description: This method creates a table in the given database which will be used to insert the Good data after raw data validation.
        Output: None
        On Failure: Raise Exception

       """
      
        try:
            db=self.dataBaseConnection()
            collection_name='Covertype_dataSet'
            collection=db[collection_name]
            
            
            file = open("Training_Logs/DbCollectioCreateLog.txt", 'a+')
            self.logger.log(file, "Collection created successfully!!")
            file.close()
            print("no error")
            
        
           


        except Exception as e:
            file = open("Training_Logs/DbCollectionCreateLog.txt", 'a+')
            self.logger.log(file, "Error while creating collection: %s " % e)
            file.close()
            
            file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Closed %s database successfully")
            file.close()
            raise e
        print("noerror")    
        return collection      


    def GoodDatainsertIntoCollection(self,collname):

        """
        Method Name: insertIntoCollectionGoodData
        Description: This method inserts the Good data files from the Good_Raw folder into the
        above created table.
        Output: None
        On Failure: Raise Exception

                              

        """
        collection=collname
        
        
        
        goodFilePath= self.goodFilePath
        badFilePath = self.badFilePath
        onlyfiles = [f for f in listdir(goodFilePath)]
        log_file = open("Training_Logs/DbInsertLog.txt", 'a+')
        print(onlyfiles)

        for file in onlyfiles:
            try:
                print(type(file))
                df=pd.read_csv(goodFilePath + "/"+"CoverType_DataSet.csv")
                print("yes")
                x=df.to_dict('records')
                x = collection.insert_many(x) 
                print("ok")#this is ids of records
               

            except Exception as e:
                print(traceback.format_exc())
                self.logger.log(log_file,"Error while creating store data into collection: %s " % e)
                shutil.move(goodFilePath+'/' + file, badFilePath)
                self.logger.log(log_file, "Error inserting File Moved Successfully %s" % file)
                log_file.close()
                
        log_file.close()


    def selectingDatafromCollectionintocsv(self,coll):

        """
        Method Name: selectingDatafromtableintocsv
        Description: This method exports the data in GoodData table as a CSV file. in a given location.
        above created .
        Output: None
                             
       """

        self.fileFromDb = 'Training_FileFromDB/'
        self.fileName = 'InputFile.csv'
        log_file = open("Training_Logs/ExportToCsv.txt", 'a+')
        try:
            conn = coll
            cursor = conn.find()
            mongo_docs = list(cursor)
            docs = pd.DataFrame(mongo_docs)
            docs=docs.drop(['_id'],axis=1)

            
            #Make the CSV ouput directory
            if not os.path.isdir(self.fileFromDb):
                os.makedirs(self.fileFromDb)

            docs.to_csv("Training_FileFromDB/InputFile.csv",index=False)
            
           
            self.logger.log(log_file, "File exported successfully!!!")
            log_file.close()

        except Exception as e:
            self.logger.log(log_file, "File exporting failed. Error : %s" %e)
            log_file.close()






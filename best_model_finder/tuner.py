from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics  import roc_auc_score,accuracy_score
from sklearn.model_selection import KFold,RepeatedStratifiedKFold

class Model_Finder:
    """
                This class shall  be used to find the model with best accuracy and AUC score.
    """

    def __init__(self,file_object,logger_object):
        self.file_object = file_object
        self.logger_object = logger_object
        self.clf=RandomForestClassifier()
        self.xgb = XGBClassifier()

    
    
    
    def get_best_params_for_xgboost(self,train_x,train_y):

        """
                                        Method Name: get_best_params_for_xgboost
                                        Description: get the parameters for XGBoost Algorithm which give the best accuracy.
                                                     Use Hyper Parameter Tuning.
                                        Output: The model with the best parameters
                                        
       """
        self.logger_object.log(self.file_object,'Entered the get_best_params_for_xgboost method of the Model_Finder class')
        try:
            # initializing with different combination of parameters
           
            self.param_grid_xgboost = {'learning_rate': [ 0.1, 0.01],
                'max_depth': [3, 5],
                'n_estimators': [10,30],
                'min_child_weight':range(1,3),
                }

            # Creating an object of the Grid Search class
            self.grid= GridSearchCV(XGBClassifier(),self.param_grid_xgboost, verbose=3,cv=5,n_jobs=-1)
            # finding the best parameters
            self.grid.fit(train_x, train_y)

          
            # extracting the best parameters
            self.learning_rate = self.grid.best_params_['learning_rate']
            self.max_depth = self.grid.best_params_['max_depth']
            self.n_estimators = self.grid.best_params_['n_estimators']
            self.min_child_weight=self.grid.best_params_['min_child_weight']
           

            # creating a new model with the best parameters
            self.xgb = XGBClassifier(learning_rate=self.learning_rate,max_depth=self.max_depth,n_estimators=self.n_estimators,min_child_weight=self.min_child_weight)
            # training the mew model
            self.xgb.fit(train_x, train_y)
            
            self.logger_object.log(self.file_object,
                                   'XGBoost best params: ' + str(
                                       self.grid.best_params_) + '. Exited the get_best_params_for_xgboost method of the Model_Finder class')
            return self.xgb
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in get_best_params_for_xgboost method of the Model_Finder class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'XGBoost Parameter tuning  failed. Exited the get_best_params_for_xgboost method of the Model_Finder class')
            raise Exception()

    
    
    def get_best_params_for_random_forest(self,train_x,train_y):
        """
        Method Name: get_best_params_for_naive_bayes
        Description: get the parameters for the SVM Algorithm which give the best accuracy.
                     Use Hyper Parameter Tuning.
        Output: The model with the best parameters
       
       """
        self.logger_object.log(self.file_object, 'Entered the get_best_params_for_svm method of the Model_Finder class')
        try:
            #initializing with different combination of parameters
            self. param_grid = {"n_estimators": [10, 50, 100], 
                          "criterion": ['gini', 'entropy'],
                          "max_depth": range(2, 4, 1), 
                          "max_features": ['auto', 'log2']
                         }
            #Creating an object of the Grid Search class
            self.grid = GridSearchCV(estimator=self.clf, param_grid=self.param_grid, cv=5,  verbose=3,n_jobs=-1)
            #finding the best parameters
            self.grid.fit(train_x, train_y)

            #extracting the best parameters
            self.n_estimators = self.grid.best_params_["n_estimators"]
            self.criterion = self.grid.best_params_["criterion"]
            self.max_depth = self.grid.best_params_["max_depth"]
            self.max_features=self.grid.best_params_["max_features"]

            #creating a new model with the best parameters
            self.clf = RandomForestClassifier(n_estimators=self.n_estimators,criterion=self.criterion,max_depth=self.max_depth,max_features=self.max_features)
            # training the mew model
            self.clf.fit(train_x, train_y)
            self.logger_object.log(self.file_object,
                                   'RF best params: '+str(self.grid.best_params_)+'. Exited the get_best_params_for_RF method of the Model_Finder class')

            return self.clf
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in get_best_params_for_RF method of the Model_Finder class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'RF training  failed. Exited the get_best_params_for_rf method of the Model_Finder class')
            raise Exception()


    def get_best_model(self,train_x,train_y,test_x,test_y):
        """
                                                Method Name: get_best_model
                                                Description: Find out the Model which has the best AUC score.
                                                Output: The best model name and the model object
                                                
        """
        self.logger_object.log(self.file_object,'Entered the get_best_model method of the Model_Finder class')
       
        # create best model for XGBoost
        try:
            self.xgboost= self.get_best_params_for_xgboost(train_x,train_y)
            self.prediction_xgboost = self.xgboost.predict(test_x) # Predictions using the XGBoost Model

            if len(test_y.unique()) == 1: #if there is only one label in y, then roc_auc_score returns error. We will use accuracy in that case
                self.xgboost_score = accuracy_score(test_y, self.prediction_xgboost)
                self.logger_object.log(self.file_object, 'Accuracy for XGBoost:' + str(self.xgboost_score))  # Log AUC
            else:
                self.xgboost_score = roc_auc_score(test_y, self.prediction_xgboost) # AUC for XGBoost
                self.logger_object.log(self.file_object, 'AUC for XGBoost:' + str(self.xgboost_score)) # Log AUC

            # create best model for Random Forest
            self.RF_classifier=self.get_best_params_for_random_forest(train_x,train_y)
            self.prediction_RF=self.RF_classifier.predict(test_x) # prediction using the SVM Algorithm

            if len(test_y.unique()) == 1:#if there is only one label in y, then roc_auc_score returns error. We will use accuracy in that case
                self.RF_score = accuracy_score(test_y,self.prediction_RF)
                self.logger_object.log(self.file_object, 'Accuracy for RF:' + str(self.RF_score))
            else:
                self.RF_score = roc_auc_score(test_y, self.prediction_RF) # AUC for Random Forest
                self.logger_object.log(self.file_object, 'AUC for RF:' + str(self.RF_score))

            #comparing the two models
            if(self.RF_score <  self.xgboost_score):
                return 'XGBoost',self.xgboost
            else:
                return 'RF',self.RF_classifier

        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in get_best_model method of the Model_Finder class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'Model Selection Failed. Exited the get_best_model method of the Model_Finder class')
            raise Exception()


from wsgiref import simple_server
from flask import Flask, request, render_template,url_for
from flask import Response
from flask_cors import CORS, cross_origin
import flask_monitoringdashboard as dashboard
import os
import json
import pickle
import numpy as np

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
dashboard.bind(app)
CORS(app)

# Load the Random Forest CLassifier model
filename = 'models/RFtopfea.pkl'
classifier = pickle.load(open(filename, 'rb'))


@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('Index.html')



@app.route("/onevalue", methods=['GET'])
@cross_origin()
def onevalue():
    return render_template('singlevalpred.html')

        



from prediction_data_Validation import pred_validation
from predictFromModel import prediction

@app.route("/predict", methods=['GET','POST'])
@cross_origin()
def predictRouteClient():
    try:
        #this is for POSTMAN API
        if request.json is not None:
            path = request.json['filepath']
            pred_val = pred_validation(path) #object initialization
            pred_val.prediction_validation() #calling the prediction_validation function

            pred = prediction(path) #object initialization

            # predicting for dataset present in database
            path,json_predictions = pred.predictionFromModel()
            return Response("Prediction File created at !!!"  +str(path) +'and few of the predictions are '+str(json_predictions))
        
        #this is for HTML form or web frame work
        elif request.form is not None:
            path = request.form['filepath']
            pred_val = pred_validation(path) #object initialization

            pred_val.prediction_validation() #calling the prediction_validation function

            pred = prediction(path) #object initialization

            # predicting for dataset present in database
            path,json_predictions = pred.predictionFromModel()
            return Response("Prediction File created at !!!"  +str(path) +'and few of the predictions are '+str(json_predictions))
        

        else:
            print('Nothing Matched')
    except ValueError:
        return Response("Error Occurred! %s" %ValueError)
    except KeyError:
        return Response("Error Occurred! %s" %KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" %e)



from training_data_Validation import train_validation
from Modeltraining import trainModel

@app.route("/train", methods=['POST'])
@cross_origin()
def trainRouteClient():

    try:
        if request.json['folderPath'] is not None:
            path = request.json['folderPath']

            train_valObj = train_validation(path) #object initialization

            train_valObj.train_validation()#calling the training_validation function


            trainModelObj = trainModel() #object initialization
            trainModelObj.trainingModel() #training the model for the files in the table


    except ValueError:

        return Response("Error Occurred! %s" % ValueError)

    except KeyError:

        return Response("Error Occurred! %s" % KeyError)

    except Exception as e:

        return Response("Error Occurred! %s" % e)
    return Response("Training successfull!!")






@app.route("/singlevaluepred", methods=['POST'])
def predict():
    if request.method == 'POST':
        elev= (request.form["Elevation"])
        Aspect = (request.form["Aspect"])
        slope = (request.form["Slope"])
        HDTR = (request.form["Horizontal_Distance_To_Roadways"])
        HDtFP = (request.form["Horizontal_Distance_To_Fire_Points"])
        HDtH = (request.form["Horizontal_Distance_To_Hydrology"])
        VDtH = (request.form["Vertical_Distance_To_Hydrology"])
        H_noon = (request.form["Hillshade_Noon"])
        H_9pm = (request.form["Hillshade_9am "])
        H_3pm = float(request.form["Hillshade_3pm"])
        ST4 = (request.form["Soil_Type4"])
        ST12 = (request.form["Soil_Type12"])
        ST10 = (request.form["Soil_Type10"])
        ST22 = (request.form["Soil_Type22"])
        ST23 = (request.form["Soil_Type23"])
        ST38 = (request.form["Soil_Type38"])
        ST39 = (request.form["Soil_Type39"])
        W_area1= (request.form["Wilderness_Area1"])
        W_area3 = (request.form["Wilderness_Area3"])
        W_area4 = (request.form["Wilderness_Area4"])
        
        data = np.array([ [elev,Aspect,slope,HDTR ,HDtFP,
                     HDtH ,VDtH ,H_noon ,H_9pm,H_3pm ,ST4,ST12
                     ,ST10 ,ST22,ST23 ,ST38 ,ST39 ,W_area1,W_area3,W_area4]])
        my_prediction = classifier.predict(data)
        
        return render_template('Result.html', prediction=my_prediction)

port = int(os.getenv("PORT",5000))
if __name__ == "__main__":
    app.run(debug=True)
    #host = '0.0.0.0'
    #port = 5000
    #httpd = simple_server.make_server(host, port, app)
    # print("Serving on %s %d" % (host, port))
    #httpd.serve_forever()
    
 
    
    




    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

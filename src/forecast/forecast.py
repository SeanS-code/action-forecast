from forecast.redis import createreq, returnreq, returnkeys
from pathlib import Path

import numpy as np

import datetime
import uuid
import base64
import json
import joblib

modelpkldump_path = Path(__file__).parent.parent.parent

# 'data/model.pkl'
modelpkldump_file = modelpkldump_path / "data" / "model.pkl"

# Load the model
model = joblib.load(modelpkldump_file)

def submitreq(data):
    requestid = str(uuid.uuid4())

    if type(data) is dict:
        data = json.dumps(data)

    dataenc = (base64.b64encode(data.encode('utf-8'))).decode('utf-8')
    current_date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    request_json = {
        "requestid": requestid,
        "request": {
            "taskid": requestid,
            "reqdate": current_date,
            "data": {
                "args": dataenc
            }
        },
        "response": {
            "requestid": requestid,
            "reqdate": current_date,
            "restime": 0,
            "message": "In Progress",
            "data": {}
        }
    }

    print(" ")
    print("--- JSON String of Request")
    print(request_json)
    createreq(requestid, json.dumps(request_json))

    return requestid


def predictres(requestid):
    request_dict = json.loads(returnreq(requestid))
    dataenc = request_dict["request"]["data"]["args"]

    datadec = (base64.b64decode(dataenc.encode('utf-8'))).decode('utf-8')
    data_dict = json.loads(datadec)

    print(" ")
    print("--- Data Dict.")
    print(data_dict)
    print(" ")

    input_features = np.array(data_dict['features']).reshape(1, -1)

    print(" ")
    print("--- Input Features")
    print(input_features)
    print(" ")

    prediction = model.predict(input_features)
    prediction_json = json.dumps(prediction[0])

    predenc = (base64.b64encode(prediction_json.encode('utf-8'))).decode('utf-8')

    request_dict["response"]["data"]["args"] = predenc
    request_dict["response"]["message"] = "Complete"

    dumped_json = json.dumps(request_dict)
    response_json = json.loads(dumped_json)

    print(" ")
    print("--- Checking JSON Response")
    print(type(response_json))
    print(" ")

    print(" ")
    print("--- JSON Response")
    print(response_json)
    print(" ")

    return response_json

def returnallreq():
    allreqs = returnkeys()
    return allreqs
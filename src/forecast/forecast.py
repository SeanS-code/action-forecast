import os
from forecast.redis import createreq, returnreq, savereq, returnkeys
from pathlib import Path
from time import perf_counter
# from memory_profiler import profile

import numpy as np
import datetime
import uuid
import base64
import json
import joblib

# check if the "UNRELIABLE" environment variable exists
profile = os.environ.get("ENABLE_PROFILING")

modelpkldump_path = Path(__file__).parent.parent.parent

# 'data/model.pkl'
modelpkldump_file = modelpkldump_path / "data" / "model.pkl"

# Load the model
model = joblib.load(modelpkldump_file)


def generatereq():
    requestid = str(uuid.uuid4())

    return requestid


def submitreq(requestid, data):

    if profile is not None and profile == "True": 
        start = perf_counter()

    message = "In Progress"

    if type(data) is dict:
        data = json.dumps(data)

    dataenc = (base64.b64encode(data.encode('utf-8'))).decode('utf-8')

    current_date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S.%f")

    request_json = {
        "requestid": requestid,
        "message": message,
        "request": {
            "reqdate": current_date,
            "data": {
                "args": dataenc
            }
        },
        "response": {
            "resdate": 0,
            "restime": 0,
            "data": {}
        }
    }

    createreq(requestid, json.dumps(request_json))

    if profile is not None and profile == "True": 
        duration = perf_counter() - start

        print(" ")
        print(f"--- xxx1 {requestid} | Response Time: {duration}, Data: {message}")
        print(" ")


#@profile
def predictmodel(requestid):

    if profile is not None and profile == "True": 
        start = perf_counter()

    request_dict = json.loads(returnreq(requestid))
    dataenc = request_dict["request"]["data"]["args"]

    datadec = (base64.b64decode(dataenc.encode('utf-8'))).decode('utf-8')
    data_dict = json.loads(datadec)

    input_features = np.array(data_dict['features']).reshape(1, -1)

    current_date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S.%f")

    start = perf_counter()
    prediction = model.predict(input_features)
    duration = perf_counter() - start

    prediction_json = json.dumps(prediction[0])

    predenc = (base64.b64encode(prediction_json.encode('utf-8'))).decode('utf-8')

    request_dict["message"] = "Complete"

    request_dict["response"]["data"]["result"] = predenc
    request_dict["response"]["restime"] = duration
    request_dict["response"]["resdate"] = current_date

    dumped_json = json.dumps(request_dict)
    response_json = json.loads(dumped_json)

    savereq(requestid, dumped_json)

    if profile is not None and profile == "True": 
        duration = perf_counter() - start

        print(" ")
        print(f"--- xxx2 {requestid} | Response Time: {duration} | Data: {request_dict['message']}")
        print(" ")

    return response_json


def predictres(requestid):
    request_dict = json.loads(returnreq(requestid))
    
    return request_dict


def returnallreq():
    allreqs = returnkeys()
    return allreqs

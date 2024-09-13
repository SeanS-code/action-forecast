from forecast import forecast
import uvicorn

import cProfile as profile

def main():
    data = '{"features": [8.3252, 41.0, 6.984127, 1.02381, 322.0]}'
    # , 2.555556, 37.88, -122.23
    requestid = forecast.submitreq(data)
    forecast.predictres(requestid)

    ## Profiling
    
    # Submit Request
    # profile.runctx('forecast.submitreq(data)', globals(), locals(), filename="prof1.out")
    # profile.runctx('forecast.submitreq(data)', globals(), locals())

    # Predict Reponse
    # profile.runctx('forecast.predictres(requestid)', globals(), locals(), filename="prof2.out")
    # profile.runctx('forecast.predictres(requestid)', globals(), locals())
    # snakeviz prof.out in terminal

def api():
    # skipcq: BAN-B104
    uvicorn.run("forecast.forecastapi:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == '__main__':
    main()

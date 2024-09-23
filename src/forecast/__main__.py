from forecast import forecast
import uvicorn
import os

import cProfile

# check if the "UNRELIABLE" environment variable exists
enableprofiling = os.environ.get("ENABLE_PROFILING")


def main():
    data = '{"features": [8.3252, 41.0, 6.984127, 1.02381, 322.0]}'

    requestid = forecast.generatereq()
    forecast.submitreq(requestid, data)
    forecast.predictmodel(requestid)
    forecast.predictres(requestid)

    # Profiling
    
    # Submit Request / Predict Reponse
    # profile.runctx('forecast.submitreq(data)', globals(), locals(), filename="prof1.out")
    # profile.runctx('forecast.predictres(requestid)', globals(), locals(), filename="prof2.out")


def api():
    # skipcq: BAN-B104
    uvicorn.run("forecast.forecastapi:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == '__main__':
    #export ENABLE_PROFILING=1 before calling forecast
    if enableprofiling is not None and enableprofiling == "True":
        cProfile.run('main()', '/tmp/profile.log')
        # snakeviz profile.log in terminal
        
    main()

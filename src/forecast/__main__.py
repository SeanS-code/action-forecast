from forecast import forecast
import uvicorn

def main():
    data = '{"features": [8.3252, 41.0, 6.984127, 1.02381, 322.0]}'
    # , 2.555556, 37.88, -122.23
    requestid = forecast.submitreq(data)
    forecast.predictres(requestid)


def api():
    uvicorn.run("forecast.forecastapi:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == '__main__':
    main()

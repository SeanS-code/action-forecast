import redis

# Remove global redis connection to fix pytesxt
r = None

# Load the redis
def loadredis():
    global r
    if r is None:
        r = redis.Redis(host='localhost', port=6379, db=0)
    return r

def createreq(requestid: str, req: str):
    r = loadredis()
    r.set(requestid, req)
    return r.save()
    # https://realpython.com/python-redis/ - have to see what happens if redis grows
    # .... but this does a synchronous (blocking)
    # .... save rather than using fork(), so you
    # shouldn’t use it without a specific reason.
    # >>> r.bgsave() : True


def savereq(requestid: str, req: str):
    r = loadredis()
    r.set(requestid, req)
    return r.save()


def returnreq(requestid: str):
    r = loadredis()
    dataenc = r.get(requestid)
    return dataenc


def returnkeys():
    r = loadredis()
    allkeys = r.keys()
    # print(allkeys)
    return allkeys

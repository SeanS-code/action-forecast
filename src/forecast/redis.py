import redis

r = redis.Redis(host='localhost', port=6379, db=0)


def createreq(requestid: str, req: str):
    r.set(requestid, req)
    return r.save()
    # https://realpython.com/python-redis/ - have to see what happens if redis grows
    # .... but this does a synchronous (blocking)
    # .... save rather than using fork(), so you
    # shouldn’t use it without a specific reason.
    # >>> r.bgsave() : True


def savereq(requestid: str, req: str):
    r.set(requestid, req)
    return r.save()


def returnreq(requestid: str):
    dataenc = r.get(requestid)
    return dataenc


def returnkeys():
    allkeys = r.keys()
    # print(allkeys)
    return allkeys

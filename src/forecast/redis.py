import redis

r = redis.Redis(host='localhost', port=6379, db=0)

def createreq(requestid:str, req: str):
    r.set(requestid, req)
    return r.bgsave() 
    # https://realpython.com/python-redis/ - have to see what happens if redis grows
    # .... but this does a synchronous (blocking) 
    # .... save rather than using fork(), so you 
    # shouldn’t use it without a specific reason. 
    # >>> r.bgsave() : True

def returnreq(requestid:str):
    print(" ")
    print("--- Request ID")
    print(requestid)
    print(" ")
    print("--- r.get Results ")
    print(r.get(requestid))
    print(" ")

    dataenc = r.get(requestid)
    return dataenc

def returnkeys():
    allkeys = r.keys()
    print(allkeys)
    return allkeys

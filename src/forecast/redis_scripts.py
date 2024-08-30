import redis

r = redis.Redis(host='localhost', port=6379, db=0)

def generate_taskID(uuid: str):
    r.set(uuid, "awaiting results from model")
    r.save()
    return uuid

def taskID_value(task_id, response):
    res = r.set(task_id, str(response))
    return res

def client_task(value):
    r.set("ctask"+str(k), value)
    return "ctask"+str(k)

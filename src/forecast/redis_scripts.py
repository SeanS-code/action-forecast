import redis

r = redis.Redis(host='localhost', port=6379, db=0)
i = 1
k = 1

def generate_taskID():
    r.set("task"+str(i), "value1")
    return "task"+str(i)

def taskID_value(task_id):
    res = r.get("task"+str(task_id))
    return res

def client_task(value):
    r.set("ctask"+str(k), value)
    return "ctask"+str(k)

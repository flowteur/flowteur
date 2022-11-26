import json
import time
# appent to queue.json file and return the id

# check if file exists and create it if it doesn't


queuePath = "./data/queue.json"

def add(type, params, status):
    queueFile = open(queuePath, "r")
    # create and id base on timestamp
    id = int(time.time())
    # open queue.json
    # append to queue.json file and return the id
    queue = json.load(queueFile)
    queueFile.close()

    queueFile = open(queuePath, "w")
    queue.append({"id": id,"type": type, "params": params, "status": status})
    queueFile.write(json.dumps(queue))
    queueFile.close()

    return id

def update(id, status):
    queueFile = open(queuePath, "r")
    # open queue.json
    # read the queue.json file and return the id
    queue = json.load(queueFile)
    queueFile.close()

    for item in queue:
        if item["id"] == id:
            item["status"] = status

    queueFile = open(queuePath, "w")
    queueFile.write(json.dumps(queue))
    queueFile.close()

    return id

def read(id):
    queueFile = open(queuePath, "r")
    # open queue.json
    # read the queue.json file and return the id
    queue = json.load(queueFile)
    queueFile.close()

    for item in queue:
        if item["id"] == int(id):
            if item["status"] == "done":
                if item["type"] == "gpt":
                    resultPath = "./static/" + str(item["id"]) + ".txt"
                    resultFile = open(resultPath, "r")
                    result = resultFile.read()
                    resultFile.close()
                    return result
                elif item["type"] == "sd" or item["type"] == "sd2":
                    resultPath = "./static/" + str(item["id"]) + ".png"
                    resultFile = open(resultPath, "rb")
                    result = resultFile.read()
                    resultFile.close()
                    return result
            return item

def readAll():
    queueFile = open(queuePath, "r")
    # open queue.json
    # read the queue.json file and return the id
    queue = json.load(queueFile)
    queueFile.close()

    return queue
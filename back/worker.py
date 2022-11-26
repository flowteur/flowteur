import modules.gpt as gpt
import modules.stable_diffusion as sd
import modules.queueManager as queueManager

import json
import time
from PIL import Image

# open data/queue.json and for each item in the queue, check if the status is pending, if it is, call the worker and update the status to processing
queuePath = "data/queue.json"
resultsPath = "static/"



def saveImage(image, id):
    resultPath = resultsPath + str(id) + ".png"
    image.save(resultPath)




while True:
    # open queue.json
    queueFile = open(queuePath, "r")
    queue = json.load(queueFile)
    queueFile.close()

    for item in queue:
        print(item)
        #check if status is pending
        if item["status"] == "pending":
            # if it is, call the worker and update the status to processing
            if item["type"] == "gpt":
                queueManager.update(item["id"], "processing")
                text = gpt.generate(item["params"]["text"])
                # save the result to the results folder
                resultPath = resultsPath + str(item["id"]) + ".txt"
                resultFile = open(resultPath, "w")
                resultFile.write(text)
                resultFile.close()
                queueManager.update(item["id"], "done")
                
                
            elif item["type"] == "sd":
                queueManager.update(item["id"], "processing")
                image = sd.generate(item["params"]["prompt"], item["params"]["num_inference_steps"], item["params"]["width"], item["params"]["height"])
                # save the result to the results folder
                resultPath = resultsPath + str(item["id"]) + ".png"
                saveImage(image, item["id"])
                queueManager.update(item["id"], "done")
            
            elif item["type"] == "sd2":
                queueManager.update(item["id"], "processing")
                image = sd2.generate(item["params"]["prompt"], item["params"]["num_inference_steps"], item["params"]["width"], item["params"]["height"])
                saveImage(image, item["id"])
                queueManager.update(item["id"], "done")
                
                
    print("sleeping")
    time.sleep(2)
    


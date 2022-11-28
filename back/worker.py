import modules.gpt as gpt
import modules.stable_diffusion as sd
import modules.queueManager as queueManager

import json
import time
from PIL import Image

# adding a loggin system
import logging
logging.basicConfig(filename='log.log', filemode='a', format='%(asctime)s - %(message)s', level=logging.DEBUG)


# open data/queue.json and for each item in the queue, check if the status is pending, if it is, call the worker and update the status to processing
queuePath = "data/queue.json"
resultsPath = "static/"



def saveImage(image, id):
    logging.info("saving image")
    resultPath = resultsPath + str(id) + ".png"
    image.save(resultPath)




while True:
    # open queue.json
    queueFile = open(queuePath, "r")
    queue = json.load(queueFile)
    queueFile.close()

    for item in queue:
        logging.info("checking item")
        #check if status is pending
        if item["status"] == "pending":
            logging.info("item is pending")
            # if it is, call the worker and update the status to processing
            if item["type"] == "gpt":
                logging.info("item is gpt")
                queueManager.update(item["id"], "processing")
                text = gpt.generate( item["params"]["model"],item["params"]["text"], item["params"]["min_length"], item["params"]["max_length"], item["params"]["eos_token_id"], item["params"]["pad_token"], item["params"]["top_k"], item["params"]["top_p"], item["params"]["no_repeat_ngram_size"])
                # save the result to the results folder
                resultPath = resultsPath + str(item["id"]) + ".txt"
                resultFile = open(resultPath, "w")
                resultFile.write(text)
                resultFile.close()
                logging.info("gpt done")
                queueManager.update(item["id"], "done")
                
                
            elif item["type"] == "sd":
                logging.info("item is sd")
                queueManager.update(item["id"], "processing")
                image = sd.generate(item["params"]["prompt"], item["params"]["num_inference_steps"], item["params"]["width"], item["params"]["height"])
                # save the result to the results folder
                resultPath = resultsPath + str(item["id"]) + ".png"
                saveImage(image, item["id"])
                logging.info("sd done")
                queueManager.update(item["id"], "done")
                
    logging.info("sleeping")
    print("sleeping")
    time.sleep(2)
    


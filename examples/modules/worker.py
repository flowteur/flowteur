import requests
from mastodon import Mastodon
import json
from time import sleep
import logging
import urllib.parse
import time
import random
import os

logging.basicConfig(level=logging.DEBUG)

#   Set up Mastodon
mastodon = Mastodon(
    access_token = 'token.secret',
    api_base_url = os.environ.get("MASTODON_URL")
)

apiUrl = os.environ.get("API_URL")
token = os.environ.get("API_TOKEN")


apiUrl = "http://localhost:5000"
token = "autobot3000"

def getPrompts(model="gpt2-large", text="test",min_length=20, max_length=50, no_repeat_ngram_size=1, top_p=0.5):
    # encode the text to be sent trough http parameters
    logging.debug("Getting prompts for text: " + text)
    text = urllib.parse.quote(text)
    print(apiUrl)
    response = requests.get(apiUrl + '/api/gpt/generate?token='+token+'&model='+model+'&text='+text+'&min_length='+str(min_length)+'&max_length='+str(max_length)+'&no_repeat_ngram_size='+str(no_repeat_ngram_size)+'&top_p='+str(top_p))
    logging.debug("Got response: " + str(response.json()))
    
    while True:
        # check if the worker is done
        worker = getWorkerStatus(response.json())

        if worker["status"] == "done":
            # get the result
            result = getWorkerResult(str(response.json()), "text")
            logging.debug("Got result: " + str(result))
            return result
        else:
            logging.debug("Worker not done yet, waiting 5 seconds")
            time.sleep(5)
    

def getImage(text):
    text = urllib.parse.quote(text)
    logging.debug("Getting image for text: " + text)
    response = requests.get(apiUrl + '/api/sd/generate?height=512&width=512&num_inference_steps=17&prompt='+text+'&token='+token)
    #logging.debug("Got response: " + str(response.json()))
    while True:
        # check if the worker is done
        worker = getWorkerStatus(response.json())

        if worker["status"] == "done":
            # get the result
            result = getWorkerResult(str(response.json()), "image")
            logging.debug("Got result: " + str(result))
            return result
        else:
            logging.debug("Worker not done yet, waiting 5 seconds")
            time.sleep(5)
        return response.json()

def getWorkerStatus(id):
    response = requests.get(apiUrl + '/api/queue?token='+token)
    #logging.debug("Got response: " + str(response.json()))
    # for each worker, check if it's the one we're looking for
    response = response.json()
    for worker in response:
        if worker["id"] == id:
            logging.debug("Found worker: " + str(worker))
            return worker
    return "not found"


def getWorkerResult(id : int, type: str):
    if type == "image":
        logging.debug("Getting image for worker: " + str(id))
        response = requests.get(apiUrl + '/api/queue/'+str(id)+'?token='+token)
        # read image from response
        return response.content
    elif type == "text":
        logging.debug("Getting text for worker: " + str(id))
        response = requests.get(apiUrl + '/api/queue/'+str(id)+'?token='+token)
        return response.json()
    return "not found"


def postImage(image, text):
    logging.debug("Posting image: " + str(image))
    # post image
    media = mastodon.media_post(image)
    mastodon.status_post(text, media_ids=media)
    return True

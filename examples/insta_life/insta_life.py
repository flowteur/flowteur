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

# open words.txt and read a random line
with open('words.txt', 'r') as f:
    words = f.readlines()
    word = words[random.randint(0, len(words))]
    
print("Posting image for word: " + word)

def getPrompts(text):
    # encode the text to be sent trough http parameters
    logging.debug("Getting prompts for text: " + text)
    text = urllib.parse.quote(text)
    response = requests.get(apiUrl + '/api/gpt/generate?token='+token+'&text='+text)
    logging.debug("Got response: " + str(response.json()))
    return response.json()

def getImage(text):
    text = urllib.parse.quote(text)
    logging.debug("Getting image for text: " + text)
    response = requests.get(apiUrl + '/api/sd/generate?height=512&width=512&num_inference_steps=17&prompt='+text+'&token='+token)
    logging.debug("Got response: " + str(response.json()))
    return response.json()

def getWorkerStatus(id):
    response = requests.get(apiUrl + '/api/queue?token='+token)
    logging.debug("Got response: " + str(response.json()))
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

# get todays time Hour:Minute
now = time.strftime("%H:%M")


id = getPrompts("New instagram picture #" + word)

while True:
    workerStatus = getWorkerStatus(id)
    if workerStatus["status"] == "done":
        break
    print(workerStatus["status"])
    print("sleeping for 10 seconds")
    sleep(10)

text = getWorkerResult(id, "text")["result"]

id = getImage(text)

while True:
    workerStatus = getWorkerStatus(int(id))
    if workerStatus["status"] == "done":
        break
    print(workerStatus["status"])
    print("sleeping for 10 seconds")
    sleep(10)

image = getWorkerResult(id, "image")
# save image to file
with open("image.png", "wb") as f:
    f.write(image)
postImage("image.png", text)
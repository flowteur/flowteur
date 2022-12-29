import string
import random
import os
import requests

def getInstanceInf():
   instanceId = os.environ['INSTANCE_ID']
   url = os.environ['FUNCTION_DOMAIN']
   token = os.environ['TOKEN']
   tunnelUrl = "https://"+instanceId+".tunnel.stableai.club"

   # make a request to the function api url
   response = requests.get(url + "/api/instance/callback?token=" + token + "&requestId=" + instanceId + "&instance_url=" + tunnelUrl)
   print(response.text)
   
getInstanceInf()

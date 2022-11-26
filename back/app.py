from flask import Flask, send_file, request
from flask_restx import Resource, Api
import modules.queueManager as queue

import os
import io
app = Flask(__name__)
api = Api(app)
# enable debug mode
app.config['DEBUG'] = True

ns = api.namespace('Flowteur', description='Flowteur API')

# get env var for token API_TOKEN

token = os.environ.get("API_TOKEN")

def checkToken(tokenInput):
    if tokenInput == token:
        return True
    else:
        return False



@api.route("/api/queue/<resultId>")
class Queue(Resource):
    @ns.param('token', 'Auth token')
    @ns.param('resultId', 'Text to generate image from')
    def get(self, resultId):
        if checkToken(request.args.get("token")):
            result = queue.read(resultId)
            # check if the result is a string or a byte array
            if isinstance(result, str):
                # return a json object with the result
                return {"result": result}
            elif isinstance(result, bytes):
                return send_file(io.BytesIO(result), mimetype='image/png')
            
            return queue.read(resultId)
        return {"error": "invalid token"}
    

@api.route("/api/queue")
class Queue(Resource):
    @ns.param('token', 'Auth token')
    def get(self):
        if checkToken(request.args.get("token")):
            if id :
                return queue.readAll()
        return {"error": "invalid token"}


@api.route("/api/sd/generate")
class StableDiff(Resource):
    @ns.param('token', 'Auth token')
    @ns.param('prompt', 'Text to generate image from')
    @ns.param('num_inference_steps', 'Number of inference steps')
    @ns.param('width', 'Width of the image')
    @ns.param('height', 'Height of the image')
    def get(self):
        if checkToken(request.args.get("token")):
            # add a param with flask_restx
            prompt = request.args.get('prompt')
            num_inference_steps = request.args.get('num_inference_steps')
            width = request.args.get('width')
            height = request.args.get('height')
            
            return queue.add("sd", {"prompt": prompt if prompt else "flowers", "num_inference_steps": num_inference_steps if num_inference_steps else "1" , "width": width if width else "256", "height": height if height else "256"}, "pending")
        return {"error": "invalid token"}

@api.route("/api/gpt/generate")
class Gpt(Resource):
    @ns.doc('generate text ')
    @ns.param('token', 'Auth token')
    @ns.param('text', 'Text to generate text from')
    def get(self):
        if checkToken(request.args.get("token")):
            # add a param with flask_restx
            text = str(request.args.get('text'))
            return queue.add("gpt", {"text": text}, "pending")
        return {"error": "invalid token"}


if __name__ == "__main__":
    app.run(debug=True)

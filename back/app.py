from flask import Flask, send_file, request
from flask_restx import Resource, Api
from flask_cors import CORS
import os
import io
import json
import modules.queueManager as queue

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# enable debug mode
app.config['DEBUG'] = True

ns = api.namespace('Flowteur', description='Flowteur API')

# get env var for token API_TOKEN

token = os.environ.get("API_TOKEN")


def checkToken(tokenInput: str):
    if tokenInput == token:
        return True
    else:
        return False


# add a rout named api/entrypoint who returns a json of file apiEntrypoint.json
@api.route("/api/entrypoint")
@api.doc(
    params={
        'token': 'Auth token',
        }
)
class EntryPoint(Resource):
    def get(self):
        if checkToken(request.args.get("token")):
            # open the file
            apiEntrypointFile = open("apiEntrypoint.json", "r")
            # read the file as a json
            apiEntrypoint = json.load(apiEntrypointFile)
            # close the file
            apiEntrypointFile.close()
            # return the json
            return apiEntrypoint
            
            
            
            
        return {"error": "invalid token"}


@api.route("/api/queue/<id>")
@api.doc(
    params={
        'token': 'Auth token',
        'id': 'Worker ID'
        }
)
class QueueId(Resource):
    def get(self, id):
        if checkToken(request.args.get("token")):
            result = queue.read(id)
            # check if the result is a string or a byte array
            if isinstance(result, str):
                # return a json object with the result
                return {"result": result}
            elif isinstance(result, bytes):
                return send_file(io.BytesIO(result), mimetype='image/png')
            
            return queue.read(id)
        return {"error": "invalid token"}
    

@api.route("/api/queue")
@api.doc(
    params={
        'token': 'Auth token',
        }
)
class checkQueue(Resource):
    def get(self):
        if checkToken(request.args.get("token")):
            if id :
                return queue.readAll()
        return {"error": "invalid token"}

# add a remover for the queue
@api.route("/api/queue/remove/<resultId>")
@api.doc(
    params={
        'token': 'Auth token',
        }
)
class delQ(Resource):
    def get(self, resultId):
        if checkToken(request.args.get("token")):
            return queue.remove(int(resultId))
        return {"error": "invalid token"}


@api.route("/api/sd/generate")
@api.doc(
    params={
        'token': 'Auth token',
        'prompt': 'Prompt text',
        'num_inference_steps': 'Number of inference steps',
        'width': 'Image width',
        'height': 'Image height'
        }
)
class StableDiff(Resource):
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
@api.doc(
    params={
        'token': 'Auth token',
        'text': 'Text to generate image from',
        'model': 'Model to use',
        'min_length': 'Minimum length of the generated text',
        'max_length': 'Maximum length of the generated text',
        'eos_token_id': 'End of sentence token id',
        'pad_token': 'Padding token id',
        'top_k': 'Top k',
        'top_p': 'Top p',
        'no_repeat_ngram_size': 'No repeat ngram size'
        }
)

class Gpt(Resource):
    def get(self):
        if checkToken(request.args.get("token")):
            # add a param with flask_restx
            model = request.args.get('model') if request.args.get('model') else "gpt2-large"
            text = request.args.get('text') if request.args.get('text') else "flowers"
            min_length = request.args.get('min_length') if request.args.get('min_length') else 20
            max_length = request.args.get('max_length') if request.args.get('max_length') else 80
            eos_token_id = request.args.get('eos_token_id') if request.args.get('eos_token_id') else 5
            pad_token = request.args.get('pad_token') if request.args.get('pad_token') else 1
            top_k = request.args.get('top_k') if request.args.get('top_k') else 10
            top_p = request.args.get('top_p') if request.args.get('top_p') else 0.7
            no_repeat_ngram_size = request.args.get('no_repeat_ngram_size') if request.args.get('no_repeat_ngram_size') else 1
            
            return queue.add("gpt", {"model": model, "text": text, "min_length": min_length, "max_length": max_length, "eos_token_id": eos_token_id, "pad_token": pad_token, "top_k": top_k, "top_p": top_p, "no_repeat_ngram_size": no_repeat_ngram_size}, "pending")

        return {"error": "invalid token"}
    


if __name__ == "__main__":
    app.run(debug=True)

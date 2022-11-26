import os
from diffusers import StableDiffusionPipeline
from PIL import Image
from huggingface_hub import HfApi
from huggingface_hub.commands.user import _login

# get env var for token
huggingface_token = os.environ.get("HUGGINGFACE_TOKEN")

_login(HfApi(), token=huggingface_token)

notLoaded = True

model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, low_cpu_mem_usage=True)
pipe = pipe.to("cpu")
def dummy(images, **kwargs):
    return images, False
pipe.safety_checker = dummy


def generate(prompt, num_inference_steps=16, width=256, height=256):
    image = pipe(str(prompt), num_inference_steps=int(num_inference_steps), width=int(width), height=int(height)).images[0]
    return image
import os
from diffusers import StableDiffusionPipeline
from PIL import Image

# get env var for token
huggingface_token = os.environ.get("HUGGINGFACE_TOKEN")

model_id = "CompVis/stable-diffusion-v1-4"

def generate(prompt, num_inference_steps=16, width=256, height=256):
    pipe = StableDiffusionPipeline.from_pretrained(model_id, low_cpu_mem_usage=True, use_auth_token=huggingface_token)
    pipe = pipe.to("cpu")
    
    # remove nsfw filter
    def dummy(images, **kwargs):
        return images, False
    
    #pipe.safety_checker = dummy
    image = pipe(str(prompt), num_inference_steps=int(num_inference_steps), width=int(width), height=int(height)).images[0]
    return image
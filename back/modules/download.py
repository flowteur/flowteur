import os
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from diffusers import StableDiffusionPipeline
# get env var for token
huggingface_token = os.environ.get("HUGGINGFACE_TOKEN")

StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", use_auth_token=huggingface_token)
GPT2Tokenizer.from_pretrained("sberbank-ai/mGPT", use_auth_token=huggingface_token)
GPT2LMHeadModel.from_pretrained("sberbank-ai/mGPT", use_auth_token=huggingface_token)

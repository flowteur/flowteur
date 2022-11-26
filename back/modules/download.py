import os
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from diffusers import StableDiffusionPipeline
# get env var for token
huggingface_token = os.environ.get("HUGGINGFACE_TOKEN")

GPT2Tokenizer.from_pretrained("sberbank-ai/mGPT", use_auth_token=huggingface_token)
GPT2LMHeadModel.from_pretrained("sberbank-ai/mGPT", use_auth_token=huggingface_token)
model_id = "runwayml/stable-diffusion-v1-5"
StableDiffusionPipeline.from_pretrained(model_id, low_cpu_mem_usage=True, use_auth_token=huggingface_token)
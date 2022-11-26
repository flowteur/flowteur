import os
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from huggingface_hub import HfApi
# get env var for token
huggingface_token = os.environ.get("HUGGINGFACE_TOKEN")

notLoaded = True

def load():
    global notLoaded
    global tokenizer
    global model
    if notLoaded:
        tokenizer = GPT2Tokenizer.from_pretrained("sberbank-ai/mGPT", use_auth_token=huggingface_token)
        model = GPT2LMHeadModel.from_pretrained("sberbank-ai/mGPT", use_auth_token=huggingface_token)

        notLoaded = False
        return tokenizer, model   
    return tokenizer, model


def generate(text, min_length=100, max_length=100, eos_token_id=5, pad_token=1, top_k=10, top_p=0.0, no_repeat_ngram_size=5):
    # get the tokenizer and model and out
    tokenizer, model = load()
    
    input_ids = tokenizer.encode(text, return_tensors="pt")
    out = model.generate(
            input_ids, 
            min_length=100, 
            max_length=100, 
            eos_token_id=5, 
            pad_token=1,
            top_k=10,
            top_p=0.0,
            no_repeat_ngram_size=5
    )
    generated_text = list(map(tokenizer.decode, out))[0]
    print(generated_text)
    return generated_text

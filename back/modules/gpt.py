import os
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import logging


# get env var for token
huggingface_token = os.environ.get("HUGGINGFACE_TOKEN")


def generate(model: str, text: str, min_length=30, max_length=100, eos_token_id=5, pad_token=1, top_k=10, top_p=0.7, no_repeat_ngram_size=1) -> str:
    logging.info("Generating text")

    tokenizer = GPT2Tokenizer.from_pretrained(
        model, use_auth_token=huggingface_token)
    model:  GPT2LMHeadModel = GPT2LMHeadModel.from_pretrained(
    model, use_auth_token=huggingface_token)

    input_ids : str = tokenizer.encode(text, return_tensors="pt")
    out = model.generate(
            input_ids = input_ids,
            max_length = int(max_length),
            min_length = int(min_length),
            eos_token_id = int(eos_token_id), 
            pad_token = int(pad_token),
            top_k = int(top_k),
            top_p = float(top_p),
            no_repeat_ngram_size = int(no_repeat_ngram_size),
            do_sample=True
    )
    generated_text : list = list(map(tokenizer.decode, out))[0]
    return generated_text
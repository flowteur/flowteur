# Flowteur

API for ML on CPU

## TODO
- [ ] Add status_msg to queue
- [ ] 

## Routes

/api/sd/generate
/api/gpt/generate
/api/queue/remove/{resultId}
/api/queue
/api/queue/{id}

**GET** /api/sd/generate

params: token, prompt, num_inference_steps, width, height

returns: queue id

**GET** /api/gpt/generate

params: token, text, model, min_length, max_length,eos_token_id, pad_token, top_k, top_p,no_repeat_ngram_size

returns: queue id


**GET** /api/queue/<id>

params: token

```json
[
    {
        "id": "number",
        "type": "string",
        "params": "object",
        "status": "string"
    }
]
```

# Flowteur

Flowter is a ML API using cpu and gpu
Id has been designed to be runned on a raspberrypi

## Backend
The backend is sliced into 2 parts
- API
- Worker

The api can be used to make generation request and the worker is here to fulfill the request one by one

###  QuickStart

**Docker**

copy .env.example into .env and modify it 

`docker-compose up `


**Python**

You need to have installed
- Tensorflow
- Pytorch

```python
pip install -r requirements.txt
```

Launch the flasker server and the worker into seperate terminals
`python app.py`

`python worker.py`


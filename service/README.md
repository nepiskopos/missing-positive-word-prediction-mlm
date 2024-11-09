## Missing word predictor service

This directory contains an the API-based missing word predicition service.

To manually launch the service in a web server, you can use [uvicorn](https://www.tutorialspoint.com/fastapi/fastapi_uvicorn.htm).

### Launch service
```console
cd missing-positive-word-prediction-mlm/service
uvicorn main:app --host 0.0.0.0 --port 8888 --reload
```

Now, the service listens for HTTP requests at the following URL addresses under port 8888:
- http://localhost:8888/
- http://127.0.0.1:8888/
- http://0.0.0.0:8888/

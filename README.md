# Missing word predictor using BERT MLM and NLTK

This repository contains API-based ML application which predicts a missing word in a sentence, which gives the sentence a positive vibe, using BERT MLM and NLTK.

The developed solution predicts a single missing word, which is masked using the <blank> keyword.

For example, given the sentence "I wish you have a <blank> day!" as the service input should return a list of words like "great", "worderful", "good", "lovely", etc., so that the sentiment is not negative.

---

To easily use this application, use the provided docker container, which contains all the required setup instructions and procedure to build and deploy this application to production.

For a scalable option, a dockerized load-balancer solution is provided, which spawns an Nginx server which redirects any incoming traffic to any of the 4 spawned docker containers backends.

---

To launch the service in a single docker container, first you need to [install Docker](https://docs.docker.com/desktop/install/linux/) and [buildx](https://docs.docker.com/reference/cli/docker/buildx/).

After you setup Docker and launch the Docker service, use the following commands to build the Docker Image and run the Container.

### To build the Docker image naming it "nepiskopos/predict" using the provided Dockerfile
```console
cd missing-positive-word-prediction-mlm
docker buildx build -t nepiskopos/predict .
```

### To deploy the application to production using a Docker container named "predict" which accepts network traffic in container port 8000 through host port 8888
```console
docker run -p 8888:8000 --name predict nepiskopos/predict
```

Then, you can send POST HTTP requests to the application API and get the response as a JSON object.

---

To launch a Load-balancing service, first you need to [install Docker](https://docs.docker.com/desktop/install/linux/) and [Docker Compose](https://docs.docker.com/compose/install/linux/).

After you setup Docker and launch the Docker service, use the following command to easily build the Docker Image and run all the Containers.

### To build the Docker image naming it "nepiskopos/predict-lb" using the provided Dockerfile
```console
cd missing-positive-word-prediction-mlm/load_balancer
docker-compose up
```

Then, you can send POST HTTP requests to the application API and get the response as a JSON object, just like before, but this time more requests can be served in parallel.

---

# To send a post HTTP request to the application API on a running server using cURL (command-line tool):
```console
curl -X 'POST' 'http://127.0.0.1:8888/api/predict_single' 
     -H 'accept: application/json'
     -H 'Content-Type: text/plain'
     -d 'I wish you have a <blank> day!'
```

The service response to the HTTP request is a JSON object which contains a list of strings the "content" key or with a suitable error message in case an error occurs or no suitable words are predicted.

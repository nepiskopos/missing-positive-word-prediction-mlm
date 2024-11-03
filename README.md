# Missing word predictor using MLMs

This repository contains API-based ML application which predicts a missing word in a sentence which gives the sentence a positive vibe.

Predict a single missing word in a sentence, masked under the keyword, which is given to the API as an input string. The predicted missing words always give a positive sentiment to the input sentence.

---

To easily use this application, use the provided docker container, which contains all the required setup instructions and procedure to build and deploy this application to production.

# Docker setup and execution on Ubuntu 20.04

## Install Docker
```console
sudo apt-get -y install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
sudo apt-get -y install docker-ce
```


## Create a group for docker users
```console
sudo groupadd docker
```

## Add your user to the docker group
```console
sudo usermod -aG docker $USER
```

## Apply the new group membership
```console
newgrp docker
su - ${USER}
exit # IT IS NEEDED, AT LEAST AFTERWARDS
```

## Confirm your user was added to the docker group
```console
id -nG
```

## Start docker service and enable automatic start on boot
```console
sudo systemctl enable docker.service
sudo systemctl start docker.service
```

## (Optional) if docker service can not be activated, reboot
```console
reboot
```

## Test docker installation
```console
docker run hello-world
```

## Build a custom application Docker image named "nepiskopos/appimg" using our Dockerfile
```console
docker build -t nepiskopos/appimg:latest -f ./Dockerfile .
```

## Deploy the application to production using a Docker container named "appcont" which accepts network traffic in port 8000
```console
docker run -p 8000:8000 --name appcont nepiskopos/appimg
```

---

# Send a post HTTP request to the application API on a running server using curl (command-line tool):
```console
curl -X 'POST' 'http://API_IP_ADDRESS:PORT/predict' -H 'accept: application/json' -H 'Content-Type: text/plain' -d 'I wish you have a day!'
```

Request response is a JSON object which contains a list of strings which satisfy the positive sentiment requirements under the "content" name (key) or with a suitable error message in case an error occurs or no suitable words are predicted.

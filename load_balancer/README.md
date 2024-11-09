# Load-balancing prediction service

This directory provides a set of tools to create a Load-balancing version of the provided forecast service, using a containerized [Nginx server](https://nginx.org/) as the service frontend and 4 forecast containers as the service backend. This setup balances inbound traffic reducing response time, improving service availability.

---

To launch a Load-balancing service, first you need to [install Docker](https://docs.docker.com/desktop/install/linux/) and [Docker Compose](https://docs.docker.com/compose/install/linux/).

After you setup Docker and launch the Docker service, use the following command to easily build the Docker Image and run all the Containers.

### To build the Docker image naming it "nepiskopos/predict-lb" using the provided Dockerfile
```console
cd missing-positive-word-prediction-mlm/load_balancer
docker-compose up
```

The service response to the HTTP request is a JSON object which contains the predicted values under the "forecast" key.

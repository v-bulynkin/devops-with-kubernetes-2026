# Ping-pong app

Application that simply responds with "pong $NUMBER" to a GET request and increases a counter (the $NUMBER) so that you can see how many requests have been sent. The counter is kept in memory so it resets at app restart. Route requests directed '/pingpong' to it.

Works together with [log-output app](../log-output/README.md), showing current score on its webpage (via HTTP GET requests to URL /pings from log-output-reader container).

## Build image
```
# in the Dockerfile directory
docker build -t bvadocker/ping-pong:2.1 .
# push
docker push bvadocker/ping-pong:2.1
```
Dockerhub page: https://hub.docker.com/r/bvadocker/ping-pong

## Start in k8s
First of all, persistent volume and "exercises" namespace must be created (from log-output):
```
kubectl apply -f ../log-output/pv -f ../log-output/manifests/namespace.yaml
```

Then, start log-output and ping-pong:
```
kubectl apply -f ../log-output/manifests -f manifests
```

## External access to the webpage
If you use k3d, you should forward a port to your cluster from Docker, for example, `-p 8081:80@loadbalancer`.  
In this case, the external access will be http://\<your docker server ip or localhost\>:8081  
Ingress path: /pingpong  
Service port: 5000  
Pod port: 5000

URL example: http://192.168.1.21:8081/pingpong

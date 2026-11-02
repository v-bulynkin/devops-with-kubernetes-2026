# Ping-pong app

Application that simply responds with "pong $NUMBER" to a GET request and increases a counter (the $NUMBER) so that you can see how many requests have been sent. The counter is kept in Postgres DB. Route requests directed '/pingpong' to it.

Works together with [log-output app](../log-output/README.md), showing current score on its webpage (via HTTP GET requests to URL /pings from log-output-reader container).

## Build image
```
# in the Dockerfile directory
docker build -t bvadocker/ping-pong:2.7 .
# push
docker push bvadocker/ping-pong:2.7
```
Dockerhub page: https://hub.docker.com/r/bvadocker/ping-pong

## Start / stop
Start / update
```
kubectl apply -k ../log-output
kubectl apply -k .
```

Stop and keep persistent data:
```
kubectl delete deploy -n exercises ping-pong log-output
kubectl delete statefulset -n exercises ping-pong-pg-stset
```

Stop and delete everything:
```
kubectl delete -k .
kubectl delete -k ../log-output
```

## External access to the webpage
If you use k3d, you should forward a port to your cluster from Docker, for example, `-p 8081:80@loadbalancer`.  
In this case, the external access will be http://\<your docker server ip or localhost\>:8081  
Ingress path: /pingpong  
Service port: 5000  
Pod port: 5000

URL example: http://k1:8081/pingpong

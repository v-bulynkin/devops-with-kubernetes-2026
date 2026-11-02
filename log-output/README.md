# Log output app

Shows the following information on the web page (example):
```
file content: this text is from file

env variable: MESSAGE=hello world

2026-10-31T13:30:54.334Z: 2a6d9f64-1eb6-4a9f-b1b5-2924f14e138a

Ping / Pongs: 2
```

The Log output app is divided into two containers which work in one pod:

1. Writer - generates the string starts from current time and writes it every 5 seconds to file `/shared/data.txt` and to stdout;
1. Reader - accumulates information and shows it on the webpage.

The `/shared` directory is an persistent volume (PV) in a pod so both containers can work with it.

"File content" and "env variable" are taken from the [ConfigMap](manifests/configmap.yaml).  
A value in the "Ping / Pongs" sting is obtained from [ping-pong app](../ping-pong/).

## Build image
```
# in the Dockerfile directory
docker build -t bvadocker/log-output-writer:2.1 -f Dockerfile.writer .
docker build -t bvadocker/log-output-reader:2.5 -f Dockerfile.reader .
# push
docker push bvadocker/log-output-writer:2.1
docker push bvadocker/log-output-reader:2.5
```
Dockerhub pages:  
https://hub.docker.com/r/bvadocker/log-output-writer  
https://hub.docker.com/r/bvadocker/log-output-reader

## Start / stop
Start / update
```
kubectl apply -k .
kubectl apply -k ../ping-pong
```

Stop and keep persistent data:
```
kubectl delete deploy -n exercises ping-pong log-output
kubectl delete statefulset -n exercises ping-pong-pg-stset
```

Stop and delete everything:
```
kubectl delete -k ../ping-pong
kubectl delete -k .
```

## External access to the webpage
If you use k3d, you should forward a port to your cluster from Docker, for example, `-p 8081:80@loadbalancer`.  
In this case, the external access will be http://\<your docker server ip or localhost\>:8081  
Ingress path: /  
Service port: 5000  
Pod port: 5000

URL example: http://k1:8081
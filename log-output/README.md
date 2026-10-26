# Log output app

Application that generates a random string on startup, stores this string into memory, and outputs it every 5 seconds with a timestamp. e.g.
```
2020-03-30T12:15:17.705Z: 8523ecb1-c716-4cb6-a044-b9e83bb98e43
2020-03-30T12:15:22.705Z: 8523ecb1-c716-4cb6-a044-b9e83bb98e43
```

Splitted to two containers which work in one pod:

1. Writer - generates strings and writes it to file `/shared/data.txt`;
1. Reader - reads `/shared/data.txt` and shows it on a webpage.

The `/shared` directory is an persistent volume (PV) in a pod so both containers can work with it.

Log output app works together with ping-pong app, which adds second string to the webpage.

## Build image
```
# in the Dockerfile directory
docker build -t bvadocker/log-output-writer:1.11 -f Dockerfile.writer .
docker build -t bvadocker/log-output-reader:1.11 -f Dockerfile.reader .
# push
docker push bvadocker/log-output-writer:1.11
docker push bvadocker/log-output-reader:1.11
```
Dockerhub pages:  
https://hub.docker.com/r/bvadocker/log-output-writer  
https://hub.docker.com/r/bvadocker/log-output-reader

## Start in k8s
First of all, persistent volume must be created:
```
kubectl apply -f pv
```

Then, you can kick off the deploy with pvc/service/ingress:
```
kubectl apply -f manifests
```

At the end, start [ping-pong app](../ping-pong/README.md).

## See logs
```
kubectl logs -f log-output-writer<press tab> <--tail 1>
```

## Webpage
Service port: 5000  
Pod port: 5000

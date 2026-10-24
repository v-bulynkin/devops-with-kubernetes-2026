# Log output app

Application that generates a random string on startup, stores this string into memory, and outputs it every 5 seconds with a timestamp. e.g.
```
2020-03-30T12:15:17.705Z: 8523ecb1-c716-4cb6-a044-b9e83bb98e43
2020-03-30T12:15:22.705Z: 8523ecb1-c716-4cb6-a044-b9e83bb98e43
```
Also, show the current string on a webpage.

## Build image
```
# in the Dockerfile directory
docker build -t bvadocker/log-output:1.7 .
# push
docker push bvadocker/log-output:1.7
```
Dockerhub page: https://hub.docker.com/r/bvadocker/log-output

## Start in k8s
```
kubectl apply -f manifests
```

## See logs
```
kubectl logs -f log-output<press tab> <--tail 1>
```

## Webpage
Service port: 5000  
Pod port: 5000

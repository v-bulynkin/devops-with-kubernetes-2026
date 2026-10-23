# Log output app

Application that generates a random string on startup, stores this string into memory, and outputs it every 5 seconds with a timestamp. e.g.
```
2020-03-30T12:15:17.705Z: 8523ecb1-c716-4cb6-a044-b9e83bb98e43
2020-03-30T12:15:22.705Z: 8523ecb1-c716-4cb6-a044-b9e83bb98e43
```

## Build image
```
# in the Dockerfile directory
docker build -t <your tag> .
```
or use the ready image from https://hub.docker.com/r/bvadocker/log-output

## Start in k8s
```
kubectl create deploy log-output --image=docker.io/bvadocker/log-output
```

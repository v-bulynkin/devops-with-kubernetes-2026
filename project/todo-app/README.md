# Todo app

Application web server that outputs "Server started in port NNNN" when it is started. Default port value: 5000

## Build image
```
# in the Dockerfile directory
docker build -t <your tag> .
```
or use the ready image from https://hub.docker.com/r/bvadocker/todo-app:1.2

## Start in k8s
```
kubectl create deploy todo-app --image=docker.io/bvadocker/todo-app
```

## Start in docker
```
# With port specified
docker run --rm --name todo-app -p 8080:8080 -e PORT=8080 docker.io/bvadocker/todo-app:1.2
# Default port 5000
docker run --rm --name todo-app -p 5000:5000 docker.io/bvadocker/todo-app:1.2
```


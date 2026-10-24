# Todo app

Application web server that outputs "Server started in port NNNN" when it is started. Default port value: 5000

## Build image
```
# in the Dockerfile directory
docker build -t <your tag> .
```
or use the ready image from https://hub.docker.com/r/bvadocker/todo-app

## Start in k8s
```
kubectl create deploy todo-app --image=docker.io/bvadocker/todo-app:1.2
# or declaratively
kubectl apply -f ../manifests/deployment.yaml
```

## Start in docker
```
# With port specified
docker run --rm --name todo-app -p 8080:8080 -e PORT=8080 docker.io/bvadocker/todo-app:1.2
# Default port
docker run --rm --name todo-app -p 5000:5000 docker.io/bvadocker/todo-app:1.2
```

## Check if it works in k8s

After the app has started, execute the following command:
```
kubectl port-forward <todo-app pod name> 3000:5000
```
It creates a network tunnel from your local machine (port 3000) straight to the pod (port 5000). While console is captured by this command, you can try:

1. To open http://localhost:3000 in a web-browser.
1. In another console session, execute `curl localhost:3000`.

In both cases, the application should return "Server started in port 5000".

## Service (external access to the webpage)
```
kubectl apply -f ../manifests/service.yaml
```
It opens NodePort 30080 to targetPort 5000.  
If you use k3d, you should forward a port to your cluster from Docker, for example, `--port 8082:30080@agent:0`.  
In this case, the external access will be http://<your docker server ip or localhost>:8082
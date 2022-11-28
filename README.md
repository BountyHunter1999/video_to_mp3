# video_to_mp3

## if requirements fail to install for mysql

- `sudo apt-get install default-libmysqlclient-dev`

## For secret

- `echo -n Auth123 | base64` MYSQL_PASSWORD
- `echo -n pokemon | base64` JWT_SECRET

## To run

- `minikube start`
- in k9s choose 0 to see all
- from the manifest directory `kubectl apply -f ./`

## What is happening?

### In manifest directory

- we wrote the infrastructure code for our auth deployment
- when we apply the yaml files here will interface with the k8s api, which is the API for our k8s cluster(to interface with our k8s cluster)
- these files are going to interface with that API to provide services and resources(configmap and its secrets)
- to do that all we need to do is `kubectl apply -f ./` from the manifest directory to apply all the files in the manifest directory

## to make sure mp3converter.com gets routed to localhost

- make sure minikube is running
- `sudo nano /etc/hosts`
- map the loop back address `127.0.0.1` (local host also resolves to this) to mp3converter.com
        - `127.0.0.1       mp3converter.com`
- so now whenever we enter mp3converter.com into our browser or send request to this host it's going to resolve to local host
- `minikube addons list` and enable ingress addon
        - `minikube addons enable ingress`
- whenever we want to run this microservice architecture we're going to run `minikube tunnel` command

## important commands

- to scale down `kubectl scale deployment --replicas=0 gateway`

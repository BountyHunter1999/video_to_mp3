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

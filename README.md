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

## for rabbitmq management GUI access

- make sure minikube is running
- `sudo nano /etc/hosts`
- map the loop back address `127.0.0.1` (local host also resolves to this) to mp3converter.com
        - `127.0.0.1       rabbitmq-manager.com`
- `kubectl port-forward services/rabbitmq 15672:15672` if nothing works we can do this too
        - pwd and username both are guest

## important commands

- to scale down `kubectl scale deployment --replicas=0 gateway`

## Connect to mysql

- `kubectl get pod` to get the pod name
- `kubectl exec -it pods/mysql-59bcb9bdc7-bc66c bash` get inside the pod
- `mysql -u auth_user auth -p` a prompt appears to enter the password
- `SHOW DATABASES` to see the available databases
- `SHOW TABLES` to see the available tables
- `SELECT * FROM user` to see the available user in the table user

### Later on

- update the email to an actual email so u can download
- `UPDATE user SET email = "your_email@gmail.com"`
- get a new token after you do this

## See if our mp3 are in mongodb

- get into the mongodb container
- `mongo` to enter into its shell
- `show databases` we can see mp3 and videos there
- `use mp3` > `show collections` we can see fs.chunks and fs.files
        - with gridsfs the actual file data is stored in chunks and
        - the files will have reference simply a metadata for a collection
                of chunks
- `db.fs.files.find()`: we'll see all of the objects that we have stored
- `db.fs.files.find("_id": ObjectId("object's id"))`

### Download files from mongodb

- `mongofiles --db=mp3 get_id --local=mp3s/test.mp3 '{"$oid": "object's id"}'`
- we will look in mp3 database, get the object by id
- want the local file to be named test.mp3 in the mp3s directory
- we can see this in using `minikube ssh` and inside `/mnt/mongodata`

## Need to fix

- the auth/server is using root fix it to use the auth_user and fix the privileges

## Keep in mind

- if the rabbitmq pod goes down or restarts the gateway uses the same old rabbitmq host using the rabbitmq service name and so when we try to upload a video it will return Internal Server Error.
- so we must restart the gateway service too.

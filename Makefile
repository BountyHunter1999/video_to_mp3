all: |
	kubectl apply -f src/auth/manifests 

mysql_pf: 
	kubectl port-forward mysql-0 3306:3306

mp3_login:
	curl -X POST http://mp3converter.com/login -u mikeyy@tokyo.com:Admin123

mysql_connect:
	kubectl run -it --rm --image=mysql:latest --restart=Never mysql-client -- mysql -h mysql -password="password"

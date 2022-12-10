all: |
	kubectl apply -f src/auth/manifests 

mysql_pf: 
	kubectl port-forward mysql-0 3306:3306

gatewayy_pf:
	kubectl port-forward services/gateway 8080:8080

gateway_login:
	curl -X POST http://localhost:8080/login -u mikeyy@tokyo.com:Admin123

video_upload:
	curl -X POST -F "file=@./Funny_rabbit.mp4" \
	 -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im1pa2V5eUB0b2t5by5jb20iLCJleHAiOjE2NzA2ODM0MTAsImlhdCI6MTY3MDU5NzAxMCwiYWRtaW4iOnRydWV9.0RS520lzUYJiduCHkZ28_vEeCaCVprnkW3U34UagOZk' \
	 http://localhost:8080/upload

scale_down:
	kubectl scale deployment --replicas=1 gateway
	kubectl scale deployment --replicas=1 auth
	kubectl scale deployment --replicas=1 converter

gateway_logs:
	kubectl logs -f gateway

mysql_connect:
	kubectl run -it --rm --image=mysql:latest --restart=Never mysql-client -- mysql -h mysql -password="password"

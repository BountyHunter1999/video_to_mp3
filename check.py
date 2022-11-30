import requests

url = "http://rabbitmq-manager.com:15672/"

res = requests.get(url)
print(res.status_code)

url = "http://rabbitmq-manager.com:15672/"

res = requests.get(url)
print(res.status_code)
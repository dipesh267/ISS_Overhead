import requests

response = requests.get('http://api.open-notify.org/iss-now.json')
response.raise_for_status()
response_code = response.status_code
print(response_code)
if(response_code == 200):
    print(response.json()["iss_position"])
else:
    print("something broke")
import requests

url = "http://localhost:5000/upload"

payload={'password': 'mango'}
files=[
  ('image',('2021-02-14_23-34-54.jpg',open('2021-02-14_23-34-54.jpg','rb'),'image/jpeg'))
]
headers = {}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)
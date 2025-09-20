import requests

url = "https://public-api.wordpress.com/wpcom/v2/work-with-us"
response = requests.get(url)
print(response.json())

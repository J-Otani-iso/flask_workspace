import requests

url = "http://127.0.0.1:5000/users"

response = requests.get(url)

# GET
print("GET")
print(response.status_code)
print(response.json())

# POST
new_user = {
    "name": "Suzuki",
    "age": 28
}

response = requests.post(url, json=new_user)

print("POST")
print(response.status_code)
print(response.json())

print("POST後の結果")
response = requests.get(url)
print(response.json())

# PATCH
update_data = {
    "age": 31
}

response = requests.patch(
    "http://127.0.0.1:5000/users/2",
    json=update_data
)

print("PATCH")
print(response.status_code)
print(response.json())

print("PACTH後の結果")
response = requests.get(url)
print(response.json())

# PUT
replace_data = {
    "name": "Kubo",
    "age": 25
}

response = requests.put(
    "http://127.0.0.1:5000/users/2",
    json=replace_data
)

print("PUT")
print(response.status_code)
print(response.json())

print("PUT後の結果")
response = requests.get(url)
print(response.json())

# DELETE
response = requests.delete(
    "http://127.0.0.1:5000/users/3"
)

print("DELETE")
print(response.status_code)
print(response.json())

print("DELETE後の結果")
response = requests.get(url)
print(response.json())
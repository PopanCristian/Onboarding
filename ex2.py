import requests

token_access = "Bearer ee493b8012fc048bbdd4c6de16e3c963aac76bb42a36430fd990cdc9b049c138"
url_user_resource = "https://gorest.co.in/public/v2/users"

headers = {
    "Authorization": token_access
}
data = {
    "id": "16032002",
    "name": "Popan Cristian Florin",
    "email": "p_cristi10@yahoo.com",
    "gender": "male",
    "status": "active"
}
response_post = requests.post(url_user_resource, headers=headers, json=data,verify=False)

print(f"About new user : {response_post.json()}")
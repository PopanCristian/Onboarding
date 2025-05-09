import requests

list_of_resources = ["https://gorest.co.in/public/v2/users","https://gorest.co.in/public/v2/posts",
                     "https://gorest.co.in/public/v2/comments","https://gorest.co.in/public/v2/todos"]

for resource in list_of_resources:
    response_get = requests.get(resource, verify=False)
    data = response_get.json()

    for each_data in data:
        print(each_data)

    print("--------")
import requests

url_users = "https://gorest.co.in/public/v2/users"
token_access = "Bearer ee493b8012fc048bbdd4c6de16e3c963aac76bb42a36430fd990cdc9b049c138"
response_get = requests.get(url_users, verify=False)
data = {
    "id": "16032002",
    "name": "Nelu Frumuselu",
    "email": "nelu_frumuselu@yahoo.com",
    "gender": "male",
    "status": "active"
}
headers = {
    "Authorization": token_access
}

while True:
    input_user = int(input("Type problem's number between 3 and 6 (0 to quit): "))
    if input_user == 0:  # 0 to quit
        break
    elif input_user == 3:
        # Create a method to verify that after adding the new user, the total number of users has increased by 1
        data = response_get.json()
        total_users = 0
        for each_data in data:
            if each_data["id"] != 0:
                total_users += 1
        print(total_users)
        # now I have current users
        response_post = requests.post(url_users, headers=headers, json=data, verify=False)
        total_users += 1
        print(f"After post method we have {total_users}")
        print("--------------------")

    elif input_user == 4:
        # Create a method that will bring a specified user name by adding a query parameter and use it to retain the
        # user ID
        def get_user_name_by_id(name='Nelu Frumuselu'):
            parameters = {'name': name}
            response = requests.get(url_users, headers=headers, params=parameters, verify=False)
            if response.status_code == 200:
                data = response.json()
                if data:
                    print(f"User {data['name']} have {data['id']}")
                else:
                    print(f"No user have been found with name {name}")
            else:
                print(f"Error code : {response.status_code}")
        get_user_name_by_id()
    elif input_user == 5:
        # Display first 20 active users
        def get_first_20_active_users(status='active'):
            parameters = {'status': status}
            response = requests.get(url_users, headers=headers, params=parameters, verify=False)
            if response.status_code == 200:
                data = response.json()
                nr_active_users = len(data)  # I used len(data) just to prevent the case there are
                print(f"Those {nr_active_users} people active are :")
                # less than 20 people active
                if nr_active_users < 1:
                    print("No one active")
                else:
                    print(f"Those {nr_active_users} people active are :")
                    for user in data[:20]:  # even I have less than 20 people it's fine
                        print(user['name'])
            else:
                print(f"Error code: {response.status_code}")
        get_first_20_active_users()
    elif input_user == 6:
        # Display first 5 users that also have a middle name
        response = requests.get(url_users, headers=headers, verify=False)
        if response.status_code == 200:
            data = response.json()
            count = 5
            ok = 0
            for user in data:
                if count >= 1:
                    if len(user['name'].split()) == 3:  # true means that I have middle name
                        print(user['name'])
                        count -= 1
                        ok = 1
            if ok == 0:
                print("No one have middle name")

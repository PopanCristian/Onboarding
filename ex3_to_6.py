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
    input_user = int(input("Type problem's number between 3 and 7 (0 to quit): "))
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
    elif input_user == 7:
        # For the previously added user, create a post, a comment and a todo.
        # Make sure the methods created at this point to be available for any other user
        def show_all_users():
            """

            :return: display all users from endpoint
            """
            response = requests.get(url_users, verify=False)
            data = response.json()
            return [name['name'] for name in data]


        def get_user_id_by_name(username):
            """

            :param username: User name from /users endpoint
            :return: user's id
            """
            parameters = {'name': username}
            response = requests.get(url_users, verify=False, params=parameters)

            if response.status_code == 200:
                data = response.json()
                if data:
                    return data[0]['id']
                else:
                    return "User not found"
            else:
                return f"Error code status : {response.status_code}"


        def create_post(post_id, user_id, title, body):
            url = "https://gorest.co.in/public/v2/posts"
            load = {
                'id': post_id,
                'user_id': user_id,
                'title': title,
                'body': body
            }
            response = requests.post(url, json=load, headers=headers, verify=False)
            return response.json()


        def create_comment(comment_id, post_id, user_name, email, body):
            url = "https://gorest.co.in/public/v2/comments"
            load = {
                'id': comment_id,
                'post_id': post_id,
                'name': user_name,
                'email': email,
                'body': body
            }
            response = requests.post(url, verify=False, json=load, headers=headers)
            return response.json()


        def create_todo(todo_id, user_id, todo_title, due_on, status):
            url = "https://gorest.co.in/public/v2/todos"
            load = {
                'id': todo_id,
                'user_id': user_id,
                'title': todo_title,
                'due_on': due_on,
                'status': status
            }
            response = requests.post(url, verify=False, json=load, headers=headers)
            return response.json()


        print(show_all_users())  # First I should list all the users from endpoint /users
        user_name = input("Choose a name :")
        user_id = get_user_id_by_name(user_name)  # now I have user id

        new_user_post = create_post(post_id='123', user_id=user_id, title='brain damaged',
                                    body="This is the body of post")
        print(f"The post contains next info: {new_user_post}")  # I create a new post for chosen user

        new_user_comment = create_comment(comment_id='321', post_id=new_user_post["id"], user_name=user_name,
                                          email="abracadabra@yahoo.com", body="Somebody I used to know")
        print(f"The comment contains next info: {new_user_comment}")  # I create a new comment for that new post

        new_user_todo = create_todo(todo_id="123", user_id=user_id, todo_title="I am hungry af",
                                    due_on="2025-05-20T00:00:00.000+05:30", status="pending")
        print(f"The todo task contains next info: {new_user_todo}")

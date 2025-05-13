import requests


def create_url(endpoint):
    return f"{BASE_URL}{endpoint}"


def get_info_from_all_endpoints():
    users_url = create_url("users")
    posts_url = create_url("posts")
    comments_url = create_url("comments")
    todos_url = create_url("todos")

    list_of_resources = [users_url, posts_url,  comments_url, todos_url]

    for resource in list_of_resources:
        response = requests.get(resource, verify=False)
        data = response.json()

        for each_data in data:
            print(each_data)

        print("--------")


def create_new_user_and_display():
    url_user_resource = create_url("users")

    headers = {
        "Authorization": token_access
    }
    id = int(input("Desired id: "))
    name = input("Desired name: ")
    email = input("Desired email: ")
    gender = input("Your gender (male/female): ")
    status = input("Your status(active/inactive): ")
    data = {
        "id": id,
        "name": name,
        "email": email,
        "gender": gender,
        "status": status
    }
    response_post = requests.post(url_user_resource, headers=headers, json=data, verify=False)

    return response_post.json()


def add_user_and_display_increased_total_users():
    url_users = create_url("users")
    response = requests.get(url_users, verify=False)
    data = response.json()
    total_users = 0
    for each_data in data:
        if each_data["id"] != 0:
            total_users += 1
    response_post = requests.post(url_users, headers=headers, json=data, verify=False)
    total_users += 1
    print(f"After post method we have {total_users}")
    print("--------------------")


def get_user_name_by_id(name):
    parameters = {'name': name}
    url_users = create_url("users")
    response = requests.get(url_users, headers=headers, params=parameters, verify=False)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]['id']
        else:
            print(f"No user have been found with name {name}")
            return None
    else:
        print(f"Error code : {response.status_code}")
        return None


def get_active_users(status):
    parameters = {'status': status}
    url_users = create_url("users")
    response = requests.get(url_users, headers=headers, params=parameters, verify=False)
    how_many_users = int(input("How many people you wanna display ? : "))
    if response.status_code == 200:
        data = response.json()
        nr_users = len(data)  # I used len(data) just to prevent the case there are
        # less than X people active/inactive
        if nr_users < 1:
            print("There are no users")
            print("\n--------------")
        else:
            if nr_users < how_many_users and status == "active":
                print(f"There are only {nr_users} active users ")
            elif nr_users < how_many_users and status == "inactive":
                print(f"There are only {nr_users} inactive users")
            elif nr_users > how_many_users and status == "active":
                print(f"Those {how_many_users} people active are :")
            elif nr_users > how_many_users and status == "inactive":
                print(f"Those {how_many_users} inactive people are :")

            for user in data[:how_many_users]:
                print(user['name'])
            print("\n-------------")
    else:
        print(f"Error code: {response.status_code}")


def first_X_ppl_with_middle_name():
    url_users = create_url("users")
    response = requests.get(url_users, headers=headers, verify=False)
    how_many_users = int(input("How many users you want :"))
    if response.status_code == 200:
        data = response.json()
        ok = 0
        for user in data:
            if how_many_users >= 1:
                if len(user['name'].split()) >= 3:  # true means that I have middle name
                    print(user['name'])
                    how_many_users -= 1
                    ok = 1
        if ok == 0:
            print("No one have middle name")


def show_all_users():
    """

    :return: display all users from endpoint
    """
    url_users = create_url("users")
    response = requests.get(url_users, verify=False)
    data = response.json()
    return [user_data['name'] for user_data in data]


def get_user_id_by_name(username):
    """

    :param username: User name from /users endpoint
    :return: user's id
    """
    url_users = create_url("users")
    parameters = {'name': username}
    response = requests.get(url_users, verify=False, params=parameters)

    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]['id']
        else:
            print("User not found")
            return None
    else:
        print(f"Error code status : {response.status_code}" )
        return None


def create_post(user_id):
    url = create_url("posts")
    print("\nCreate a post :\n")
    post_id = int(input("ID : "))
    title = input("Title : ")
    body = input("Body : ")
    load = {
        'id': post_id,
        'user_id': user_id,
        'title': title,
        'body': body
    }
    response = requests.post(url, json=load, headers=headers, verify=False)
    return response.json()


def create_comment(post_id, user_name):
    url = "https://gorest.co.in/public/v2/comments"
    print("\nCreate a comment :\n")
    comment_id = int(input("ID : "))
    email = input("Email : ")
    body = input("Body : ")
    load = {
        'id': comment_id,
        'post_id': post_id,
        'name': user_name,
        'email': email,
        'body': body
    }
    response = requests.post(url, verify=False, json=load, headers=headers)
    return response.json()


def create_todo(user_id):
    url = create_url("todos")
    print("\nCreate a todo :\n")
    todo_id = int(input("ID : "))
    todo_title = input("Title : ")
    due_on = input("Due : ")
    status = input("Status (pending/completed) : ")
    load = {
        'id': todo_id,
        'user_id': user_id,
        'title': todo_title,
        'due_on': due_on,
        'status': status
    }
    response = requests.post(url, verify=False, json=load, headers=headers)
    return response.json()


token_access = "Bearer ee493b8012fc048bbdd4c6de16e3c963aac76bb42a36430fd990cdc9b049c138"
BASE_URL = "https://gorest.co.in/public/v2/"
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
    print("\n\n1.Create a GET request for each endpoint available (users/posts/comments/todos)\n"
          "2.Create new user with your desired information, display the information of the new user\n"
          "3.Create a method to verify that after adding the new user, the total number of users has increased by 1\n"
          "4.Create a method that will bring a specified user name by adding a query parameter and use it to retain "
          "the user ID \n"
          "5.Display first active users\n"
          "6.Display first users that also have a middle name\n"
          "7.For the previously added user, create a post, a comment and a ttodo.\n")
    input_user = int(input("Type problem's number between 1 and 7 (0 to quit): "))
    if input_user == 0:
        break
    elif input_user == 1:
        #  Create a GET request for each endpoint available (users/posts/comments/todos),
        #  and modify the result in order to have a friendly format
        get_info_from_all_endpoints()
    elif input_user == 2:
        #  Create new user with your desired information, display the information of the new user
        new_user = create_new_user_and_display()
        print(f"The new user is : {new_user}")
    elif input_user == 3:
        # Create a method to verify that after adding the new user, the total number of users has increased by 1
        add_user_and_display_increased_total_users()
    elif input_user == 4:
        # Create a method that will bring a specified user name by adding a query parameter and use it to retain the
        # user ID
        name = input("Name: ")
        print(f"User {name} have id {get_user_name_by_id(name)}")
    elif input_user == 5:
        # Display first X  users depending their status
        type_status = input("Choose type of users (active/inactive): ")
        get_active_users(type_status)
    elif input_user == 6:
        # Display first X users that also have a middle name
        first_X_ppl_with_middle_name()
    elif input_user == 7:
        # For the previously added user, create a post, a comment and a ttodo.
        # Make sure the methods created at this point to be available for any other user
        print(show_all_users())  # First I should list all the users from endpoint /users
        user_name = input("Choose a name :")
        user_id = get_user_id_by_name(user_name)

        new_user_post = create_post(user_id)
        print(f"The post contains next info: {new_user_post}")  # I create a new post for chosen user

        new_user_comment = create_comment(post_id=new_user_post["id"], user_name=user_name)
        print(f"The comment contains next info: {new_user_comment}")  # I create a new comment for that new post

        new_user_todo = create_todo(user_id=user_id)
        print(f"The todo task contains next info: {new_user_todo}")

import requests
import json

url = "https://jsonplaceholder.typicode.com/posts"

def list_posts():
    response = requests.get(url)

    if response.status_code == 200:
        for i, data in enumerate(response.json()):
            print(f'================[{i}]================')
            print(f'userId : {data["userId"]}')
            print(f'id     : {data["id"]}')
            print(f'title  : {data["title"]}')
            print(f'body   : {data["body"]}')
        print("\n")
        return
    else:
        raise Exception(f'GET request to server failed : {response.status_code}')

def create_post(new_post):    
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=new_post)

    if response.status_code == 201:
        return response.json()
    else:
        raise Exception(f'POST request to server failed : {response.status_code}')

def update_post(post_id, new_post):
    headers = {"Content-Type": "application/json"}
    response = requests.put(f'{url}/{post_id}', headers=headers, data=new_post)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'PUT request to server failed : {response.status_code}')

def delete_post(post_id):
    response = requests.delete(f'{url}/{post_id}')

    if (response.status_code == 200) or (response.status_code == 204):
        return response.json()
    else:
        raise Exception(f'DELETE request to server failed : {response.status_code}')

def main():
    while True:
        print(
            "\n################# TOP MENU #################\n"
            "1. list existing post\n"
            "2. create new post\n"
            "3. update whole post\n"
            "4. delete specific post\n"
        )
        userSelect = input("Select number to perform : ").strip()
        print("______________________")

        if userSelect == "1":
            try:
                list_posts()
            except Exception as e:
                print(e)
            continue
        elif userSelect == "2":
            new_data = {}
            new_data["title"] = input("Specity the title : \n >>> ")
            new_data["body"] = input("Specity the body : \n >>> ")
            new_data_json = json.dumps(new_data)
            try:
                ret = create_post(new_data_json)
                print(f'Success : {ret}')
            except Exception as e:
                print(e)
            continue
        elif userSelect == "3":
            post_id = input("Specity the ID to update : \n >>> ")
            new_data = {}
            new_data["title"] = input("Specity the title : \n >>> ")
            new_data["body"] = input("Specity the body : \n >>> ")
            new_data_json = json.dumps(new_data)
            try:
                ret = update_post(post_id, new_data_json)
                print(f'Success : {ret}')
            except Exception as e:
                print(e)
            continue
        elif userSelect == "4":
            post_id = input("Specity the ID to update : \n >>> ")
            try:
                ret = delete_post(post_id)
                print(f'Success : {ret}')
            except Exception as e:
                print(e)
            continue
        else:
            print("Invalid input...")
    return

if __name__ == "__main__":
    main()
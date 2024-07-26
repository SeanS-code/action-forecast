import requests

def get_posts():
    url = "http://127.0.0.1:8000/bye"

    try:
        res = requests.get(url)
        if res.status_code == 200:
            posts = res.json()
            return posts
        else:
            print('Error: ', res.status_code)
            return none
    except requests.exceptions.RequestException as e:
        print('Error: ', e)
        return none

def main():
    print(get_posts())

if __name__ == '__main__':
    main()
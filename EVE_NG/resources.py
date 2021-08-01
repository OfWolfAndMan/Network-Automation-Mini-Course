import requests


def get_response_code(r):
    if "40" in str(r.status_code):
        raise Exception(r.json())
    elif "50" in str(r.status_code):
        raise Exception(r.json())
    elif "30" in str(r.status_code):
        raise Exception(r.json())
    elif "20" not in str(r.status_code):
        raise Exception(
            f"An error occurred! The error was {r.status_code}: {r.json().get('message')}"
        )


def connect_to_api(
    method, uri, headers=None, auth=None, data=None, json=None, cookies=None
):
    methods = ["GET", "PUT", "PATCH", "DELETE", "POST"]
    if method not in methods:
        raise ValueError("Not a valid HTTP method!")
    r = requests.request(
        method, uri, headers=headers, auth=auth, data=data, json=json, cookies=cookies
    )
    get_response_code(r)
    return r

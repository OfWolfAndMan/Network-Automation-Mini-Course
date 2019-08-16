import requests
from netmiko import ConnectHandler
import os
# import pytest

####################################################################
# Environment variables required to be set prior to running this
# EVE_HOST      The hostname of the EVE-NG instance
####################################################################

headers = {
        'Content-Type': "application/json",
        'Accept': "*/*",
        'cache-control': "no-cache"
}

def test_login():

    data = '{"username":"admin","password":"eve","html5":-1}'

    r = requests.post(f'http://{EVE_HOST}/api/auth/login', data=data)
    cookies = r.cookies.get_dict()
    if r.status_code == 200:
        print("Logged in...")
    else:
        print("An error occurred logging in", r.json())
    return cookies

def test_create_lab(cookies, headers):
    data = '''{
    "path": "/",
    "name":"Mock Lab 2",
    "version":"1",
    "author":"Bob",
    "description":"A demo lab",
    "body":"Lab usage and guide"
    }'''

    r = requests.post('http://{EVE_HOST}/api/labs', cookies=cookies, data=data, headers=headers)
    if r.status_code == 200:
        print("Lab has been created")
    elif r.status_code == 412:
        print("User is not authenticated or session timed out.")
    else:
        print("An error occurred creating the lab")

def test_get_lab(cookies):
    rthird = requests.get(f'http://{EVE_HOST}/api/labs/Mock%20Lab%202.unl', cookies=cookies)
    print("Getting lab...")
    # print(rthird.json())
    # return rthird

def test_delete_lab(cookies):
    rthird = requests.delete(f'http://{EVE_HOST}/api/labs/Mock%20Lab%202.unl', cookies=cookies)
    if rthird.status_code == 404:
        print("Lab already deleted")
    else:
        print("Lab has been deleted")

def test_logout(cookies, headers):
    r = requests.delete(f'http://{EVE_HOST}/api/auth/logout', cookies=cookies, headers=headers)
    print("Logging out")


def test_get_nodes(cookies, headers):
    r = requests.get(f'http://{EVE_HOST}/api/labs/Mock%20Lab%202.unl/nodes', headers=headers,
                             cookies=cookies)
    print("Phase: Get nodes: {}".format(r.json()))

def test_add_config(cookies, headers):

    url = f"http://{EVE_HOST}/api/labs/Mock%20Lab%202.unl/configs/1"

    payload = "{\n\t\"data\": \"aaa new-model\\ninterface eth0/0\\n ip address dhcp\\n no shut\\n line vty 0 4\\n transport input ssh\"\n}"

    r = requests.request("PUT", url, data=payload, headers=headers, cookies=cookies)
    print(("Phase: Adding config: {}".format(r.text, r.status_code)))

    url = f"http://{EVE_HOST}/api/labs/Mock%20Lab%202.unl/nodes/1"

    payload = "{\n\t\"config\": 1\n}"

    rtwo = requests.request("PUT", url, data=payload, headers=headers, cookies=cookies)
    print("Phase: Set config flag: {}".format(rtwo.json()))


def test_start_nodes(cookies, headers):
    url = f"http://{EVE_HOST}/api/labs/Mock%20Lab.unl/nodes/start"

    r = requests.request("GET", url, headers=headers, cookies=cookies)

    print("Phase: Start nodes: {}".format(r.json()))

cookies = test_login()
test_create_lab(cookies, headers)
test_get_lab(cookies)
test_add_config(cookies, headers)
test_start_nodes(cookies, headers)
test_logout(cookies, headers)

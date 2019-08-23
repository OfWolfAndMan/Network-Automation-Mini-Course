import requests
import os
import pytest

####################################################################
# Environment variables required to be set prior to running this
# EVE_HOST      The hostname of the EVE_NG instance
# EVE_PASS      The password of the CLI login
####################################################################

headers = {
    "Content-Type": "application/json",
    "Accept": "*/*",
    "cache-control": "no-cache",
}
EVE_HOST = os.getenv("EVE_HOST", "192.168.170.129")
api_hostname = f"{EVE_HOST}"
EVE_PASS = os.getenv("EVE_PASS", "eve")
ProjectName = "Lab Sample A"
PreviousFailed = False


@pytest.fixture()
def test_login():
    data = {"username": "admin", "password": "eve", "html5": -1}
    r = requests.post(f"http://{EVE_HOST}/api/auth/login", json=data, timeout=1)
    cookies = r.cookies.get_dict()
    return cookies


def test_create_lab(test_login):
    cookies = test_login
    # if type(cookies) != dict():
    #     PreviousFailed = True
    # if PreviousFailed:
    #     pytest.xfail("Previous test failed. Skipping...")
    # else:
    data = {
        "path": "/",
        "name": "{}".format(ProjectName),
        "version": "1",
        "author": "Anthony",
        "description": "A demo lab",
        "body": "Lab usage and guide",
    }

    r = requests.request(
        "POST",
        f"http://{EVE_HOST}/api/labs",
        cookies=cookies,
        json=data,
        headers=headers,
    )
    assert r.status_code == 200, "Response code should be 200"


def test_get_lab(test_login):
    cookies = test_login
    assert cookies != None
    r = requests.request(
        "GET", f"http://{EVE_HOST}/api/labs/{ProjectName}.unl", cookies=cookies
    )
    assert r.status_code == 200, "Response code should be 200"


def test_create_node(test_login):
    cookies = test_login
    assert cookies != None
    data = {
        "console": "telnet",
        "delay": 0,
        "left": 774,
        "icon": "Router.png",
        "image": "vios-adventerprisek9-m.SPA.156-2.T",
        "name": "vIOS",
        "ram": 512,
        "status": 0,
        "template": "vios",
        "type": "qemu",
        "top": 180,
        "config": 0,
        "cpu": 1,
        "ethernet": 4,
    }
    r = requests.request(
        "POST",
        f"http://{EVE_HOST}/api/labs/{ProjectName}.unl/nodes",
        headers=headers,
        cookies=cookies,
        json=data,
    )
    assert r.status_code == 201, "Response code should be 201"


def test_get_nodes(test_login):
    cookies = test_login
    assert cookies != None
    r = requests.request(
        "GET",
        f"http://{EVE_HOST}/api/labs/{ProjectName}.unl/nodes",
        headers=headers,
        cookies=cookies,
    )
    assert r.status_code == 200, "Response code should be 200"


def test_create_net(test_login):
    cookies = test_login
    assert cookies != None
    defaults = {
        "count": 0,
        "left": 588,
        "name": "Net",
        "top": 36,
        "type": "pnet0",
        "visibility": 1,
    }
    r = requests.request(
        "POST",
        f"http://{EVE_HOST}/api/labs/{ProjectName}.unl/networks",
        headers=headers,
        cookies=cookies,
        json=defaults,
    )
    assert r.status_code == 201, "Response code should be 201"


def test_get_net(test_login):
    cookies = test_login
    assert cookies != None
    r = requests.request(
        "GET",
        f"http://{EVE_HOST}/api/labs/{ProjectName}.unl/networks",
        headers=headers,
        cookies=cookies,
    )
    assert r.status_code == 200, "Response code should be 200"


def test_connect_intf(test_login):
    cookies = test_login
    assert cookies != None
    data = {"0": "1"}
    r = requests.request(
        "PUT",
        f"http://{EVE_HOST}/api/labs/{ProjectName}.unl/nodes/1/interfaces",
        headers=headers,
        cookies=cookies,
        json=data,
    )
    assert r.status_code == 201, "Response code should be 201"


def test_start_nodes(test_login):
    cookies = test_login
    assert cookies != None
    url = f"http://{EVE_HOST}/api/labs/{ProjectName}.unl/nodes/start"

    r = requests.request("GET", url, headers=headers, cookies=cookies)

    assert r.status_code == 200, "Response code should be 200"


def test_stop_nodes(test_login):
    cookies = test_login
    assert cookies != None
    url = f"http://{EVE_HOST}/api/labs/{ProjectName}.unl/nodes/stop"

    r = requests.request("GET", url, headers=headers, cookies=cookies)

    assert r.status_code == 200, "Response code should be 200"


def test_delete_net(test_login):
    cookies = test_login
    assert cookies != None
    r = requests.request(
        "DELETE",
        f"http://{EVE_HOST}/api/labs/{ProjectName}.unl/networks/1",
        headers=headers,
        cookies=cookies,
    )
    assert r.status_code == 200, "Response code should be 200"


def test_delete_node(test_login):
    cookies = test_login
    assert cookies != None
    r = requests.request(
        "DELETE",
        f"http://{EVE_HOST}/api/labs/{ProjectName}.unl/nodes/1",
        headers=headers,
        cookies=cookies,
    )
    assert r.status_code == 200, "Response code should be 200"


def test_delete_lab(test_login):
    cookies = test_login
    assert cookies != None
    r = requests.request(
        "DELETE", f"http://{EVE_HOST}/api/labs/{ProjectName}.unl", cookies=cookies
    )
    assert r.status_code == 200, "Response code should be 200"


def test_logout(test_login):
    cookies = test_login
    r = requests.request(
        "GET", f"http://{EVE_HOST}/api/auth/logout", cookies=cookies, headers=headers
    )
    assert r.status_code == 200, "Response code should be 200"


# @pytest.mark.xfail(raises=Error)

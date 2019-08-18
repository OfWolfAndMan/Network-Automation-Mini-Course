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
EVE_HOST = os.getenv("EVE_HOST", "192.168.100.193")
api_hostname = f"{EVE_HOST}"
EVE_PASS = os.getenv("EVE_PASS", "eve")
ProjectName = "Lab Sample A"


@pytest.fixture()
def test_login():
    data = {"username": "admin", "password": "eve", "html5": -1}
    r = requests.post(f"http://{EVE_HOST}/api/auth/login", json=data)
    cookies = r.cookies.get_dict()
    assert r.status_code == 200
    assert cookies
    return cookies


def test_create_lab(test_login):
    cookies = test_login
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
    assert r.status_code == 200


def test_get_lab(test_login):
    cookies = test_login
    r = requests.request(
        "GET", f"http://{EVE_HOST}/api/labs/{ProjectName}.unl", cookies=cookies
    )
    assert r.status_code == 200


def test_create_node(test_login):
    cookies = test_login
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
    assert r.status_code == 201


def test_get_nodes(test_login):
    cookies = test_login
    r = requests.request(
        "GET",
        f"http://{EVE_HOST}/api/labs/{ProjectName}.unl/nodes",
        headers=headers,
        cookies=cookies,
    )
    assert r.status_code == 200


def test_create_net(test_login):
    cookies = test_login
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
    assert r.status_code == 201


def test_delete_net(test_login):
    cookies = test_login
    r = requests.request(
        "DELETE",
        f"http://{EVE_HOST}/api/labs/{ProjectName}.unl/networks/1",
        headers=headers,
        cookies=cookies,
    )
    assert r.status_code == 200


def test_stop_nodes(test_login):
    cookies = test_login
    url = f"http://{EVE_HOST}/api/labs/{ProjectName}.unl/nodes/stop"

    r = requests.request("GET", url, headers=headers, cookies=cookies)

    assert r.status_code == 200


def test_delete_node(test_login):
    cookies = test_login
    r = requests.request(
        "DELETE",
        f"http://{EVE_HOST}/api/labs/{ProjectName}.unl/nodes/1",
        headers=headers,
        cookies=cookies,
    )
    assert r.status_code == 200


def test_delete_lab(test_login):
    cookies = test_login
    r = requests.request(
        "DELETE", f"http://{EVE_HOST}/api/labs/{ProjectName}.unl", cookies=cookies
    )
    assert r.status_code == 200


def test_logout(test_login):
    cookies = test_login
    r = requests.request(
        "GET", f"http://{EVE_HOST}/api/auth/logout", cookies=cookies, headers=headers
    )
    assert r.status_code == 200

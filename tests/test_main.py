import pytest


@pytest.fixture
def numbers():
    return [2, 3, 5, 6]


@pytest.fixture
def schema():
    return {"id": 123, "ip": "192.168.50.51", "port": 443, "type": "firewall"}


@pytest.fixture
def types():
    return ["firewall", "switch", "router", "vpn"]


def test_addition_pass(numbers: list):
    assert type(numbers) == list
    assert [type(x) == int for x in numbers]
    assert sum(numbers) <= 1000


@pytest.mark.xfail(raises=AssertionError)
def test_addition_fail(numbers: list):
    assert type(numbers) == list
    numbers.append(1000)
    assert [type(x) == int for x in numbers]
    assert sum(numbers) <= 1000


def test_api_schema_pass(schema, types):
    assert [x != None for x in schema.values()]
    assert len(schema) == 4
    assert type(schema["port"]) == int
    assert schema["type"] in types


@pytest.mark.xfail(raises=AssertionError)
def test_api_schema_fail(schema, types):
    assert [x != None for x in schema.values()]
    schema["NOS"] = "IOS"
    assert len(schema) == 4
    assert type(schema["port"]) == int
    assert schema["type"] in types

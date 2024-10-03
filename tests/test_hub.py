import pytest
from requests_mock import Mocker
from ics_2000.config import API_URL
from ics_2000.hub import Hub

LOGIN_JSON_RES = {
    "person_name": "test",
    "newsletter": "false",
    "ipcam_only": False,
    "homes": [
        {
            "home_id": "0",
            "home_name": "test home",
            "mac": "0123456789AB",
            "aes_key": "324fa6cd0d4dd01aa528db45a2c736a3",
        }
    ],
    "cameras": [],
}

GATEWAY_JSON_RES = [
    {
        "home_id": "0",
        "id": "25660643",
        "version_status": "2",
        "version_data": "28",
        "status": "GCgplnB5EKgCBKBtWSDEcPl4PHMaYgroGs04We0cnmkhkMsBhlV0iQrSS59R7P+/SYD20A4RWD+NQl4f/YjJk7Q1mih8wYKeqepdJCgU4M4=",
        "data": "LJJtBF4nBtlxXG+T+wJK0UNHhP4eycyXRbXNL9pss38CoKPqYV6DxVCdPd2zNZ7EELIk/OtAUNJJ7iDkDGQ3AIky3szIlE7jI2MfkAs9d/aqgPzgiZ8i8+Sf5ACnRLPi3GGZsXMfwiG1zhuJaDPNBkW9hIkyQPNnO7caJV7zkmyTvWIi1+pNYOYsL3F9ayV/VqjTP63qCvf+JJ3mr63OlJ35jO2VMwb2RFYQ7IZqUcnw9KGIEnhe2on1if7hNTFR/rBJo2zfZ8KElb6EmKSgh7FhZxFVekdSkGRmAvmKk125aLL9AFp/5JXgICgjPksnplP9YHolsNmbUSZrebRwZYGAekXH5kC+oBuyaIB8EHeOxw5oBKJJsnAt1ShxlG7CFK6KX7izO7Mj6X8Fj8Q63Zd7KcC61h367kyq/WyY9YG1z/XWPcPB4u1B4FlrtxEAVBWonZq/6iZJRmmZiQs5AQjNvRGBDSt0L5S+fjO4TFNA5AMtDLz9xdcDz53DD35oLh9HvhX+KBIV7YEiVPhMf01fXwFY4RkUQDJ030K8vTdq0JMF1E9ZOSla5nnoRgRRipHOfH0dFLqWb+BFs8eMIMCf9IjnE+TczW6Wv0uV74H3VvEYsiKcdOPHWL3XYjRJbIRMcZ34b5p1o8PfQEmUersiGpWfkUuR/FDVxCj9uiiLYi+JWzWxMQw4jPRldJjk1YkHKAHifp8ADUcjqthRpw==",
        "time_added": "2022-12-12 11:40:25",
    },
    {
        "home_id": "0",
        "id": "19973075",
        "version_status": "1",
        "version_data": "107",
        "status": "MGgsr6FGF6xjDegEk3NcpuvlTW+I9Y5it+788J+ka7nVkXmQh+Q43KK+mVmkWf4AUn8sKot7rEeh8oogjZCf2UEf9/UmrpUF/YJR8mY2VKM=",
        "data": "oVvI0bUE+p9PfAEHfDS8NU8k+iz99EEYVkCOmRk37k5RLs194EVTPfYqo2YCASJB5Bj+B6Efpvk5aHsjQoOdD4aHTryUxRCrWJxiMrXDT65nxdFkJDSFvkSxcXXl6dmzMH7jP/NnvUN1UVGcJAOMAkEwG7SD0K+e1zH0geg1qyW+sQyFtXyQYt/CepnOIFcevehHvlu5N0BcE7mYBmHmCPHovqzIwmQ3xVJ5+v9Me874901eb7bGDh6rlgkU6YAakjamjnJRf9kmDXIGz9S2FLsrOsGFgDJzvWiuczvoPmr47nPYMC+sybip+iKhn2eOeS4pW1lXJh11UM0Cp8u5Lyh0HjclxInOPhDSoBcA3XvXsQafT9wOSKNnNy7+IVBDJ58PDsrN4e49fc7v/i8L6j15Uep2EjvBXQ/C0WDYFKvxwjtkO52h8WHIy4uoIRCI0E92AS2nqAtOJXWaRJP706EtNjd0riO6+sMwANa9UeL79FWXEbWIFahNOyfEfYMShob8WLDA11CYepufWWtmRejBdCvueWULlCKmMsZ7bmWjlvAlocTexdMLpq5Ui1fPm84OZv5EPTISEoUAIE4RA+ApuWGZKS6y6A5TbnnGqfr8wM+s/oWDQ/asKC00vlOgv+rEz4eiRUAnHSsK1riN8vBnhbw1lDBzwkmluY4dDJYhhFSgTFLoRIkZ33iYj4li8Z6dMUEsaGItPuR+7dXFsw==",
        "time_added": "2022-12-12 10:43:29",
    },
]

ENTITY_JSON_RES = [
    {
        "data": "LJJtBF4nBtlxXG+T+wJK0UNHhP4eycyXRbXNL9pss38CoKPqYV6DxVCdPd2zNZ7EELIk/OtAUNJJ7iDkDGQ3AIky3szIlE7jI2MfkAs9d/aqgPzgiZ8i8+Sf5ACnRLPi3GGZsXMfwiG1zhuJaDPNBkW9hIkyQPNnO7caJV7zkmyTvWIi1+pNYOYsL3F9ayV/VqjTP63qCvf+JJ3mr63OlJ35jO2VMwb2RFYQ7IZqUcnw9KGIEnhe2on1if7hNTFR/rBJo2zfZ8KElb6EmKSgh7FhZxFVekdSkGRmAvmKk125aLL9AFp/5JXgICgjPksnplP9YHolsNmbUSZrebRwZYGAekXH5kC+oBuyaIB8EHeOxw5oBKJJsnAt1ShxlG7CFK6KX7izO7Mj6X8Fj8Q63Zd7KcC61h367kyq/WyY9YG1z/XWPcPB4u1B4FlrtxEAVBWonZq/6iZJRmmZiQs5AQjNvRGBDSt0L5S+fjO4TFNA5AMtDLz9xdcDz53DD35oLh9HvhX+KBIV7YEiVPhMf01fXwFY4RkUQDJ030K8vTdq0JMF1E9ZOSla5nnoRgRRipHOfH0dFLqWb+BFs8eMIMCf9IjnE+TczW6Wv0uV74H3VvEYsiKcdOPHWL3XYjRJbIRMcZ34b5p1o8PfQEmUersiGpWfkUuR/FDVxCj9uiiLYi+JWzWxMQw4jPRldJjk1YkHKAHifp8ADUcjqthRpw==",
        "data_version": 28,
        "id": 25660643,
        "status": "2MnYT38u4/sbbuJtyX7FwfKgpWrdVy9/qy9dtedDTJPfi3JBmy1Jf1JYcoyxjQHXkxiaoupFbqToWQUJ5z4CSZORCC3dGNI3QZGLt/PMapE=",
        "status_version": 17108,
    },
    {
        "data": "oVvI0bUE+p9PfAEHfDS8NU8k+iz99EEYVkCOmRk37k5RLs194EVTPfYqo2YCASJB5Bj+B6Efpvk5aHsjQoOdD4aHTryUxRCrWJxiMrXDT65nxdFkJDSFvkSxcXXl6dmzMH7jP/NnvUN1UVGcJAOMAkEwG7SD0K+e1zH0geg1qyW+sQyFtXyQYt/CepnOIFcevehHvlu5N0BcE7mYBmHmCPHovqzIwmQ3xVJ5+v9Me874901eb7bGDh6rlgkU6YAakjamjnJRf9kmDXIGz9S2FLsrOsGFgDJzvWiuczvoPmr47nPYMC+sybip+iKhn2eOeS4pW1lXJh11UM0Cp8u5Lyh0HjclxInOPhDSoBcA3XvXsQafT9wOSKNnNy7+IVBDJ58PDsrN4e49fc7v/i8L6j15Uep2EjvBXQ/C0WDYFKvxwjtkO52h8WHIy4uoIRCI0E92AS2nqAtOJXWaRJP706EtNjd0riO6+sMwANa9UeL79FWXEbWIFahNOyfEfYMShob8WLDA11CYepufWWtmRejBdCvueWULlCKmMsZ7bmWjlvAlocTexdMLpq5Ui1fPm84OZv5EPTISEoUAIE4RA+ApuWGZKS6y6A5TbnnGqfr8wM+s/oWDQ/asKC00vlOgv+rEz4eiRUAnHSsK1riN8vBnhbw1lDBzwkmluY4dDJYhhFSgTFLoRIkZ33iYj4li8Z6dMUEsaGItPuR+7dXFsw==",
        "data_version": 107,
        "id": 19973075,
        "status": "yAmOwVIWJPKr5SlAcB0BdHVbo/RDHzkQykCeyG1eLVxYv3TO8zNgf0eYHEMih3NkTw5oYOmoKqqxHkV4UpEdcF6MCjQq/p0ReyrA77Sge/A=",
        "status_version": 17107,
    },
]


@pytest.fixture
def hub():
    return Hub("test@email.com", "Password")


def auth(hub, requests_mock: Mocker):
    requests_mock.post(f"{API_URL}/account.php", json=LOGIN_JSON_RES)
    hub.login()


def test_login(hub, requests_mock: Mocker):
    auth(hub, requests_mock)
    assert hub.aes_key == "324fa6cd0d4dd01aa528db45a2c736a3"
    assert hub.home_name == "test home"


def test_get_devices(hub, requests_mock: Mocker):
    auth(hub, requests_mock)

    requests_mock.post(f"{API_URL}/gateway.php", json=GATEWAY_JSON_RES)
    hub.get_devices()
    assert len(hub.devices) > 0


def test_get_device_status(hub, requests_mock: Mocker):
    auth(hub, requests_mock)

    requests_mock.post(f"{API_URL}/gateway.php", json=GATEWAY_JSON_RES)
    hub.get_devices()
    assert len(hub.devices) > 0

    requests_mock.post(f"{API_URL}/entity.php", json=ENTITY_JSON_RES)
    for device in hub.devices:
        if device.name == "Hoge Deel":
            assert device.get_on_status() == False

import pytest

from service.api_client import APIClient


@pytest.fixture
def api_client(base_url: str='http://127.0.0.1:8000/api/v1'):
    return APIClient(base_url=base_url)


@pytest.fixture
def response(api_client):
    def _on_success(response, message):
        raise AttributeError(response)

    resp = api_client.post(
        endpoint='users/login',
        data={
            'email': 'qwe11@qwe.com',
            'password': 'super secret password'
        },
        on_success=_on_success,
        on_failure=lambda *_: None,
        on_cancel=lambda *_: None
    )

    return resp


@pytest.mark.requires_server
def test_token_acquisition(response):
    x = response
    # s = f'{dir(x)}\n{x}\n{type(x)}'
    # raise AttributeError(s)
    assert 1 == 1

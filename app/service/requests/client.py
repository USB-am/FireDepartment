from __future__ import annotations
from typing import Any, Callable, TYPE_CHECKING


if TYPE_CHECKING:
    class UrlRequest:
        def __init__(self, *args, **kwargs):
            ...
else:
    from kivy.network.urlrequest import UrlRequest


TKivyCallback = Callable[[UrlRequest, Any], None]


class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self._token: str | None = None

    def set_token(self, token: str) -> None:
        self._token = token

    def clear_token(self) -> None:
        self._token = None

    def _build_headers(self, use_auth: bool, extra_headers: dict[str, str] | None=None) -> dict[str, str]:
        headers = {'Content-Type': 'application/json'}

        if extra_headers:
            headers.update(extra_headers)

        if use_auth and self._token:
            headers['Authorization'] = self._token

        return headers

    def request(
        self,
        method: str,
        endpoint: str,
        on_success: TKivyCallback,
        on_failure: TKivyCallback | None = None,
        on_redirect: TKivyCallback | None = None,
        on_cancel: TKivyCallback | None = None,
        on_error: TKivyCallback | None = None,
        data: dict | None = None,
        params: dict | None = None,
        use_auth: bool = True,
        extra_headers: dict[str, str] | None = None,
        timeout: int = 10
    ) -> UrlRequest:

        url = f'{self.base_url}/{endpoint.lstrip("/")}'

        if params:
            from urllib.parse import urlencode
            url = f'{url}?{urlencode(params)}'

        headers = self._build_headers(use_auth, extra_headers)

        req_body = None
        if data:
            import json
            req_body = json.dumps(data)

        req = UrlRequest(
            url=url,
            req_body=req_body,
            req_headers=headers,
            method=method.upper(),
            on_success=on_success,
            on_failure=on_failure or self._default_failure,
            on_redirect=on_redirect or self._default_redirect,
            on_cancel=on_cancel or self._default_cancel,
            on_error=on_error or self._default_error,
            timeout=timeout,
            decode=True
        )
        return req

    @staticmethod
    def _default_failure(req: 'UrlRequest', error: Any):
        print(f'Request failed: {error}')

    @staticmethod
    def _default_redirect(req: 'UrlRequest', error: Any):
        print(f'Request redirected: {error}')

    @staticmethod
    def _default_cancel(req: 'UrlRequest', error: Any):
        print(f'Request cancel: {error}')

    @staticmethod
    def _default_error(req: 'UrlRequest', error: Any):
        print(f'Request error: {error}')

    def post(self, endpoint: str, data: dict[str, Any], on_success: TKivyCallback, on_failure: TKivyCallback | None=None, **kwargs):
        return self.request('POST', endpoint, on_success, on_failure, data=data, **kwargs)

    def get(self, endpoint: str, on_success: TKivyCallback, on_failure: TKivyCallback | None=None, **kwargs):
        return self.request('GET', endpoint, on_success, on_failure, **kwargs)

    def put(self, endpoint: str, data: dict[str, Any], on_success: TKivyCallback, on_failure: TKivyCallback | None=None, **kwargs):
        return self.request('PUT', endpoint, on_success, on_failure, data=data, **kwargs)

    def delete(self, endpoint: str, on_success: TKivyCallback, on_failure: TKivyCallback | None=None, **kwargs):
        return self.request('DELETE', endpoint, on_success, on_failure, **kwargs)

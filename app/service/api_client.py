from typing import Optional, Dict

import requests


class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self._token = None
        self._session = requests.Session()

    def set_token(self, token: str) -> None:
        self._token = token

    def clear_token(self) -> None:
        self._token = None

    def _build_headers(self, use_auth: bool, extra_headers: Optional[Dict[str, str]]=None) -> Dict[str, str]:
        headers = {'Content-Type': 'application/json'}

        if extra_headers:
            headers.update(extra_headers)

        if use_auth and self._token:
            headers['Authorization'] = self._token

        return headers

    def request(self,
                method: str,
                endpoint: str,
                data: Optional[Dict]=None,
                json: Optional[Dict]=None,
                params: Optional[Dict]=None,
                use_auth: bool=True,
                extra_headers: Optional[Dict[str, str]]=None,
                timeout: int=10
    ) -> requests.Response:
        url = f'{self.base_url}/{endpoint.lstrip("/")}/'
        headers = self._build_headers(use_auth, extra_headers)

        response = self._session.request(
            method=method.upper(),
            url=url,
            headers=headers,
            data=data,
            json=json,
            params=params,
            timeout=timeout)
        response.raise_for_status()

        return response

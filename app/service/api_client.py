from typing import Any, Optional, Dict, Callable
from urllib.parse import urlencode
import json
from http.cookies import SimpleCookie
from kivy.network.urlrequest import UrlRequest


class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self._token = None          # для обратной совместимости (Bearer)
        self._cookies = {}          # хранилище cookie {name: value}

    def set_token(self, token: str) -> None:
        """Установить Bearer-токен (если нужен)."""
        self._token = token

    def clear_token(self) -> None:
        self._token = None

    def set_cookie(self, name: str, value: str) -> None:
        """Установить отдельную cookie вручную."""
        self._cookies[name] = value

    def clear_cookies(self) -> None:
        self._cookies.clear()

    def _update_cookies_from_response(self, req: UrlRequest) -> None:
        headers = getattr(req, 'resp_headers', {})
        if not headers:
            # return
            x = headers
            s = f'{dir(x)}\n{x}\n{type(x)}'
            raise AttributeError(s)

        # Ищем заголовок Set-Cookie независимо от регистра
        set_cookie_value = None
        for key, value in headers.items():
            if key.lower() == 'set-cookie':
                set_cookie_value = value
                break

        if set_cookie_value is None:
            return

        # Если значение – строка, превращаем в список
        if isinstance(set_cookie_value, str):
            set_cookie_values = [set_cookie_value]
        else:
            set_cookie_values = set_cookie_value

        for cookie_header in set_cookie_values:
            try:
                cookie = SimpleCookie()
                cookie.load(cookie_header)
                for key, morsel in cookie.items():
                    self._cookies[key] = morsel.value
            except Exception as e:
                print(f'Ошибка парсинга Cookie: {e}')

    def _build_headers(self, use_auth: bool, extra_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        headers = {'Content-Type': 'application/json'}

        if extra_headers:
            headers.update(extra_headers)

        # Добавляем Bearer-токен, если он есть и требуется
        if use_auth and self._token:
            headers['Authorization'] = self._token

        # Добавляем Cookie, если они есть
        if self._cookies:
            cookie_str = '; '.join(f'{k}={v}' for k, v in self._cookies.items())
            headers['Cookie'] = cookie_str

        return headers

    def request(
        self,
        method: str,
        endpoint: str,
        on_success: Callable[[UrlRequest, Any], None],
        on_failure: Optional[Callable[[UrlRequest, Any], None]] = None,
        on_redirect: Optional[Callable[[UrlRequest, Any], None]] = None,
        on_cancel: Optional[Callable[[UrlRequest, Any], None]] = None,
        on_error: Optional[Callable[[UrlRequest, Any], None]] = None,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        use_auth: bool = True,
        extra_headers: Optional[Dict[str, str]] = None,
        timeout: int = 10
    ) -> UrlRequest:

        url = f'{self.base_url}/{endpoint.lstrip("/")}'
        if params:
            url = f'{url}?{urlencode(params)}'

        headers = self._build_headers(use_auth, extra_headers)

        req_body = json.dumps(data) if data else None

        # Оборачиваем колбэки, чтобы обновлять cookies из ответа
        def wrap_callback(cb):
            if cb is None:
                return None
            def wrapper(req, result):
                self._update_cookies_from_response(req)
                cb(req, result)
            return wrapper

        req = UrlRequest(
            url=url,
            req_body=req_body,
            req_headers=headers,
            method=method.upper(),
            on_success=wrap_callback(on_success),
            on_failure=wrap_callback(on_failure or self._default_failure),
            on_redirect=wrap_callback(on_redirect or self._default_redirect),
            on_cancel=on_cancel or self._default_cancel,   # для cancel ответа нет
            on_error=wrap_callback(on_error or self._default_error),
            timeout=timeout,
            decode=True
        )
        return req

    # Статические методы по умолчанию оставляем без изменений
    @staticmethod
    def _default_failure(req: UrlRequest, error: Any):
        print(f'Request failed: {error}')

    @staticmethod
    def _default_redirect(req: UrlRequest, error: Any):
        print(f'Request redirected: {error}')

    @staticmethod
    def _default_cancel(req: UrlRequest, error: Any):
        print(f'Request cancel: {error}')

    @staticmethod
    def _default_error(req: UrlRequest, error: Any):
        print(f'Request error: {error}')

    # Удобные методы-обёртки
    def post(self, endpoint: str, data: Dict, on_success: Callable, on_failure: Optional[Callable] = None, **kwargs):
        return self.request('POST', endpoint, on_success, on_failure, data=data, **kwargs)

    def get(self, endpoint: str, on_success: Callable, on_failure: Optional[Callable] = None, **kwargs):
        return self.request('GET', endpoint, on_success, on_failure, **kwargs)

    def put(self, endpoint: str, data: Dict, on_success: Callable, on_failure: Optional[Callable] = None, **kwargs):
        return self.request('PUT', endpoint, on_success, on_failure, data=data, **kwargs)

    def delete(self, endpoint: str, on_success: Callable, on_failure: Optional[Callable] = None, **kwargs):
        return self.request('DELETE', endpoint, on_success, on_failure, **kwargs)

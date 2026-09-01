from typing import Callable, Any, TYPE_CHECKING


if TYPE_CHECKING:
    from kivy.network.urlrequest import UrlRequest


TKivyCallback = Callable[['UrlRequest', Any], None]

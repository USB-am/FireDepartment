from typing import Callable, Any, TYPE_CHECKING


if TYPE_CHECKING:
    from kivy.network.urlrequest import UrlRequestUrllib


TKivyCallback = Callable[['UrlRequestUrllib', Any], None]

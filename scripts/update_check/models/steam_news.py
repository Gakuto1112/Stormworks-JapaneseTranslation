from dataclasses import dataclass

from .steam_app_news import SteamAppNews


@dataclass(frozen=True, slots=True)
class SteamNews:
	"""
	Steamからニュースをフェッチする際のレスポンスのデータモデル。
	"""

	appnews: SteamAppNews
	"""
	特定のアプリ（ゲーム）に関するニュース。
	"""

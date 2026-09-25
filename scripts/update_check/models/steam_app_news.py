from dataclasses import dataclass

from .steam_news_entry import SteamNewsEntry


@dataclass(frozen=True, slots=True)
class SteamAppNews:
	"""
	Steamからニュースをフェッチする際のレスポンスのデータモデル。
	特定のアプリ（ゲーム）に関するニュースのデータモデル。
	"""

	appid: int
	"""
	アプリ（ゲーム）のID。
	"""

	newsitems: list[SteamNewsEntry]
	"""
	ニュースのエントリーのリスト。
	"""

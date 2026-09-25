from dataclasses import dataclass
from typing import Self

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

	@classmethod
	def from_dict(cls, news_dict: dict) -> Self:
		"""
		辞書型のニュースレスポンスからSteamNewsクラスのインスタンスを生成する。

		Args:
			news_dict (dict): Steamニュースの辞書型レスポンス。

		Returns:
			Self: 生成されたSteamNewsのインスタンス。

		Raises:
			TypeError: 辞書型の構造が正しくない場合
		"""

		appnews_dict = news_dict.get("appnews")
		if not isinstance(appnews_dict, dict):
			raise TypeError("Invalid type for \"appnews\": expected dict")

		appnews = SteamAppNews.from_dict(appnews_dict)

		return cls(
			appnews=appnews
		)

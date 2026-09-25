from dataclasses import dataclass
from typing import Self

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

	@classmethod
	def from_dict(cls, app_news_dict: dict) -> Self:
		"""
		辞書型のアプリニュースからSteamAppNewsクラスのインスタンスを生成する。

		Args:
			app_news_dict (dict): Steamアプリニュースの辞書型レスポンス。

		Returns:
			Self: 生成されたSteamAppNewsのインスタンス。

		Raises:
			TypeError: 辞書型の構造が正しくない場合
		"""

		appid = app_news_dict.get("appid")
		if not isinstance(appid, int):
			raise TypeError("Invalid type for \"appid\": expected int")

		newsitems_list = app_news_dict.get("newsitems")
		if not isinstance(newsitems_list, list):
			raise TypeError("Invalid type for \"newsitems\": expected list")

		newsitems = [SteamNewsEntry.from_dict(item) for item in newsitems_list]

		return cls(
			appid=appid,
			newsitems=newsitems
		)

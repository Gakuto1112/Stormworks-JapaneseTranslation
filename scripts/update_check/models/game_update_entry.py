from dataclasses import dataclass
from typing import Self
import re

from common_modules.logger import Logger
from ..models.steam_news_entry import SteamNewsEntry


@dataclass(frozen=True, slots=True)
class GameUpdateEntry:
	"""
	Steamニュースから抽出したゲームのアップデートエントリーのデータモデル。
	"""

	version: str
	"""
	ゲームバージョン。
	"""

	title: str
	"""
	ゲームアップデートのタイトル名。
	"""

	url: str
	"""
	ゲームアップデートに関連したニュースURL。
	"""

	@classmethod
	def from_steam_news_entry(cls, steam_news_entry: SteamNewsEntry) -> Self | None:
		"""
		ゲームのアップデートのエントリーのSteamNewsEntryからGameUpdateEntryを生成する。
		入力されたSteamNewsEntryがゲームアップデートのものではない場合はNoneを返す。

		Args:
			steam_news_entry (SteamNewsEntry): Steamニュースのエントリー。

		Returns:
			Self | None: ゲームアップデートのエントリーであればGameUpdateEntryのインスタンス、そうでなければNone。
		"""

		version = re.match(r"[vV](\d+\.){2}\d+", steam_news_entry.title)
		if not isinstance(version, re.Match):
			return None

		update_title_match = re.match(r"[vV](\d+\.){2}\d+\s(-\s)?([^!]+)", steam_news_entry.title)
		if isinstance(update_title_match, re.Match):
			update_title = update_title_match.group(3)
		else:
			Logger.print_warning("Failed to extract game update title from news title.")
			update_title = ""

		return cls(
			version=version.group(0),
			title=update_title,
			url=steam_news_entry.url
		)

import argparse
import json
import urllib.request
import errno
from urllib.error import HTTPError, URLError

from common_modules.logger import Logger
from ..models.steam_news import SteamNews
from ..models.steam_news_entry import SteamNewsEntry
from ..models.game_update_entry import GameUpdateEntry


class NewsFetcher:
	"""
	StormworksのSteamニュースを取得するクラス。
	"""

	STEAM_NEWS_URL: str = "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=573090"
	"""
	SteamニュースのフェッチURL
	"""

	_debug_last_timestamp: int = 0
	"""
	最後に取得した際のタイムスタンプ（デバッグ用）
	"""

	@classmethod
	def fetch_news(cls) -> SteamNews:
		"""
		APIを利用してSteamからStormworksのニュースを取得する。

		Returns:
			SteamNews: 取得したSteamニュースのオブジェクト
		
		Raises:
			HTTPError: エラーレスポンスを受信した場合
			URLError: ネットワークエラーが発生した場合
			TimeoutError: リクエストがタイムアウトした場合
			ConnectionResetError: リクエスト実行中にネットワークが切断された場合
			UnicodeError: レスポンスのデコードに失敗した場合
		"""

		with urllib.request.urlopen(cls.STEAM_NEWS_URL) as response:
			return SteamNews.from_dict(json.loads(response))

	@staticmethod
	def filter_new_arrival_news(news_entries: list[SteamNewsEntry], from_timestamp: int) -> list[SteamNewsEntry]:
		"""
		指定したタイムスタンプ以降に公開されたニュースをフィルタリングし、リストとして返す。

		Args:
			news_entries (list[SteamNewsEntry]): Steamニュースエントリのリスト。SteamNewsオブジェクトから取得される。
			from_timestamp (int): フィルタリングの基準となるタイムスタンプ。これ以降のニュースが抽出対象となる。

		Returns:
			list[SteamNewsEntry]: フィルタリングされたニュースのリスト
		"""

		return [entry for entry in news_entries if entry.date > from_timestamp]

	@staticmethod
	def extract_game_update_news(news_entries: list[SteamNewsEntry]) -> list[GameUpdateEntry]:
		"""
		Steamニュースのエントリーのリストからゲームのアップデートに関するニュースを抽出し、GameUpdateEntryのリストとして返す。

		Args:
			news_entries (list[SteamNewsEntry]): Steamニュースのエントリーのリスト。

		Returns:
			list[GameUpdateEntry]: ゲームのアップデートに関するニュースのリスト。
		"""

		game_update_news = []
		for entry in news_entries:
			game_update_entry = GameUpdateEntry.from_steam_news_entry(entry)
			if game_update_entry is not None:
				game_update_news.append(game_update_entry)

		return game_update_news

	@classmethod
	def _set_debug_args(cls) -> None:
		"""
		デバッグ用コマンドライン引数を設定する。
		"""

		# 引数の設定
		parser = argparse.ArgumentParser(description="Steam News Fetcher for Stormworks Japanese Translation")
		parser.add_argument("last_timestamp", type=str, help="The UNIX timestamp of the last update check")

		# 引数の処理
		args = parser.parse_args()
		cls._debug_last_timestamp = int(args.last_timestamp)

	@classmethod
	def debug(cls) -> None:
		"""
		Steamニュース取得クラスのデバッグ動作を実行する。
		"""

		cls._set_debug_args()

		Logger.should_print_debug_log = True
		Logger.is_colored = True

		Logger.print_info("Steam News Fetcher for Stormworks Japanese Translation")
		Logger.print_spacer(1)

		Logger.print_info("Fetching Steam news...")

		try:
			news = cls.fetch_news()
		except HTTPError as e:
			Logger.print_error(f"Failed to fetch Steam news: got error response ({e.code})")
			exit(errno.ECONNABORTED)
		except URLError as e:
			Logger.print_error(f"Failed to fetch Steam news: network error ({e.reason})")
			exit(errno.ECONNABORTED)
		except TimeoutError:
			Logger.print_error("Failed to fetch Steam news: request timed out")
			exit(errno.ETIMEDOUT)
		except ConnectionResetError:
			Logger.print_error("Failed to fetch Steam news: connection was reset")
			exit(errno.ECONNABORTED)
		except UnicodeError:
			Logger.print_error("Failed to fetch Steam news: failed to decode response")
			exit(errno.EILSEQ)
		except Exception as e:
			Logger.print_error(f"Failed to fetch Steam news: unexpected error: {str(e)}")
			exit(errno.ECONNABORTED)

		Logger.print_info("Successfully fetched Steam news.")

		new_arrival_news = cls.filter_new_arrival_news(news.appnews.newsitems, cls._debug_last_timestamp)
		new_arrival_updates = cls.extract_game_update_news(new_arrival_news)

		Logger.print_debug("New arrival updates:")
		for entry in new_arrival_updates:
			Logger.print_debug(f"- {entry.version}: {entry.title}")
		Logger.print_spacer(1)

if __name__ == "__main__":
	NewsFetcher.debug()

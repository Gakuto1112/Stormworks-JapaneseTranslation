import urllib.request
import errno
from urllib.error import HTTPError, URLError

from common_modules.logger import Logger
from ..models.steam_news import SteamNews


class NewsFetcher:
	"""
	StormworksのSteamニュースを取得するクラス。
	"""

	STEAM_NEWS_URL: str = "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=573090"
	"""
	SteamニュースのフェッチURL
	"""

	@classmethod
	def fetchNews(cls) -> SteamNews:
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

		with urllib.request.urlopen(cls.STEAM_NEWS_URL) as res:
			response_data = res.read().decode("utf-8")

		return SteamNews(response_data)

	@classmethod
	def debug(cls) -> None:
		"""
		Steamニュース取得クラスのデバッグ動作を実行する。
		"""

		Logger.should_print_debug_log = True

		Logger.print_info("Steam News Fetcher for Stormworks Japanese Translation")
		Logger.print_spacer(1)

		Logger.print_info("Fetching Steam news...")

		try:
			news = cls.fetchNews()
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
			Logger.print_error(f"Failed to fetch Steam news: unexpected error ({e})")
			exit(errno.ECONNABORTED)

		Logger.print_info("Successfully fetched Steam news.")
		Logger.print_debug(str(news))

if __name__ == "__main__":
	NewsFetcher.debug()

from argparse import ArgumentParser, Namespace
import errno
import time
from urllib.error import HTTPError, URLError

from common_modules.logger import Logger
from .modules.news_fetcher import NewsFetcher
from .models.game_update_entry import GameUpdateEntry


def get_last_timestamp(args: Namespace) -> int:
	"""
	最後に更新を確認した際のUNIXタイムスタンプを取得する。

	Args:
		args (Namespace): 解釈されたコマンドライン引数を格納したオブジェクト

	Returns:
		int: 最後に更新を確認した際のUNIXタイムスタンプ

	Raises:
		ValueError: 無効なタイムスタンプ値が指定された場合
	"""

	try:
		timestamp_num = int(args.last_timestamp)
	except ValueError:
		raise ValueError("Invalid timestamp value specified")
	
	if timestamp_num < 0:
		raise ValueError("Invalid timestamp value specified")

	return timestamp_num

def set_args() -> ArgumentParser:
	"""
	アップデート確認スクリプトのコマンドライン引数を設定する。

	Returns:
		ArgumentParser: 設定したコマンドライン引数を管理するパーサーオブジェクト
	"""

	parser = ArgumentParser(description="Checks game updates and Creates update issues for Stormworks Japanese Translation")

	parser.add_argument("last_timestamp", type=str, help="The UNIX timestamp of the last update check")
	parser.add_argument("--colored", "-l", action="store_true", help="Enables colored output in the terminal.")
	parser.add_argument("--debug", "-d", action="store_true", help="Enables debug mode, which provides additional debug information during execution.")

	return parser

def parse_args(parser: ArgumentParser) -> Namespace:
	"""
	コマンドライン引数を解釈し、入力値をオブジェクトに格納する。

	Args:
		parser (ArgumentParser): コマンドライン引数を管理するパーサーオブジェクト

	Returns:
		Namespace: 解釈されたコマンドライン引数を格納したオブジェクト
	"""

	return parser.parse_args()

def process_args(args: Namespace) -> None:
	"""
	コマンドライン引数を処理する。

	Args:
		args (Namespace): 解釈されたコマンドライン引数を格納したオブジェクト

	Raises:
		ValueError: 無効なタイムスタンプ値が指定された場合
	"""

	if args.colored:
		Logger.is_colored = True
	if args.debug:
		Logger.should_print_debug_log = True

	get_last_timestamp(args) # タイムスタンプの整合性確認のために呼び出し

def get_new_game_update(timestamp: int) -> list[GameUpdateEntry]:
	"""
	入力されたタイムスタンプから現在までにニュース投稿されたゲームアップデートの情報を取得する。

	Args:
		timestamp (int): 最後に更新を確認した際のUNIXタイムスタンプ

	Returns:
		list[GameUpdateEntry]: 新たに投稿されたゲームアップデートの情報のリスト
	"""

	try:
		news = NewsFetcher.fetch_news()
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

	new_arrival_news = NewsFetcher.filter_new_arrival_news(news.appnews.newsitems, timestamp)
	new_game_updates = NewsFetcher.extract_game_update_news(new_arrival_news)

	return new_game_updates

def main() -> None:
	"""
	エントリー関数
	"""

	# タイトル表示
	Logger.print_info("Update Checker Tool for Stormworks Japanese Translation")
	Logger.print_spacer(1)

	# 引数の処理
	parser = set_args()
	args = parse_args(parser)
	try:
		process_args(args)
	except ValueError:
		Logger.print_error("Invalid timestamp value specified.")
		exit(errno.EINVAL)

	# 現在のタイムスタンプが最後の更新確認よりも未来のものか確認
	last_timestamp = get_last_timestamp(args)
	current_timestamp = int(time.time())

	Logger.print_debug(f"Last timestamp: {last_timestamp}")
	Logger.print_debug(f"Current timestamp: {current_timestamp}")
	Logger.print_debug(f"Difference from last check: {current_timestamp - last_timestamp}")
	Logger.print_spacer(1)

	if current_timestamp <= last_timestamp:
		Logger.print_info("This update check is being skipped because the current timestamp is not later than the last update check.")
		exit(0)

	Logger.print_info("Checking for new game updates...")

	new_game_updates = get_new_game_update(last_timestamp)
	if len(new_game_updates) > 0:
		Logger.print_info(f"Found {len(new_game_updates)} new game update(s).")
		for update in new_game_updates:
			Logger.print_debug(f"- {update.version} - {update.title}")
		# TODO: 新しいゲームアップデートに関するIssue作成の処理を作成。
	else:
		Logger.print_info("No new game updates found.")

	# TODO: 最終更新確認のタイムスタンプを更新

if __name__ == "__main__":
	main()

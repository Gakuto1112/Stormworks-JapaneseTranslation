from argparse import ArgumentParser, Namespace
import errno
import time
from urllib.error import HTTPError, URLError

from github import GithubException

from common_modules.logger import Logger
from .modules.news_fetcher import NewsFetcher
from .modules.issue_generator import IssueGenerator
from .modules.actions_variable_updater import ActionsVariableUpdater


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

	# タイムスタンプの比較
	if current_timestamp <= last_timestamp:
		Logger.print_info("This update check is being skipped because the current timestamp is not later than the last update check.")
		exit(0)

	# Steamニュースをフェッチして新しいゲームアップデートを取得
	Logger.print_info("Fetching Steam news...")

	try:
		news_game_updates = NewsFetcher.fetch_new_arrival_game_updates(last_timestamp)
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

	Logger.print_info("Fetched Steam news successfully.")

	if len(news_game_updates) > 0:
		Logger.print_info(f"Found {len(news_game_updates)} new game update(s).")
		for update in news_game_updates:
			Logger.print_debug(f"- {update.version} - {update.title}")

		# ゲームアップデート対応のIssueの作成
		Logger.print_info("Creating issues for new game updates...")
		for update in news_game_updates:
			try:
				IssueGenerator.post_issue(f"{update.version}への対応", IssueGenerator.generate_issue_content(update))
			except EnvironmentError:
				Logger.print_error("GITHUB_TOKEN or GITHUB_REPOSITORY environment variable is not set.")
				exit(errno.EINVAL)
			except GithubException as e:
				Logger.print_error(f"Failed to create issue on GitHub: {str(e)}")
				Logger.print_debug(str(e.message))
				exit(errno.ECONNABORTED)
	else:
		Logger.print_info("No new game updates found.")

	Logger.print_spacer(1)

	# 最終更新確認のタイムスタンプを更新
	Logger.print_info("Updating the last checked timestamp...")

	try:
		ActionsVariableUpdater.update_last_timestamp(current_timestamp)
	except EnvironmentError:
		Logger.print_error("GITHUB_VARIABLES_TOKEN or GITHUB_REPOSITORY environment variable is not set.")
		exit(errno.EINVAL)
	except GithubException as e:
		Logger.print_error(f"Failed to update GitHub Actions variable: {str(e)}")
		Logger.print_debug(str(e.message))
		exit(errno.ECONNABORTED)

	Logger.print_info("Updated the last checked timestamp successfully.")

if __name__ == "__main__":
	main()

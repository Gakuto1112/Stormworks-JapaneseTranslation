from argparse import ArgumentParser, Namespace
import errno

from common_modules.logger import Logger


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

if __name__ == "__main__":
	main()

from argparse import ArgumentParser, Namespace
from pathlib import Path

from common_modules.paths import paths
from common_modules.logger import Logger


def setArgs() -> ArgumentParser:
	"""
	ビルドスクリプトのコマンドライン引数を設定する。

	Returns:
		ArgumentParser: 設定したコマンドライン引数を管理するパーサーオブジェクト
	"""

	parser = ArgumentParser(description="Builds translation data for Stormworks")

	parser.add_argument("--src-path", "-i", type=str, default=paths.input_locale_path, help="Overrides default source path. Default: ../../src/japanese.tsv")
	parser.add_argument("--dist-path", "-o", type=str, default=paths.output_locale_path, help="Overrides default destination path. Default: ../../dist/japanese.tsv")
	parser.add_argument("--colored", "-l", action="store_true", help="Enables colored output in the terminal.")

	return parser

def parseArgs(parser: ArgumentParser) -> Namespace:
	"""
	コマンドライン引数を解釈し、入力値をオブジェクトに格納する。

	Args:
		parser (ArgumentParser): コマンドライン引数を管理するパーサーオブジェクト

	Returns:
		Namespace: 解釈されたコマンドライン引数を格納したオブジェクト
	"""

	return parser.parse_args()

def processArgs(args: Namespace) -> None:
	"""
	コマンドライン引数を処理する。

	Args:
		args (Namespace): 解釈されたコマンドライン引数を格納したオブジェクト
	"""

	paths.input_locale_path = Path(args.src_path)
	paths.output_locale_path = Path(args.dist_path)
	if args.colored:
		Logger.is_colored = True

def main() -> None:
	"""
	エントリー関数
	"""

	# 引数の処理
	parser = setArgs()
	args = parseArgs(parser)
	processArgs(args)

if __name__ == "__main__":
	main()

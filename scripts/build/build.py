from argparse import ArgumentParser, Namespace
from pathlib import Path
import errno

from common_modules.paths import paths
from common_modules.logger import Logger
from common_modules.config_reader import ConfigReader
from common_modules.errors.config_not_loaded_error import ConfigNotLoadedError
from .modules.translation_data_builder import TranslationDataBuilder


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
	parser.add_argument("--debug", "-d", action="store_true", help="Enables debug mode, which provides additional debug information during execution.")

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
	if args.debug:
		Logger.should_print_debug_log= True

def build() -> None:
	"""
	翻訳データをビルドする。
	"""

	Logger.print_info("Loading configuration...")

	try:
		ConfigReader.read_config()
	except FileNotFoundError:
		Logger.print_error(f"Configuration file not found ({paths.config_path})")
		exit(errno.ENOENT)
	except IsADirectoryError:
		Logger.print_error(f"Configuration path is a directory ({paths.config_path})")
		exit(errno.EISDIR)
	except PermissionError:
		Logger.print_error(f"No permission to read configuration file ({paths.config_path})")
		exit(errno.EACCES)
	except IOError:
		Logger.print_error(f"An unexpected I/O error occurred while reading the configuration file ({paths.config_path})")
		exit(errno.EIO)
	except Exception as e:
		Logger.print_error(f"An unexpected error occurred while reading the configuration file ({paths.config_path}): {str(e)}")
		exit(errno.EPERM)

	Logger.print_info("Configuration loaded successfully.")

	try:
		TranslationDataBuilder.build()
	except FileNotFoundError:
		Logger.print_error(f"Translation source file not found ({paths.input_locale_path})")
		exit(errno.ENOENT)
	except IsADirectoryError:
		Logger.print_error(f"Translation source file is a directory ({paths.input_locale_path})")
		exit(errno.EISDIR)
	except PermissionError:
		Logger.print_error(f"No permission to read/write translation files ({paths.input_locale_path} / {paths.output_locale_path})")
		exit(errno.EACCES)
	except IOError:
		Logger.print_error("An unexpected I/O error occurred.")
		exit(errno.EIO)
	except ConfigNotLoadedError:
		Logger.print_error("Tool configuration has not been loaded yet. This error should not occur if the tool is used correctly. Please report this issue to the developer.")
		exit(errno.EPERM)
	except Exception as e:
		Logger.print_error(f"An unexpected error occurred while building translation data: {str(e)}")
		exit(errno.EPERM)

def main() -> None:
	"""
	エントリー関数
	"""

	# タイトル表示
	Logger.print_info("Translation Data Build Tool for Stormworks Japanese Translation")
	Logger.print_spacer(1)

	# 引数の処理
	parser = setArgs()
	args = parseArgs(parser)
	processArgs(args)

	# 設定値のデバッグ出力
	Logger.print_debug(f"Input source path: {paths.input_locale_path}")
	Logger.print_debug(f"Output destination path: {paths.output_locale_path}")
	Logger.print_debug(f"Configuration file path: {paths.config_path}")
	Logger.print_spacer(1)

	Logger.print_info("Building translation data...")

	# ビルド
	build()

	Logger.print_info(f"Completed building translation data.")
	Logger.print_info(f"The built translation data has been saved to \"{paths.output_locale_path}\".")

if __name__ == "__main__":
	main()

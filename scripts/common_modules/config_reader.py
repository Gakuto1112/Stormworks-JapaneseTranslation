import tomllib
import errno
from argparse import ArgumentParser

from .paths import paths
from .logger import Logger
from .errors.config_not_loaded_error import ConfigNotLoadedError
from .models.config_models.config import Config


class ConfigReader:
	"""
	ツールの設定値をファイルから読み取り、設定値を他のモジュールに提供するクラス
	"""

	_config: Config|None = None
	"""
	ファイルから読み込んだ設定値を格納するインスタンス。
	`None`の場合はまだ読み込んでいないことを示す。
	"""

	@classmethod
	def read_config(cls) -> None:
		"""
		ツールの設定値をファイルから読み取り、モジュール内にロードする。
		既にロード済みの場合に呼び出すと、設定値をリロードする。

		Raises:
			FileNotFoundError: 指定されたパスにファイルが存在しない場合
			IsADirectoryError: 指定されたパスがディレクトリである場合
			PermissionError: 指定されたパスのファイルに対する読み取り�権限がない場合
			IOError: その他の入出力エラーが発生した場合
			TypeError: 設定値の形式が正しくない場合
		"""

		cls._config = None

		with open(paths.config_path, "rb") as file:
			raw_config = tomllib.load(file)

		cls._config = Config.from_dict(raw_config)

	@classmethod
	def get_separator(cls) -> str:
		"""
		設定値から翻訳データの区切り文字(`build.separator`)を取得する。

		Returns:
			str: 設定値から取得した翻訳データの区切り文字

		Raises:
			ConfigNotLoadedError: 設定値がロードされる前に呼び出された場合
		"""

		if cls._config is None:
			raise ConfigNotLoadedError("Configuration has not been loaded yet. Please call read_config() before accessing configuration values.")

		return cls._config.build.separator

	@staticmethod
	def _set_debug_args() -> None:
		"""
		デバッグ用コマンドライン引数を設定する。
		"""

		# 引数の設定
		parser = ArgumentParser(description="Config Reader for Stormworks Japanese translation")
		parser.add_argument("--src-path", "-i", type=str, default=paths.config_path, help="Overrides default config file path. Default: ../config.toml")
		parser.add_argument("--colored", "-l", action="store_true", help="Enables colored output in the terminal.")

		# パスの設定
		args = parser.parse_args()
		paths.config_path = args.src_path
		if args.colored:
			Logger.is_colored = True

	@classmethod
	def debug(cls) -> None:
		"""
		動作確認用のメソッド
		"""

		cls._set_debug_args()
		Logger.should_print_debug_log = True

		# デバッグ出力
		Logger.print_info("Config Reader for Stormworks Japanese translation")
		Logger.print_spacer(1)
		Logger.print_info(f"Reading config from \"{paths.config_path}\" ...")

		try:
			cls.read_config()
		except FileNotFoundError:
			Logger.print_error(f"The specified config file was not found ({paths.config_path})")
			exit(errno.ENOENT)
		except IsADirectoryError:
			Logger.print_error(f"The specified config file is a directory ({paths.config_path})")
			exit(errno.EISDIR)
		except PermissionError:
			Logger.print_error(f"No permission to read the specified config file ({paths.config_path})")
			exit(errno.EACCES)
		except IOError:
			Logger.print_error(f"An unexpected error occurred while reading the config file ({paths.config_path})")
			exit(errno.EIO)

		Logger.print_info(f"Successfully read config from \"{paths.config_path}\"")
		Logger.print_spacer(1)
		Logger.print_debug(str(cls._config))

if __name__ == "__main__":
	ConfigReader.debug()

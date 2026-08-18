from argparse import ArgumentParser
import errno
import re

from common_modules.paths import paths
from common_modules.logger import Logger
from common_modules.translation_data_reader import TranslationDataReader
from common_modules.config_reader import ConfigReader
from common_modules.models.translation_key import TranslationKey


class TranslationDataBuilder:
	"""
	翻訳データをソースからビルドするクラス
	"""

	@staticmethod
	def _prepare_dist_directory() -> None:
		"""
		ビルド済みの翻訳データを出力するディレクトリを作成する。
		すでにディレクトリが存在する場合は何もしない。

		Raises:
			PermissionError: ディレクトリの作成権限がない場合
			IOError: その他の入出力エラーが発生した場合
		"""

		dist_directory = paths.output_locale_path.parent
		if not dist_directory.exists():
			dist_directory.mkdir(parents=True, exist_ok=True)

	@staticmethod
	def _write_translation_output(translation_data: str) -> None:
		"""
		入力された文字列を翻訳データを出力ファイルに書き込む。

		Args:
			translation_data (str): 書き込む翻訳データの文字列

		Raises:
			IsADirectoryError: 指定されたパスがディレクトリである場合
			PermissionError: 指定されたパスのファイルに対する書き込み権限がない場合
			IOError: その他の入出力エラーが発生した場合
		"""

		with open(paths.output_locale_path, "w", encoding="utf-8") as file:
			file.write(translation_data)

	@staticmethod
	def _merge_component_names(translation_data: str) -> str:
		"""
		ゲーム内コンポーネントの名称の和訳と英語原文を結合して返す。
		和訳と英語原文の間に挟まる区切り文字はコンフィグファイルから読み込まれる。

		Args:
			translation_data (str): 書き込む翻訳データの文字列

		Returns:
			str: マージ済みの翻訳データの文字列
		"""

		merged_translation_data = ""

		for key in TranslationDataReader.get_translation_key_iterator(translation_data):
			if key.id is not None and key.en is not None and key.jp is not None and re.fullmatch(r"def_.+_name", key.id) is not None:
				merged_translation_data += f"{key.id}\t\t{key.en}\t{key.jp}{ConfigReader.get_separator()}{key.en}\n"
			else:
				merged_translation_data += f"{key.id if key.id is not None else ''}\t\t{key.en if key.en is not None else ''}\t{key.jp if key.jp is not None else ''}\n"

		return merged_translation_data

	@staticmethod
	def build() -> None:
		"""
		翻訳データのビルドを行う。

		このメソッドは以下の動作を行う。

		1. 翻訳データをソースファイルから読み込む。
		2. ゲーム内コンポーネントの名称の和訳と英語原文を結合する。
		3. ビルド済みの翻訳データを出力するディレクトリがなければ作成する。
		4. ビルド済みの翻訳データを出力ファイルに書き込む。

		このメソッドはConfigReaderがロードした設定値を使用するため、このメソッドを呼ぶ前に少なくとも1回はConfigReader.read_config()を呼び出す必要がある。

		Raises:
			FileNotFoundError: 指定されたパスにファイルが存在しない場合
			IsADirectoryError: 指定されたパスがディレクトリである場合
			PermissionError: 指定されたパスのファイルに対する読み取り/書き込み権限がない場合
			IOError: その他の入出力エラーが発生した場合
			ConfigNotLoadedError: 設定値がロードされる前に呼び出された場合
		"""

		source_data = TranslationDataReader.read_translation_source()
		merged_data = TranslationDataBuilder._merge_component_names(source_data)
		TranslationDataBuilder._prepare_dist_directory()
		TranslationDataBuilder._write_translation_output(merged_data)
	
	@staticmethod
	def _set_debug_args() -> None:
		"""
		デバッグ用コマンドライン引数を設定する。
		"""

		# 引数の設定
		parser = ArgumentParser(description="Translation data builder for Stormworks Japanese translation")
		parser.add_argument("--src-path", "-i", type=str, default=paths.input_locale_path, help="Overrides default source path. Default: ../../src/japanese.tsv")
		parser.add_argument("--colored", "-l", action="store_true", help="Enables colored output in the terminal.")

		# パスの設定
		args = parser.parse_args()
		paths.input_locale_path = args.src_path
		if args.colored:
			Logger.is_colored = True

	@classmethod
	def debug(cls) -> None:
		"""
		動作確認用のメソッド
		"""

		cls._set_debug_args()
		Logger.should_print_debug_log = True

		ConfigReader.read_config()

		# デバッグ出力
		Logger.print_info("Translation data builder for Stormworks Japanese translation")
		Logger.print_spacer(1)
		Logger.print_info(f"Reading translation source from \"{paths.input_locale_path}\" ...")

		try:
			source_data = TranslationDataReader.read_translation_source()
		except FileNotFoundError:
			Logger.print_error(f"The specified translation source file was not found ({paths.input_locale_path})")
			exit(errno.ENOENT)
		except IsADirectoryError:
			Logger.print_error(f"The specified translation source file is a directory ({paths.input_locale_path})")
			exit(errno.EISDIR)
		except PermissionError:
			Logger.print_error(f"No permission to read the specified translation source file ({paths.input_locale_path})")
			exit(errno.EACCES)
		except IOError:
			Logger.print_error(f"An unexpected error occurred while reading the translation source file ({paths.input_locale_path})")
			exit(errno.EIO)

		if Logger.should_print_debug_log:
			Logger.print_spacer(1)
		Logger.print_info(f"Successfully read translation source from \"{paths.input_locale_path}\"")

		merged_data = cls._merge_component_names(source_data)

		try:
			TranslationDataBuilder._prepare_dist_directory()
		except PermissionError:
			Logger.print_error(f"No permission to create the output directory for translation data ({paths.output_locale_path.parent})")
			exit(errno.EACCES)
		except IOError:
			Logger.print_error(f"An unexpected error occurred while creating the output directory for translation data ({paths.output_locale_path.parent})")
			exit(errno.EIO)

		try:
			TranslationDataBuilder._write_translation_output(merged_data)
		except IsADirectoryError:
			Logger.print_error(f"The specified translation output file is a directory ({paths.output_locale_path})")
			exit(errno.EISDIR)
		except PermissionError:
			Logger.print_error(f"No permission to write to the specified translation output file ({paths.output_locale_path})")
			exit(errno.EACCES)
		except IOError:
			Logger.print_error(f"An unexpected error occurred while writing to the translation output file ({paths.output_locale_path})")
			exit(errno.EIO)

		Logger.print_info(f"Successfully wrote translation data to \"{paths.output_locale_path}\"")

if __name__ == "__main__":
	TranslationDataBuilder.debug()

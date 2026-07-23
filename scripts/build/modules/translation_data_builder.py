import errno

from common_modules.paths import paths
from common_modules.logger import Logger


class TranslationDataBuilder:
	"""
	翻訳データをソースからビルドするクラス
	"""

	@staticmethod
	def _read_translation_source() -> str:
		"""
		翻訳データのソースファイルを読み込み、その内容を文字列として返す。

		Returns:
			str: 読み込んだ翻訳データの文字列

		Raises:
			FileNotFoundError: 指定されたパスにファイルが存在しない場合
			IsADirectoryError: 指定されたパスがディレクトリである場合
			PermissionError: 指定されたパスのファイルに対する読み取り権限がない場合
			IOError: その他の入出力エラーが発生した場合
		"""

		with open(paths.input_locale_path, "r", encoding="utf-8") as file:
			return file.read()

	@staticmethod
	def debug() -> None:
		"""
		動作確認用のメソッド
		"""

		# デバッグ出力
		Logger.print_info("Translation data builder for Stormworks Japanese translation")
		Logger.print_spacer(1)
		Logger.print_info(f"Reading translation source from \"{paths.input_locale_path}\" ...")

		try:
			source_data = TranslationDataBuilder._read_translation_source()
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

		Logger.print_debug(source_data)
		if Logger.should_print_debug_log:
			Logger.print_spacer(1)
		Logger.print_info(f"Successfully read translation source from \"{paths.input_locale_path}\"")

if __name__ == "__main__":
	TranslationDataBuilder.debug()

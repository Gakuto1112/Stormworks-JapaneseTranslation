from common_modules.paths import paths


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

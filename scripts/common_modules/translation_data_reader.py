from .paths import paths
from .models.translation_key import TranslationKey

class TranslationDataReader:
	"""
	翻訳データを読み込むクラス。
	"""

	@staticmethod
	def read_translation_source() -> str:
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
	def get_translation_key_iterator(translation_data: str):
		"""
		翻訳データの文字列から、各行をTranslationKeyオブジェクトに変換するイテレータを返す。

		Args:
			translation_data (str): 翻訳データの文字列

		Yields:
			TranslationKey: 翻訳データの各行を表すTranslationKeyオブジェクト
		"""

		for line in translation_data.splitlines():
			chunks = line.split("\t")
			yield TranslationKey(id=chunks[0] if chunks[0] != "" else None, en=chunks[2] if chunks[2] != "" else None, jp=chunks[3] if chunks[3] != "" else None)

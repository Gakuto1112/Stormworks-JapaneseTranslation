from .models.translation_key import TranslationKey

class TranslationKeyIteratorGenerator:
	"""
	翻訳データの各行を翻訳キーに変換し、各キーのイテレータを返すクラス
	"""

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

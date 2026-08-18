from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class TranslationKey:
	"""
	翻訳キー1つのデータを表すクラス
	"""

	id: str | None = None
	"""
	翻訳ID
	"""

	en: str | None = None
	"""
	英語原文
	"""

	jp: str | None = None
	"""
	和訳
	"""

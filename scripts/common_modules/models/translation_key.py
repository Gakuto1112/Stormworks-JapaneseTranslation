from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class TranslationKey:
	"""
	翻訳ID
	"""
	id: str | None = None

	"""
	英語原文
	"""
	en: str | None = None

	"""
	和訳
	"""
	jp: str | None = None

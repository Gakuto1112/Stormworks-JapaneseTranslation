from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class TestConfig:
	"""
	テストの設定値のデータを表すクラス
	"""

	prohibited_characters: list[str]
	"""
	和訳文の中に含まれてはいけない禁止文字のリスト
	"""

from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class BuildConfig:
	"""
	ビルド設定値のデータを表すクラス
	"""
	
	separator: str
	"""
	ゲーム内コンポーネントの和訳と英語原文をマージするときの区切り文字
	"""

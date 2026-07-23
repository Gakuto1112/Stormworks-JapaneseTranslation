from dataclasses import dataclass
from pathlib import Path

@dataclass
class Paths:
	_root: Path = Path(__file__).resolve().parent.parent.parent
	"""
	レポジトリのルートディレクトリのパス
	"""

	@property
	def root(self) -> Path:
		"""
		レポジトリのルートディレクトリのパス
		"""

		return self._root

	@property
	def input_locale_path(self) -> Path:
		"""
		入力データとなるローカルデータのパス
		"""

		return self._root / "src" / "japanese.tsv"

	@property
	def output_locale_path(self) -> Path:
		"""
		ビルド済みのローカルデータの出力パス
		"""

		return self._root / "dist" / "japanese.tsv"

paths = Paths()

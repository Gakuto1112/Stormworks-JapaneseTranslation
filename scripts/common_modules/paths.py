from dataclasses import dataclass
from pathlib import Path

@dataclass
class Paths:
	_root: Path = Path(__file__).resolve().parent.parent.parent
	"""
	レポジトリのルートディレクトリのパス
	"""

	_input_locale_path: Path = _root / "src" / "japanese.tsv"
	"""
	入力データとなるロケールデータのパス
	"""

	_output_locale_path: Path = _root / "dist" / "japanese.tsv"
	"""
	ビルド済みのロケールデータの出力パス
	"""

	_config_path: Path = _root / "scripts" / "config.toml"
	"""
	ツールの設定ファイルのパス
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
		入力データとなるロケールデータのパス
		"""

		return self._input_locale_path

	@input_locale_path.setter
	def input_locale_path(self, path: Path) -> None:
		"""
		input_locale_pathのセッター関数
		"""

		self._input_locale_path = path

	@property
	def output_locale_path(self) -> Path:
		"""
		ビルド済みのロケールデータの出力パス
		"""

		return self._output_locale_path

	@output_locale_path.setter
	def output_locale_path(self, path: Path) -> None:
		"""
		output_locale_pathのセッター関数
		"""

		self._output_locale_path = path

	@property
	def config_path(self) -> Path:
		"""
		ツールの設定ファイルのパス
		"""

		return self._config_path

	@config_path.setter
	def config_path(self, path: Path) -> None:
		"""
		config_pathのセッター関数
		"""

		self._config_path = path

paths = Paths()

from dataclasses import dataclass
from typing import Self

from ...paths import paths
from .build_config import BuildConfig
from .test_config import TestConfig


@dataclass(frozen=True, slots=True)
class Config:	
	"""
	ツールの設定値のデータを表すクラス
	"""

	build: BuildConfig
	"""
	ビルド設定値
	"""

	test: TestConfig
	"""
	テストの設定値
	"""

	@classmethod
	def from_dict(cls, config_dict: dict) -> Self:
		"""
		辞書型の設定値からConfigクラスのインスタンスを生成する。

		Args:
			config_dict (dict): 設定値を格納した辞書

		Returns:
			Self: 設定値を格納したConfigクラスのインスタンス

		Raises:
			TypeError: 設定値の形式が正しくない場合
		"""

		build_config = config_dict.get("build", dict())
		if not isinstance(build_config, dict):
			raise TypeError(f"The \"build\" section is required in the configuration file ({paths.config_path})")

		separator = build_config.get("separator", None)
		if not isinstance(separator, str):
			raise TypeError(f"The \"separator\" value in the \"build\" section must be a string in the configuration file ({paths.config_path})")

		test_config = config_dict.get("test", dict())
		if not isinstance(test_config, dict):
			raise TypeError(f"The \"test\" section is required in the configuration file ({paths.config_path})")

		prohibited_characters = test_config.get("prohibited_characters", None)
		if not isinstance(prohibited_characters, list) or not all(isinstance(char, str) for char in prohibited_characters):
			raise TypeError(f"The \"prohibited_characters\" value in the \"test\" section must be a list of strings in the configuration file ({paths.config_path})")

		return cls(
			build=BuildConfig(separator=separator),
			test=TestConfig(prohibited_characters=prohibited_characters)
		)

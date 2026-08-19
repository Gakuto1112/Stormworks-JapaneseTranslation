import os
import re
import unittest
from pathlib import Path

from common_modules.paths import paths


class TestReadmeGameVersion(unittest.TestCase):
	_tag_name: str|None = os.getenv("TAG_NAME")
	"""
	比較を行うタグ（バージョン）の名前
	"""

	def _read_file(self, file_path: Path) -> str:
		"""
		指定されたファイルの内容を文字列として読み込む。

		Args:
			file_path (Path): 読み込むファイルのパス

		Returns:
			str: 読み込んだファイルの内容

		Raises:
			FileNotFoundError: 指定されたファイルが存在しない場合
			IsADirectoryError: 指定されたパスがディレクトリである場合
			PermissionError: ファイルの読み取り権限がない場合
			IOError: その他の入出力エラーが発生した場合
		"""

		with open(file_path, "r", encoding="utf-8") as file:
			return file.read()

	def test_readme_game_version(self) -> None:
		"""
		`README.md`と`README_en.md`に記載されている対応ゲームバージョンが、指定されたタグ名に含まれる対応ゲームバージョンと一致するかテストする。
		"""

		print(f"Target tag name: {self._tag_name}")

		if self._tag_name is None or len(self._tag_name) == 0:
			self.skipTest("Target tag name is not provided. Skipping game version test.")
		
		match = re.fullmatch(r"v(\d+\.\d+\.\d+)-[a-z]", self._tag_name)

		if match is None:
			self.fail(f"Invalid tag name format: {self._tag_name}. Expected format: vX.Y.Z-suffix (e.g., v1.0.0-a).")

		for path in [paths.readme_jp_path, paths.readme_en_path]:
			with self.subTest(file=path.name):
				try:
					content = self._read_file(path)
				except FileNotFoundError:
					self.fail(f"Readme file not found ({path}).")
				except IsADirectoryError:
					self.fail(f"Readme file path is a directory, not a file ({path}).")
				except PermissionError:
					self.fail(f"No permission to read readme file ({path}).")
				except IOError:
					self.fail(f"An unexpected I/O error occurred while reading readme file ({path}).")
				except Exception as e:
					self.fail(f"An unexpected error occurred while reading readme file ({path}): {str(e)}")

				readme_anchor_match = re.search(r"<!--\sTARGET_GAME_VERSION_START\s-->(.*?)<!--\sTARGET_GAME_VERSION_END\s-->", content, re.DOTALL)

				if readme_anchor_match is None:
					self.fail(f"Target game version anchor not found in \"{path.name}\"")

				readme_version_match = re.match(r"(\d+\.\d+\.\d+)", readme_anchor_match.group(1).strip())

				if readme_version_match is None:
					self.fail(f"Invalid target game version format in \"{path.name}\". Expected format: X.Y.Z (e.g., 1.0.0).")

				self.assertEqual(readme_version_match.group(1), match.group(1), f"The target game version in \"{path.name}\" does not match the version in the tag name ({match.group(1)}).")

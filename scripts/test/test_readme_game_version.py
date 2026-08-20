import os
import re
import unittest

from common_modules.paths import paths
from common_modules.file_reader import FileReader


class TestReadmeGameVersion(unittest.TestCase):
	_tag_name: str|None = os.getenv("TAG_NAME")
	"""
	比較を行うタグ（バージョン）の名前
	"""

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
					content = FileReader.read_file(path)
				except FileNotFoundError:
					self.fail(f"Readme file not found ({path}).")
				except IsADirectoryError:
					self.fail(f"Readme file path is a directory, not a file ({path}).")
				except PermissionError:
					self.fail(f"No permission to read readme file ({path}).")
				except UnicodeDecodeError:
					self.fail(f"Failed to decode readme file ({path}).")
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

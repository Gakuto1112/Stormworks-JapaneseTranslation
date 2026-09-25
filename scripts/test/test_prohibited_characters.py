import unittest
import re

from common_modules.paths import paths
from common_modules.config_reader import ConfigReader
from common_modules.errors.config_not_loaded_error import ConfigNotLoadedError
from common_modules.file_reader import FileReader
from common_modules.translation_key_iterator_generator import TranslationKeyIteratorGenerator


class TestProhibitedCharacters(unittest.TestCase):
	def test_prohibited_characters(self):
		"""
		和訳文の中に禁止文字が含まれていないかをテストする。
		禁止文字のリストはConfigReader経由で、config.tomlから読み取る。
		"""

		try:
			ConfigReader.read_config()
		except FileNotFoundError:
			self.fail(f"Configuration file not found ({paths.config_path}).")
		except IsADirectoryError:
			self.fail(f"Configuration file path is a directory ({paths.config_path}).")
		except PermissionError:
			self.fail(f"No permission to read/write configuration file ({paths.config_path}).")
		except IOError:
			self.fail(f"An unexpected I/O error occurred while reading the configuration file ({paths.config_path}).")
		except Exception as e:
			self.fail(f"An unexpected error occurred while reading the configuration file ({paths.config_path}): {str(e)}")

		try:
			prohibited_characters = ConfigReader.get_prohibited_characters()
		except ConfigNotLoadedError:
			self.fail("Tool configuration has not been loaded yet. This error should not occur if the tool is used correctly. Please report this issue to the developer.")
		except Exception as e:
			self.fail(f"An unexpected error occurred while retrieving prohibited characters: {str(e)}")

		try:
			for i, key in enumerate(TranslationKeyIteratorGenerator.get_translation_key_iterator(FileReader.read_file(paths.input_locale_path))):
				if key.jp is not None:
					with self.subTest(line=i + 1):
						self.assertTrue(re.search(rf"[{re.escape(''.join(prohibited_characters))}]", key.jp) is None, f"One or more prohibited characters detected in Japanese translation at line {i + 1})")
		except FileNotFoundError:
			self.fail(f"Translation source file not found ({paths.input_locale_path}).")
		except IsADirectoryError:
			self.fail(f"Translation source path is a directory ({paths.input_locale_path}).")
		except PermissionError:
			self.fail(f"No permission to read translation source file ({paths.input_locale_path}).")
		except IOError:
			self.fail(f"An unexpected I/O error occurred while reading the translation source file ({paths.input_locale_path}).")
		except Exception as e:
			self.fail(f"An unexpected error occurred while reading the translation source file ({paths.input_locale_path}): {str(e)}")

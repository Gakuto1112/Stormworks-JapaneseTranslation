import unittest

from common_modules.paths import paths
from common_modules.config_reader import ConfigReader
from common_modules.translation_data_reader import TranslationDataReader


class TestMissingTranslations(unittest.TestCase):
	def test_missing_translations(self):
		"""
		抜けている和訳文がないかをテストする。
		"""

		try:
			ConfigReader.read_config()
		except FileNotFoundError:
			self.fail(f"Configuration file not found ({paths.config_path}).")
		except IsADirectoryError:
			self.fail(f"Configuration path is a directory ({paths.config_path}).")
		except PermissionError:
			self.fail(f"No permission to read/write configuration file ({paths.config_path}).")
		except IOError:
			self.fail(f"An unexpected I/O error occurred while reading the configuration file ({paths.config_path}).")
		except Exception as e:
			self.fail(f"An unexpected error occurred while reading the configuration file ({paths.config_path}): {str(e)}")

		try:
			for i, key in enumerate(TranslationDataReader.get_translation_key_iterator(TranslationDataReader.read_translation_source())):
				if key.en is not None:
					with self.subTest(line=i + 1):
						self.assertTrue(key.jp is not None, f"Missing Japanese translation at line {i + 1}")
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

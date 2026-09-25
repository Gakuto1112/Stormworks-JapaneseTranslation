import errno

from common_modules.logger import Logger
from common_modules.paths import paths
from common_modules.file_reader import FileReader


class IssueGenerator:
	"""
	ゲームアップデート対応に関するIssueを生成し、APIを通じて投稿するクラス。
	"""

	@staticmethod
	def read_template() -> str:
		"""
		ゲームアップデート対応Issueのテンプレートを読み込む。

		Returns:
			テンプレートの内容を文字列として返す。

		Raises:
			FileNotFoundError: 指定されたファイルが存在しない場合
			IsADirectoryError: 指定されたパスがディレクトリである場合
			PermissionError: ファイルの読み取り権限がない場合
			UnicodeDecodeError: ファイルの内容のデコードに失敗した場合（バイナリファイルを読み込もうとした場合など）
			IOError: その他の入出力エラーが発生した場合
		"""

		return FileReader.read_file(paths.game_update_issue_template_path)

	@classmethod
	def debug(cls) -> None:
		"""
		Issue生成クラスのデバッグ動作を実行する。
		"""

		Logger.should_print_debug_log = True
		Logger.is_colored = True

		Logger.print_info("Issue Generator for Stormworks Japanese Translation")
		Logger.print_spacer(1)

		Logger.print_info("Reading issue template...")
		try:
			template = cls.read_template()
		except FileNotFoundError:
			Logger.print_error(f"Issue template file not found ({paths.game_update_issue_template_path})")
			exit(errno.ENOENT)
		except IsADirectoryError:
			Logger.print_error(f"Issue template file path is a directory ({paths.game_update_issue_template_path})")
			exit(errno.EISDIR)
		except PermissionError:
			Logger.print_error(f"No permission to read issue template file ({paths.game_update_issue_template_path})")
			exit(errno.EACCES)
		except IOError:
			Logger.print_error(f"An unexpected I/O error occurred while reading the issue template file ({paths.game_update_issue_template_path})")
			exit(errno.EIO)
		except Exception as e:
			Logger.print_error(f"An unexpected error occurred while reading the issue template file ({paths.game_update_issue_template_path}): {str(e)}")
			exit(errno.EPERM)

		Logger.print_info("Issue template loaded successfully.")
		Logger.print_spacer(1)

if __name__ == "__main__":
	IssueGenerator.debug()

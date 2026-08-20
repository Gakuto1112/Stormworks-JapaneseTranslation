from pathlib import Path

class FileReader:
	"""
	テキストファイルを読み取るクラス
	"""

	@staticmethod
	def read_file(file_path: Path) -> str:
		"""
		指定されたパスのファイルの内容を文字列として読み込む。

		Args:
			file_path (Path): 読み込むファイルのパス

		Returns:
			str: 読み込んだファイルの内容

		Raises:
			FileNotFoundError: 指定されたファイルが存在しない場合
			IsADirectoryError: 指定されたパスがディレクトリである場合
			PermissionError: ファイルの読み取り権限がない場合
			UnicodeDecodeError: ファイルの内容のデコードに失敗した場合（バイナリファイルを読み込もうとした場合など）
			IOError: その他の入出力エラーが発生した場合
		"""

		with open(file_path, "r", encoding="utf-8") as file:
			return file.read()

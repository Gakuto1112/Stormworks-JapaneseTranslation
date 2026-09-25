import os

from github import Github, Auth


class ActionsVariableUpdater:
	"""
	Github ActionsのVariablesを更新するクラス。
	"""

	_LAST_TIMESTAMP_VARIABLE_NAME = "LAST_TIMESTAMP"
	"""
	最終更新確認タイムスタンプのVariable名
	"""

	@classmethod
	def update_last_timestamp(cls, new_timestamp: int) -> None:
		"""
		GitHub ActionsのVariablesにおける最終更新確認タイムスタンプを更新する。
		必要なアクセストークンは環境変数から取得する。

		Args:
			new_timestamp (int): 新しい最終更新確認タイムスタンプ

		Raises:
			EnvironmentError: 必要な環境変数が設定されていない場合
			GithubException: GitHub APIの操作中にエラーが発生した場合
		"""

		token = os.getenv("ACTIONS_VARIABLES_TOKEN")
		repository = os.getenv("GITHUB_REPOSITORY")

		if not token or not repository:
			raise EnvironmentError("ACTIONS_VARIABLES_TOKEN or GITHUB_REPOSITORY environment variable is not set.")

		github = Github(auth=Auth.Token(token))
		repository = github.get_repo(repository)

		variable = repository.get_variable(cls._LAST_TIMESTAMP_VARIABLE_NAME)
		variable.edit(str(new_timestamp))

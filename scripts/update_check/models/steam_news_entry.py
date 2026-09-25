from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True, slots=True)
class SteamNewsEntry:
	"""
	Steamからニュースをフェッチする際のレスポンスのデータモデル。
	ニュースエントリー1件のデータモデル。
	"""

	gid: str
	"""
	ニュースエントリーのID。
	"""

	title: str
	"""
	ニュースエントリーのタイトル。
	"""

	url: str
	"""
	ニュースエントリーにアクセスできるURL。
	この文字列はそのままURL型に変換可能。
	"""

	is_external_url: bool
	"""
	ニュースエントリーURLが外部のものかどうか。（要検証）
	"""

	author: str
	"""
	ニュースエントリーの作者。
	"""

	contents: str
	"""
	ニュースエントリーの本文。
	"""

	feedlabel: str
	"""
	ニュースエントリーの種類？
	"""

	date: int
	"""
	ニュースエントリーが投稿された日時を示すUNIXタイムスタンプ。
	"""

	feedname: str
	"""
	ニュースエントリー種類の名称？
	"""

	feed_type: int
	"""
	ニュースエントリーの種類を示す値？
	"""

	appid: int
	"""
	ニュースエントリーが関連するアプリ（ゲーム）ID。
	"""

	tags: list[str] | None = None
	"""
	ニュースエントリーに関連付けられたタグのリスト？
	"""

	@classmethod
	def from_dict(cls, entry_dict: dict) -> Self:
		"""
		辞書型のニュースエントリーからSteamNewsEntryクラスのインスタンスを生成する。

		Args:
			entry_dict (dict): Steamニュースエントリーの辞書型レスポンス。

		Returns:
			Self: 生成されたSteamNewsEntryのインスタンス。

		Raises:
			TypeError: 辞書型の構造が正しくない場合
		"""

		gid = entry_dict.get("gid")
		if not isinstance(gid, str):
			raise TypeError("Invalid type for \"gid\": expected str")

		title = entry_dict.get("title")
		if not isinstance(title, str):
			raise TypeError("Invalid type for \"title\": expected str")

		url = entry_dict.get("url")
		if not isinstance(url, str):
			raise TypeError("Invalid type for \"url\": expected str")

		is_external_url = entry_dict.get("is_external_url")
		if not isinstance(is_external_url, bool):
			raise TypeError("Invalid type for \"is_external_url\": expected bool")

		author = entry_dict.get("author")
		if not isinstance(author, str):
			raise TypeError("Invalid type for \"author\": expected str")

		contents = entry_dict.get("contents")
		if not isinstance(contents, str):
			raise TypeError("Invalid type for \"contents\": expected str")

		feedlabel = entry_dict.get("feedlabel")
		if not isinstance(feedlabel, str):
			raise TypeError("Invalid type for \"feedlabel\": expected str")

		date = entry_dict.get("date")
		if not isinstance(date, int):
			raise TypeError("Invalid type for \"date\": expected int")

		feedname = entry_dict.get("feedname")
		if not isinstance(feedname, str):
			raise TypeError("Invalid type for \"feedname\": expected str")

		feed_type = entry_dict.get("feed_type")
		if not isinstance(feed_type, int):
			raise TypeError("Invalid type for \"feed_type\": expected int")

		appid = entry_dict.get("appid")
		if not isinstance(appid, int):
			raise TypeError("Invalid type for \"appid\": expected int")

		tags = entry_dict.get("tags")
		if tags is not None and not isinstance(tags, list):
			raise TypeError("Invalid type for \"tags\": expected list or None")

		return cls(
			gid=gid,
			title=title,
			url=url,
			is_external_url=is_external_url,
			author=author,
			contents=contents,
			feedlabel=feedlabel,
			date=date,
			feedname=feedname,
			feed_type=feed_type,
			appid=appid,
			tags=tags
		)

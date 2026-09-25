from dataclasses import dataclass


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

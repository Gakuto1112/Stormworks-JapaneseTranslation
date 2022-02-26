# Stormworks日本語訳データ配布ページ
対応ゲームバージョン ： **1.4.9**
## はじめに
これは[Stormworks](https://store.steampowered.com/app/573090/Stormworks_Build_and_Rescue/)の日本語の翻訳データを配布するページです。既に[Steamワークショップ上に存在する日本語訳データ](https://steamcommunity.com/sharedfiles/filedetails/?id=2081775581)の更新版となります。本来ならSteamワークショップ上で公開・更新すべきなのですが、現在ゲームの不具合により更新が出来ない状態となっており、代替手段としてこちらで配布させて頂くこととなりました。故に、こちらの日本語訳データの適用は手動で行って頂く必要があります。ご了承下さい。
## 日本語訳について
既存の日本語訳は個人的に不自然な点、誤訳が多いと感じたので全て翻訳を見直しました。見直すにあたって、ゲームに慣れていない方向けの翻訳にしました。具体的には、カタカナ言葉を別の言葉で言い換えたり、注釈を付けたりしました。また、他の訳との整合性を合わせるために、英語の原文と全く同じ訳ではないものがあります。
## 翻訳データダウンローダーのご案内
より簡単に翻訳データをダウンロード、更新できるツールを作成、公開しました。[ここ](https://github.com/Gakuto1112/Stormworks-JapaneseTranslation-Downloader)から移動できます。現在はプレリリース段階で、他環境でも動くかどうかの確認段階中です。詳しくは[こちら](https://github.com/Gakuto1112/Stormworks-JapaneseTranslation-Downloader/blob/master/README.md)をご覧下さい。
## 日本語化の方法
### 翻訳データのダウンロード
前のファイル一覧の画面に戻り、黄緑色の「**Code**」から「**Download ZIP**」をクリックして、全てのファイルをzip圧縮したものをダウンロードできます。可能ならgitなどを使用してダウンロードしても構いません。
### 翻訳データのインストール
ダウンロードしたzipファイルの展開して、中の「**japanese.tsv**」と「**japanese.xml**」を以下のディレクトリに移動させて下さい。
```
C:\Users\user\AppData\Roaming\Stormworks\data\languages
```
* お使いの環境によって異なる場合があります。
* 「AppData」は隠しフォルダです。アドレスバーに直接打ち込むか、非表示ファイルを表示する設定にして下さい。
* 上記のディレクトリが存在しない場合は、正しい位置にご自身で作成して下さい。
### 翻訳データの適用
ゲームのメインメニューから「**Settings**」 → 「**Language**」 → 「**Japanese**」を選択して下さい。数秒程度で適用が完了します。
* リストに日本語データがない場合は「**Refresh**」を押してリストを更新して下さい。それでも表示されていない場合は正しいディレクトリに翻訳データが置かれているか確かめて下さい。
* ~~リストに警告が表示されていますが、翻訳を適用するにあたっては問題ありません。~~ （**2022/2/4更新**）警告が表示されないように修正しました。
### 翻訳データの更新
ゲームのアップデートや翻訳の修正などでの更新版がリリースされる場合があります。更新する場合は上記の手順でファイルを置き換えて下さい。また、定期的にこのページや[Steamワークショップのページ](https://steamcommunity.com/sharedfiles/filedetails/?id=2081775581)にアクセスして更新されていないか確認に来て下さい。また、更新時は[DiscordのStormworks日本サーバー](https://discord.gg/GBqesHHGBR)や[私のTwitter](https://twitter.com/Gakuto1112)でお知らせします。（Twitterは、私の個人的なツイートも含まれます。ご了承下さい。）
## 注意事項
ファイルをダウンロードした時点で以下の注意事項に同意したものとみなします。
* このデータを使用して発生したいかなる損害の責任は負いかねます。
* この翻訳データを適用してもなお、日本語に翻訳されない箇所が一部あります。これは、ゲームから翻訳データが提供されておらず、翻訳が不可能な場所です。
* この日本語訳が適用された状態で作成されたスクリーンショットや実況動画などの作品におけるクレジット表記は不要です。（表記して頂けると嬉しいですが...）
* 明らかな誤字脱字や提案がありましたら、[Steamワークショップのページ](https://steamcommunity.com/sharedfiles/filedetails/?id=2081775581)か[Issues](https://github.com/Gakuto1112/Stormworks-JapaneseTranslation/issues)で報告して下さい。（全ての希望には応えられない場合があります。）
## お願い
上記でも書きましたが、Steamワークショップで直接アップデート出来るのが本来の望ましい状態です。この不具合について[バグレポート](https://geometa.co.uk/support/stormworks/5174)を行いました。星を付与して賛同して頂けると幸いです。賛同者が多ければ（星の数が多ければ）、バグが修正される可能性が上がります。（ゲーム内からバグ報告フォームにジャンプしないと星を付与できない模様です。）


https://github.com/user-attachments/assets/21b1d462-9d98-406f-aca6-a46e9af27948
# 帰れま10アプリ

テレビ企画の帰れま10を個人で遊ぶためのアプリです
 
飲食店の商品を選択すると順位が表示されます

 
# DEMO

https://github.com/user-attachments/assets/4d03fbfe-e8db-4963-bab1-63e618d2c95e
 
# Features

ネット検索しても類似のアプリがなかったので作成しました
 
# Requirement
 
Ryeで必要なpythonパッケージと仮想環境を管理しています
 
* rye 0.1.0

 
# Installation

0.本リポジトリをクローンします
```bash
git clone https://github.com/muto-yuya/Ranking-app.git
```

1.Ryeをインストールします
 
```bash
curl -sSf https://rye.astral.sh/get | bash
```
2.プロジェクトフォルダでRyeを初期化し必要なパッケージをインストールします

```bash
cd ./flask_practice
rye init
rye sync
```

# Usage

1. 商品-順位のリストを.csvで用意します（適宜、ゲームに参加しない人が用意します）

| item_name | price | item_image | place | item_category_name |
| ---- | ---- | ---- | ---- | ---- |
| (例) 爆盛ねぎまぐろにぎり | 100 | https://www.kurasushi.co.jp/menu/upload/bf4c8baeb6e3f4cefe7a076204ae6a663f4ea93f.jpg | 1 | くら寿司 |
| (例) ふり塩熟成まぐろ | 115 | https://www.kurasushi.co.jp/menu/upload/b2cfcd6b8fc88de5d880e3dadaba4908a4ff37ca.jpg | 圏外 | くら寿司 |
| ... | ... | ... | ... | ... | 

2. 上記のcsvファイルを読み込みます
```bash
.venv/bin/python src/import_csv.py {上記で作成したcsvファイル}
```

3.  サーバーを立ち上げます
```bash
.venv/bin/python src/server.py
```

4.  ブラウザのアドレスバーにサーバーのアドレスを入力してアプリにアクセスします
```bash
http://127.0.0.1:5000/
```
5.  アプリ上でランキング名を選択して、ゲーム「開始」をクリックします

6.  商品を選択して「表示」をクリックすると順位が表示されます。表示履歴を見るには「履歴」をクリックします

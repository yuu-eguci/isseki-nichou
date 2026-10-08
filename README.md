IssekiNichou
===

コンソールゲーム。草原を歩いて、害獣を駆除して、石を拾って、コレクションブックを完成させる。

- Docker: 対応!
- Python: 3.14!
- Linter: Ruff!
- Test: pytest!

## パッと実行してみたい

```bash
docker compose run --build --rm game
```

- Docker image をビルドして (ソースの変更も反映して) 、ゲームを対話モードで起動します。
- 最初に既存データの名前を入力するとロードします。 `make 名前` と入力すると新しいデータを作ります。
- フィールドでは `w` で進む、 `s` で戻る、 `c` でメニュー、 `save` でセーブです。各画面で使えるキーは画面に表示されます。
- ゲーム内に終了コマンドはありません。 `Ctrl-C` で終了します。収集本に石を収めたとき以外は自動でセーブされないので、終了前に `save` します。
- セーブデータは Docker volume `isseki-data` の `/data/isseki.sqlite3` に残ります。初回はリポジトリの `app/isseki.sqlite3` がコピーされます。

lint 、テスト、脆弱性チェックは次のコマンドで実行します。

```bash
docker compose run --build --rm dev ruff check .
docker compose run --build --rm dev pytest
docker compose run --build --rm dev pip-audit
```

Docker を使わずにリポジトリのルートで `python3 KillBirds.py` を実行した場合は、 `app/isseki.sqlite3` を直接読み書きします。

![1](media/ISSEKI_1.jpg)

![2](media/ISSEKI_2.jpg)

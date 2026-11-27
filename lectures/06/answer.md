# 第6回 解答

## 演習

<!-- [tool call] の行は、表示された行をそのまま貼り付けてください。終わらなかった STEP は、空欄のままでかまいません。 -->

- STEP 1 のツールの名前：glossary_search_glossary
- STEP 2 の [tool call]：[tool call]   glossary_search_glossary({'query': '3レベル'})
- STEP 3 の [tool call]：[tool call]   fetch_fetch({'url': 'https://modelcontextprotocol.io/'})
- STEP 4 の [tool call]：[tool call]   aws_aws___search_documentation({'topics': ['general'], 'search_phrase': 'Amazon S3 バージョニング'})
[tool call]   aws_aws___search_documentation({'topics': ['general'], 'search_phrase': 'What is versioning in Amazon S3'})
- 気づき・疑問：「fetch」はコンテナー内でコマンドから起動し、AWSのサーバーにはURLで接続することが、一覧の表示から分かった。AWSの検索では、最初に日本語で検索し、次に英語に言い換えて再検索していた。呼び出しログと戻り値を見比べると、どんな検索語で、どの資料が見つかったかまで確認できた。

## 宿題

<!-- 基礎・実装・発展のどれか1つに取り組めば完了です。 -->

- 取り組んだレベル：基礎 / 実装 / 発展
- やったこと：app/mcp_server.py に get_lecture_summary の公開を1行追加した。
- 結果：「glossary_get_lecture_summary」が追加され、ツールが2個になった。「第2回では何を学びますか？」と質問すると、[tool call]   glossary_get_lecture_summary({'lecture': 2}) と表示され、ツールから第2回「ファインチューニングとLoRA」の要点が返った。テスト結果は 24 passed in 24.12s で、24件すべてに合格した。
- 気づき・疑問：サーバー側でツールの公開を1行追加するだけで、エージェントが使えるツールが増えることが分かった。一覧にはツール名のほか、引数lectureが整数であることも表示されていた。呼び出しログを見ると、質問文の「第2回」が実際にlecture:2として渡されていることを確認できた。

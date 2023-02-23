## 受講生の確認事項

- [ ] 画面をブラウザで実際に開いてテスト要件の[画面と機能](https://docs.google.com/spreadsheets/d/1tUi2xkohBzXZySmKDYruRruvlOmUV6bJK_GExeG5Tsw/edit#gid=1308498917)の動作確認をした（動作が分からない場合講師からスクリーンショットの提出を求めることがあります）
- [ ] Django Admin に，今まで作成したモデルを全て登録した
- [ ] テスト要件のテストを全て実装した
- [ ] CI が全て通った

## １次レビュアーの確認事項

### 共通事項

- [ ] [確認済み](https://www.notion.so/shinonome-inc/2766e814139041fd85b27d9689b28bf4?pvs=4#b85a183fe0654b80bb0e04ebb7da52cd)

### ツイート機能

- templates
  - [ ] tweets フォルダの中にツイート作成の html, ツイート詳細画面の html, ツイート削除の html がある
  - [ ] tweets フォルダのホーム表示の html では、ツイート一覧表示処理が記載されている
  - [ ] accounts フォルダのプロフィール表示の html では、そのユーザーに紐づくツイートが表示される処理が記載されている
- tweets/models.py

  - [ ] Tweet のモデルを作成している
  - [ ] フィールドに User との外部リレーション、文章のフィールド、作成日時のフィールドが最低でもある。
        文章のフィールドは max_length が指定できていれば CharField でも TextField でもどちらでも良い。どちらにもメリットデメリットがあるので受講生側に任せる。
  - [ ] User の外部リレーションの実装を満たす。[参考](https://www.notion.so/shinonome-inc/2766e814139041fd85b27d9689b28bf4?pvs=4#f65fa5ede4f24d8494975cc15f1bb50c)
  - [ ] 作成日時のフィールド名に関して、DateTimeField を使う場合は suffix が`_at`という命名にすることを推奨とする。

    [参考](https://blog.pinkumohikan.com/entry/date-and-datetime-column-suffix-on-db)

- tweets/admin.py
  - [ ] admin.site.register に Tweet のモデルを入れている
- tweets/forms.py
  - [ ] 必ずしも作成する必要はないが、作成している場合は文章のフィールドを fields につけてカスタマイズしている。
        ただ fields に文章のフィールドしかない場合は forms.py に記載する必要ない。views.py の方に記載してもらえれば OK。
        カスタマイズ例は、widgets をカスタマイズしているなどが考えられる。文章フィールドを CharField にしてる場合は基本的に widgets はカスタマイズした方が良いと思われるが強制はしない。
- tweets/urls.py
  - [ ] エンドポイントが`create/`で、ツイート作成のビューが呼ばれている
  - [ ] エンドポイントが`<int:pk>/`で、ツイート詳細のビューが呼ばれている
  - [ ] エンドポイントが`<int:pk>/delete/`で、ツイート削除のビューが呼ばれている
- tweets/views.py

  - [ ] ツイート作成のビュー、ツイート詳細のビュー、ツイート削除のビューがある
  - [ ] ツイート作成のビューでは、ログインユーザーが作成者となる処理を書いてる（CreateView を使っている場合、上記処理は form_valid()で記述。ユーザー作成時とは異なり、super().form_valid(form)を先に呼ぶ必要はないし、先に書いていたとしても別に OK）
  - [ ] ツイート削除のビューでは、作成者だけしか削除できないようにしている

    - UserPassesTestMixin を用いてる場合

      DeleteView と UserPassesTestMixin を用いてる場合、self.get_object()から取ってくる。そうすることでいちいちクエリ処理書く必要なくなる。ただし、同じ SQL を 2 回叩くことになってしまうというトレードオフがある。

      ```python
      def test_func(self):
      	tweet = self.get_object() # test_funcの段階でget_object実行されないのでここで実行させている。すなわちself.objectは取ってこれない。なので無駄に同じSQLを1つ叩くことになってしまう。
      	return self.request.user == tweet.user

      # 以下はN+1に関する注意

      # パターン1
      # Userをjoinしている場合
      queryset = Tweet.objects.select_related("user")

      # joinしてるので以下の2つのパフォーマンスは変わらない
      # 1. Tweetモデルのフィールドだけを参照
      def test_func(self):
      	tweet = self.get_object()
      	return self.request.user == tweet.user
      # 2. TweetモデルではなくUserモデルのフィールドを参照。joinしてるのでN+1は起きない
      def test_func(self):
      	tweet = self.get_object()
      	return self.request.user.username == tweet.user.username

      # パターン2
      # Userをjoinしてない場合
      model = Tweet

      # 1. Tweetモデルのフィールドだけを参照
      def test_func(self):
      	tweet = self.get_object()
      	return self.request.user == tweet.user

      # 2. TweetモデルではなくUserモデルのフィールドを参照。joinしてないのでN+1が起きる
      def test_func(self):
      	tweet = self.get_object()
      	return self.request.user == tweet.user.username
      ```

  - [ ] ホームビューでツイート一覧表示ができている
  - [ ] HomeView と UserProfileView で，N+1 問題が発生していない

    - N+1 解決方法

      ツイート一覧表示してユーザーネームも表示している場合は Tweet モデルと User モデルを join しないと N+1 が起きる。select_related を用いるなどして N+1 の対応ができているかチェック。
      （ちなみに上記と同じ理由で TweetDetailView, TweetDeleteView も N+1 起きるので User の join 必要ではあるが、1 つのデータでしかないので無理に N+1 を解決してもらう必要はない）

      - とりあえず簡易的に SQL を見せるなら，以下のリンクの設定がおすすめ。ユーザー情報を取得する同じような `SELECT` が投稿の数発生しているのに気づいてもらう

        [Django で Model 経由で実行した SQL をログに出力する - Qiita](https://qiita.com/fumihiko-hidaka/items/0f619749580da5ad9ce5)

      - django-debug-toolbar を使用してもらうのもアリ
      - 必要に応じて以下を投げてもらっても良いかも

        [Django を使うときに知っておきたい DB の基礎知識と N+1 問題](https://blog.shinonome.io/sql-django-n-plus-1/)

- accounts/views.py
  - [ ] プロフィールビューで、エンドポイントの username と一致するユーザーのツイートが表示される処理が書かれている
- tweets/tests.py
  - [ ] [最終課題テスト項目要件を満たす](https://docs.google.com/spreadsheets/d/1tUi2xkohBzXZySmKDYruRruvlOmUV6bJK_GExeG5Tsw/edit#gid=842149650)
    - `self.client.login` が適切，などは無いので `force_login` でもどちらでも良い！！
- accounts/tests.py
  - [ ] プロフィールビューで追記したツイート表示のテストを書いている
    - `self.client.login` が適切，などは無いので `force_login` でもどちらでも OK

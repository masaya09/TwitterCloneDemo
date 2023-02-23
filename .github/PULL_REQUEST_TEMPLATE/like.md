## 受講生の確認事項

- [ ] 画面をブラウザで実際に開いてテスト要件の[画面と機能](https://docs.google.com/spreadsheets/d/1tUi2xkohBzXZySmKDYruRruvlOmUV6bJK_GExeG5Tsw/edit#gid=1308498917)の動作確認をした（動作が分からない場合講師からスクリーンショットの提出を求めることがあります）
- [ ] Django Admin に，今まで作成したモデルを全て登録した
- [ ] テスト要件のテストを全て実装した
- [ ] CI が全て通った

## １次レビュアーの確認事項

### 共通事項

- [ ] [確認済み](https://www.notion.so/shinonome-inc/2766e814139041fd85b27d9689b28bf4?pvs=4#b85a183fe0654b80bb0e04ebb7da52cd)

### いいね機能

- templates
  - [ ] ホーム画面とプロフィール画面の各ツイートにいいね・いいね取り消しボタンがある
    - [ ] ホーム画面とプロフィール画面に実装するので、いいねのところは抜き出して like.html とし、include して表示する実装にしていること
    - [ ] いいねされているか見た目で分かるようにしている
  - [ ] ホーム画面・プロフィール画面の各ツイートとツイート詳細画面にいいね数を表示している
  - [ ] いいね画面・いいね解除画面のテンプレートが作られていない
  - [ ] いいね・いいね取り消しに Ajax の FetchAPI を使っている
    - JavaScript 部分は static 以下に分けても良い
    - [ ] CSRF Token を使っている
      - 参考：[https://docs.djangoproject.com/en/4.1/howto/csrf/](https://docs.djangoproject.com/en/4.1/howto/csrf/)
    - [ ] いいねされているかの情報を DOM を操作して切り替えている
      - form や a タグを用いると，画面全体の再読み込みを伴うため，JavaScript 経由で書く必要がある
- tweets/models.py

  - [ ] `Like` モデルを作っている

    - [ ] User と Tweet を ManyToMany で繋ぐという実装もある。こちらでも可
          実装例

          ```python
          class Tweet(models.Model):
          	# ...中略
          		liked_by = models.ManyToManyField(
          	      settings.AUTH_USER_MODEL,
          	      related_name="liking",
          	  )
          ```

    - [ ] フィールドには外部キーとして `User` と `Tweet` を持っている
      - [ ] `UniqueConstraint` で `User` と `Tweet` の組み合わせをユニークにしている
        - View でいいねを重複しないようにしているが，DB でも制約をかけて追加できないようにした方が良いため

- tweets/admin.py
  - [ ] `Like` モデルを Admin に登録している
- tweets/urls.py
  - [ ] エンドポイントが `<int:pk>/like/` で， `LikeView` が呼ばれている
  - [ ] エンドポイントが `<int:pk>/unlike/` で， `UnlikeView` が呼ばれている
- tweets/views.py
  - [ ] いいね・いいね取り消しの View がある
    - [ ] テンプレートは不要なので TemplateView などは使わない（View を継承する）
    - [ ] POST を使っている
    - [ ] ツイートが存在しなかったら 404 を返す
  - [ ] `TweetDetailView` で context にいいね数を格納している
    - [ ] N+1 問題が発生していない
    - [ ] クラスベースの場合は `get_context_data` を使っている
      - [ ] ＜上級者向け＞[https://github.com/shinonome-inc/2022_summer_hackathon_E/blob/044b413f2aeb9f40e8ee7d7f02f09d99d1c905bf/backend/api-django/posts/views.py#L26](https://github.com/shinonome-inc/2022_summer_hackathon_E/blob/044b413f2aeb9f40e8ee7d7f02f09d99d1c905bf/backend/api-django/posts/views.py#L26) のように `annotate` を使って QuerySet で渡すこともできる
  - [ ] `HomeView` で各ツイートがいいねされているかの情報を context に渡している
    - [ ] この際 N+1 問題が発生していない
    - [ ] ＜上級者向け＞[https://github.com/shinonome-inc/2022_summer_hackathon_E/blob/044b413f2aeb9f40e8ee7d7f02f09d99d1c905bf/backend/api-django/posts/views.py#L26](https://github.com/shinonome-inc/2022_summer_hackathon_E/blob/044b413f2aeb9f40e8ee7d7f02f09d99d1c905bf/backend/api-django/posts/views.py#L26) のように `annotate` を使って QuerySet で渡すこともできる
- accounts/views.py
  - [ ] `UserProfileView` で各ツイートがいいねされているかの情報を context に渡している
    - [ ] この際 N+1 問題が発生していない
- tweets/tests.py
  - [ ] [いいね機能のテスト仕様](https://docs.google.com/spreadsheets/d/1tUi2xkohBzXZySmKDYruRruvlOmUV6bJK_GExeG5Tsw/edit#gid=365041756)を満たす
    - `self.client.login` が適切，などは無いので `force_login` でもどちらでも OK

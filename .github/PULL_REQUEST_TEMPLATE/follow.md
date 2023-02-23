## 受講生の確認事項

- [ ] 画面をブラウザで実際に開いてテスト要件の[画面と機能](https://docs.google.com/spreadsheets/d/1tUi2xkohBzXZySmKDYruRruvlOmUV6bJK_GExeG5Tsw/edit#gid=1308498917)の動作確認をした（動作が分からない場合講師からスクリーンショットの提出を求めることがあります）
- [ ] Django Admin に，今まで作成したモデルを全て登録した
- [ ] テスト要件のテストを全て実装した
- [ ] CI が全て通った

## １次レビュアーの確認事項

### 共通事項

- [ ] [確認済み](https://www.notion.so/shinonome-inc/2766e814139041fd85b27d9689b28bf4?pvs=4#b85a183fe0654b80bb0e04ebb7da52cd)

### フォロー機能

- templates
  - [ ] accounts フォルダの中に，新たにフォローリスト・フォロワーリストを表示する html がある
  - [ ] フォロー画面・フォロー解除画面の html **が作られていない**
    - POST で直接操作するため，a タグを使うのは不適切
    - form を使ってメソッドを POST とし submit ボタンを押すことで実行されるようにする方法がある
  - [ ] 各 html は，base.html を適切に `extends` している
  - [ ] プロフィールの html に，フォロー/フォロー解除ボタン・フォロー数・フォロワー数を追加している
    - [ ] フォローボタンをクリックすると，フォローされ Home にリダイレクトする
    - [ ] フォロー解除ボタンをクリックすると，フォロー解除され Home にリダイレクトする
    - [ ] 人数の部分をクリックすると，フォローリスト・フォロワーリストに遷移するようになっている
- accounts/models.py [ユーザー同士の多対多の接続](https://www.notion.so/42a3c92536e2458a9ee71a2d2629c9e6) 参照
  - [ ] `FriendShip`のモデルを作成している
    - [ ] `ManyToMany` で作成する場合は，作成日時 sort に `created_at` を加える必要がある故 through を用いて明示的に接続する必要がある →[上級者向けの説明](https://www.notion.so/c4c4c4bf7a48422b85125b416e03494c)へ
  - [ ] フィールドには，User との外部リレーションとして， `followee` と `follower` が作成されていて，かつ `created_at` も作成されている
    - [ ] 命名がわかりにくくない
  - [ ] `UniqueConstraint` でユニーク制約を付与している
    - `unique_together` は[deprecated](https://docs.djangoproject.com/en/4.1/ref/models/options/#unique-together)なので注意！
  - [ ] ＜上級者向け＞ User モデルに，中間モデルを `FriendShip` として（ `through` を用いる），ManyToMany で接続している
    - [以下，発展的内容（ `ManyToMany` と `through` で明示的に `User` から繋げる）](https://www.notion.so/ManyToMany-through-User-c9b3a8fe51b149a5816a8a579a11da47) 参照
- migrations
  - [ ] 今までの migration ファイルを削除したり編集したりしていない（たくさん追加している分には問題ない）
    - わざわざまとめさせる必要は無いが，10 個とか生成されていたら，さすがに多すぎるのでまとめさせるのもアリ
- accounts/admin.py
  - [ ] `FriendShip`モデルを Admin に登録している
- accounts/urls.py
  - [ ] エンドポイントが`<str:username>/`で，プロフィールの View が呼ばれている
  - [ ] エンドポイントが`<str:username>/follow/`で，Follow の View が呼ばれている
  - [ ] エンドポイントが`<str:username>/unfollow/`で，Unfollow の View が呼ばれている
  - [ ] エンドポイントが`<str:username>/following_list/`で，フォローリストの View が呼ばれている
  - [ ] エンドポイントが`<str:username>/follower_list/`で，フォロワーリストの View が呼ばれている
- accounts/views.py

  - [ ] プロフィールに加え，フォロー・フォロー解除・フォローリスト・フォロワーリストの View がある
  - [ ] ProfileView で，context に following/follower カウント・follow しているかしていないかのフラグを含め，template で描画ができている
  - [ ] FollowView・UnFollowView で， `View` を継承して， `post` メソッドに処理を書いている

    - [ ] [フォロー機能のテスト仕様](https://docs.google.com/spreadsheets/d/1tUi2xkohBzXZySmKDYruRruvlOmUV6bJK_GExeG5Tsw/edit#gid=128988789)に従い主に 3 つのバリデーションを記述している
      1.  `get_object_or_404` などによる，url から受け取った user の存在チェック
          - `django.contrib.messages` を表示したいなら，exists を使ってチェック →add_message→Http404 みたいな処理を書いても良い
      2.  自分自身を扱おうとしたときは 400 を返すチェック
      3.  正常時は 302，tweets:home にリダイレクト
          - 既にフォローしている/フォローしていない系の表示は， `django.contrib.messages` などで伝えてあげても良いが，特段の規定はしない。この処理を書くときは， `get_or_create` などを活用できると good
    - [ ] 適切にアーリーリターンを行い，if 文の 2 重ネストなどが起こっていない
    - [ ] 画面が存在しないため， `TemplateView` は使わず， `django.contrib.messages` を用いて message を加えたうえでリダイレクトしている
          →`template_name` や `model` などの使用されないクラス変数を作成していない - [ ] `django.contrib.messages` を使ってメッセージを入れたら， `base.html` に [message 表示の設定](https://docs.djangoproject.com/en/4.1/ref/contrib/messages/#displaying-messages)を忘れないように記述する
    - [ ] `render`を使って `home.html` などを呼び出すのは基本アウト。画面が存在しない+context を適切に作っていない場合・適切なステータスコードを返していない場合が多いため。
    - [ ] `RedirectView` を使う場合

      - <大前提>どちらかというと動的にリダイレクト先を変更するのに特化した View であり，無理して使用する必要は無い
      - 使用する場合

        - [ ] 最後の `return` では，親の `post` を呼び出している（RedirectView 内で全て結局 get が呼ばれているが，混乱を招かないためにも，あくまで自分の書いている親メソッドを呼ぶ）

          ```python
          class FollowView(LoginRequiredMixin, generic.RedirectView):
              url = reverse_lazy("tweets:home")
              http_method_names = ["post"]

              def post(self, request, *args, **kwargs):
                  # 処理
                  return super().post(request, *args, **kwargs)
                  # super().get(...)ではない！！（同義だがわかりづらい）
          ```

    - 超上級者は， `FormView` を使って `form_valid` を override するなどして実装するのもｱﾘ（その場合は form の作成が必要）

  - [ ] FollowingListView と FollowerListView で適切な View を用いて，**フォロー・被フォローの新しい順で**フォロー・フォロワー一覧を返す view を作成している（以下，方法の例を列挙する）
    - `TemplateView` を使用し，context にフォロー・フォロワーリストを含める
    - `ListView` を使用し， `get_queryset` で絞り込む（一番スマート）
  - [ ] FollowingListView と FollowerListView で，N+1 問題が発生していない
    - `FriendShip` モデルから参照するときは `select_related` を単純に用いれば問題ない
    - <上級者向け> `User` から直接引っ張るときは，対多を引っ張るため， `prefetch_related` を使用する必要があることに注意
  - [ ] ごくまれに， `try` 節を例外が起こるはずのない箇所にまで広げた実装をする例があるが， `try` でくくるのは例外が発生する可能性のある 1 行だけ

    - 例

    ```python
    try:
        # ここや
        follower = User.objects.get(username=self.kwargs["username"])
        # ここに処理を書かない！！（どこでエラー起こるのかわかりにくく混乱する）
    except User.DoesNotExist:
        raise Http404
    ```

- accounts/tests.py
  - [ ] [フォロー機能のテスト仕様](https://docs.google.com/spreadsheets/d/1tUi2xkohBzXZySmKDYruRruvlOmUV6bJK_GExeG5Tsw/edit#gid=128988789)を満たす
    - `self.client.login` が適切，などは無いので `force_login` でもどちらでも OK

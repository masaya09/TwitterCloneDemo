## 受講生の確認事項

- [ ] 画面をブラウザで実際に開いてテスト要件の[画面と機能](https://docs.google.com/spreadsheets/d/1tUi2xkohBzXZySmKDYruRruvlOmUV6bJK_GExeG5Tsw/edit#gid=1308498917)の動作確認をした（動作が分からない場合講師からスクリーンショットの提出を求めることがあります）
- [ ] Django Admin に，今まで作成したモデルを全て登録した
- [ ] テスト要件のテストを全て実装した
- [ ] CI が全て通った

## １次レビュアーの確認事項

### 共通事項

- [ ] [確認済み](https://www.notion.so/shinonome-inc/2766e814139041fd85b27d9689b28bf4?pvs=4#b85a183fe0654b80bb0e04ebb7da52cd)

### ログイン・ログアウト機能

- mysite/settings.py
  - [ ] LOGIN_URL, LOGIN_REDIRECT_URL, LOGOUT_URL の記載がある
  - [ ] tweets/home のような記載ではなく、”tweets:home”のように記載してある
  - [ ] LOGIN_REDIRECT_URL を tweets:home としている
- templates
  - [ ] accounts フォルダの中にログイン画面の html がある
  - [ ] accounts フォルダの中にユーザープロフィール画面の html がある
  - [ ] base.html を継承し、ブロックの記述も適切である。
  - [ ] form の表示と csrf_token のタグがある。
  - [ ] bootstrap のバージョンは 5 であること。3 とか 4 使っている場合は 5 に変更する。
- accounts/urls.py
  - [ ] エンドポイントが `login/` で、LoginView が呼ばれている
  - [ ] エンドポイントが `logout/` で、LogoutView が呼ばれている
  - [ ] エンドポイントが `<str:username>/` で、UserProfileView が呼ばれている
  - views.py に LoginView, LogoutView を記述せずに urls.py に記載する場合は、以下のようにする。（基本こちらを推奨）
    - [ ] `from django.contrib.auth import views as auth_views` から import して LoginView, LogoutView を使っていること。（`from django.contrib.auth.views import LoginView, LogoutView`でも OK）
    - [ ] LoginView はテンプレート必要、LogoutView はテンプレート不要なので、LoginView の as_view()メソッドの引数に template_name が記述されている。
- accounts/views.py

  - [ ] サインアップ時のリダイレクト先を LOGIN_REDIRECT_URL にしている。
  - [ ] settings モジュールは、`from django.conf import settings`から import していること。`from mysite import settings`は不可
    - settings.py を分割しても推奨方法であればコード変更不要。
  - [ ] UserProfileView を作成している。Profile モデルは不要。User モデルの詳細画面表示ができていれば OK。
  - views.py に LoginView, LogoutView を記述している場合

    - [ ] import した LoginView と LogoutView と名称が被っていない。

      ```python
      # Bad
      from django.contrib.auth views import LoginView
      class LoginView(LoginView):

      # OK
      from django.contrib.auth import views as auth_views
      class LoginView(auth_views.LoginView):
      ```

    - [ ] LoginView はテンプレート必要、LogoutView はテンプレート不要
    - [ ] LogoutView に LoginRequiredMixin を付ける必要はない（あってもいいが必須ではない）

- accounts/forms.py
  - [ ] 記載する必要ない。もしカスタマイズする際は AuthenticationForm を継承すること。override してる意味のない記述は削除すること
- accounts/tests.py
  - [ ] [最終課題テスト項目要件を満たす](https://docs.google.com/spreadsheets/d/1tUi2xkohBzXZySmKDYruRruvlOmUV6bJK_GExeG5Tsw/edit#gid=842149650)
  - [ ] TestLoginView の setUp で、User.objects.create_user を用いてユーザーを作成している。
  - [ ] TestLogoutView の setUp で、User.objects.create_user を用いてユーザーを作成し、self.client.login または self.client.force_login でログイン処理させている
    - `self.client.login` が適切，などは無いのでどちらでも OK

## 受講生の確認事項

- [ ] 画面をブラウザで実際に開いてテスト要件の[画面と機能](https://docs.google.com/spreadsheets/d/1tUi2xkohBzXZySmKDYruRruvlOmUV6bJK_GExeG5Tsw/edit#gid=1308498917)の動作確認をした（動作が分からない場合講師からスクリーンショットの提出を求めることがあります）
- [ ] Django Admin に，今まで作成したモデルを全て登録した
- [ ] テスト要件のテストを全て実装した
- [ ] CI が全て通った

## １次レビュアーの確認事項

### 共通事項

- [ ] [確認済み](https://www.notion.so/shinonome-inc/2766e814139041fd85b27d9689b28bf4?pvs=4#b85a183fe0654b80bb0e04ebb7da52cd)

### サインアップ機能

- mysite/settings.py
  - [ ] TEMPLATES の DIRS の値が pathlib で `[ BASE_DIR / “templates” ]` と書かれている。os.path.join は使わない。
    - `/` ではなく `,` を使用して区切らない。データベースの設定で `BASE_DIR / "db.sqlite3"` となっていることからここに倣って β 統一
  - [ ] AUTH_USER_MODEL の記述あり
- templates

  - [ ] bootstrap のバージョンは 5 であること。3 とか 4 使っている場合は 5 に変更する。
  - [ ] 階層構造が次のようになっている

    ```
    accounts
    mysite
    templates
    	- accounts
    		- signup.html ← 命名はなるべくview名と合わせること
    	- tweets
    		- home.html
    	- welcome
    		- welcome.html
    	- base.html
    tweets
    welcome
    ```

  - [ ] template の継承機能を使っている（base.html を継承して作っている）ブロックの記述も適切である。
  - [ ] サインアップの画面にて form を表示できている。csrf_token のタグを書いている。

- accounts/models.py

  - [ ] AbstractUser を継承している
  - [ ] email フィールドを上書いて、blank=False にしている

    ```python
    # Bad
    class User(AbstractUser):
    	email = models.EmailField(max_length=254, blank=False)

    # OK
    class User(AbstractUser):
    	email = models.EmailField()

    class User(AbstractUser):
    	email = models.EmailField(max_length=150) # defaultの254でなければOK。
    ```

- accounts/admin.py
  - [ ] User を登録している
  - [ ] admin.site.register(User)としていれば OK
  - [ ] もし、カスタマイズする場合は`from django.contrib.auth.admin import UserAdmin`を用いてカスタマイズしていること。すなわち User の場合 admin.ModelAdmin よりは UserAdmin を用いることを推奨。
- accounts/forms.py
  - [ ] username と email および password を 2 回入力するフォームがある
  - UserCreationForm を継承している場合
    - [ ] Meta クラスの fields において、password1, password2 は不要とする
  - UserCreationForm を継承していない場合
    - プログラミング未経験者だと判断できた場合
      - [ ] UserCreationForm を継承するように伝える
    - プログラミング経験者だと判断できた場合
      - [ ] ModelForm を継承している
      - [ ] save メソッドや clean メソッドなど何も書かずに PR 出していた場合、UserCreationForm を継承するように伝える
      - [ ] validate_password 関数を使って password のバリデーションができている
      - [ ] 2 つの password が一致するかのバリデーション処理がきちんとできている
      - [ ] save メソッドをオーバーライドし、set_password メソッドを使ってハッシュ化してから save している
- accounts/views.py
  - [ ] ユーザー作成ができている
  - [ ] 適切にフォームのバリデーション処理を行っている
  - [ ] クラスベースビューの場合、`response = super().form_valid(form)`を form_valid()の最初に呼んでいる。[ユーザー作成時にログイン処理行う際は super().form_valid(form)を先に呼ばなければいけない理由](https://www.notion.so/django-signup-super-form_valid-form-80347478b20244ecb68366922ca0272c)
  - [ ] ユーザー作成時にログイン処理が行われている
  - [ ] authenticate 関数を使っており、その際 username と password を cleaned_data から取ってこれている。もし authenticate の引数で email=~としている場合、デフォルトの状態では意味ないので不要。カスタマイズしてればあっているか要確認。難しかったら 2 次レビュアーに任せて OK。
  - [ ] login 関数を使っている
  - [ ] リダイレクト先が、tweets/home/ になっている。その際、url の指定は reverse(success_url の場合は reverse_lazy)を用いて逆引きしていること。
- accounts/urls.py
  - [ ] エンドポイントが `signup/` で、SignupView を呼び出す path が記述されている
- accounts/tests.py

  - [ ] TestSignupView という命名でテストしている
  - [ ] 複数使う項目をきちんと setUp に統一している（ex: url など）
  - [ ] [最終課題テスト項目要件を満たす](https://docs.google.com/spreadsheets/d/1tUi2xkohBzXZySmKDYruRruvlOmUV6bJK_GExeG5Tsw/edit#gid=842149650)
  - [ ] form のバリデーションテストの際は assertFormError を使わずに、`response.context[”form”]`から form エラーを確認している

    - 補足

      form を view から引っ張ってこずに，新たにインスタンス化している人がたまにいるため
      form をインスタンス化するくらいなら，view と form のテストを分離すべき，となっちゃうけど最終課題ではそこまでしなくて良い

  - [ ] assertIn を用いている場合、string in string の形になっていないこと。assertIn を使う場合は string in list<string>の形式にする。

- tweets/views.py
  - [ ] HomeView を作成している
- tweets/urls.py
  - [ ] エンドポイントが `home/` で、HomeView を呼び出す path が記述されている
- tweets/tests.py
  - [ ] TestHomeView という命名で test している

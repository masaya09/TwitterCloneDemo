## SQL

#### session チェック

```python
# django/contrib/sessions/backends/db.py in _get_session_from_db(32)
self.model.objects.get(
  session_key=self.session_key, expire_date__gt=timezone.now()
)
```

```SQL
SELECT django_session.session_key, django_session.session_data, django_session.expire_date
FROM django_session
WHERE (django_session.expire_date > 'yyyy-mm-dd hh:mm:ss.000000'
  AND django_session.session_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
LIMIT 21
```

#### request.user

```python
# django/contrib/auth/backends.py in get_user(158)
user = UserModel._default_manager.get(pk=user_id)
```

```SQL
SELECT users.id, users.password, users.last_login, users.is_superuser, users.username, users.email, users.slug, users.is_staff, users.is_active
FROM users
WHERE users.id = 1
LIMIT 21
```

## SignUpView

#### 通常時（クエリ 11 ）

```SQL
SELECT (1) AS a FROM users WHERE users.username = 'TESTER7' LIMIT 1
SELECT (1) AS a FROM users WHERE users.email = 'tester7@test.com' LIMIT 1
INSERT INTO users (password,  last_login,  is_superuser,  username,  email,  slug,  is_staff,  is_active) SELECT 'pbkdf2_sha256$xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  NULL,  0,  'TESTER7',  'tester7@test.com',  'tester7',  0,  1 RETURNING users.id
INSERT INTO profile (user_id,  bio) SELECT 7,  '' RETURNING profile.id
SELECT users.id,  users.password,  users.last_login,  users.is_superuser,  users.username,  users.email,  users.slug,  users.is_staff, users.is_active FROM users WHERE users.email = 'tester7@test.com' LIMIT 21
SELECT (1) AS a FROM django_session WHERE django_session.session_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' LIMIT 1
BEGIN
INSERT INTO django_session (session_key, session_data, expire_date) SELECT 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'yyyy-mm-dd hh:mm:ss.000000'
UPDATE users SET last_login = 'yyyy-mm-dd hh:mm:ss.000000' WHERE users.id = 7
BEGIN
UPDATE django_session SET session_data = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', expire_date = 'yyyy-mm-dd hh:mm:ss.000000' WHERE django_session.session_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
```

#### クエリ 12 個発生した時

```SQL
SELECT (1) AS a FROM users WHERE users.username = 'tester5' LIMIT 1
SELECT (1) AS a FROM users WHERE users.email = 'tester5@test.com' LIMIT 1
INSERT INTO users (password, last_login, is_superuser, username, email, slug, is_staff, is_active) SELECT 'pbkdf2_sha256$xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', NULL, 0, 'tester5', 'tester5@test.com', 'tester5', 0, 1 RETURNING users.id
INSERT INTO profile (user_id,  bio) SELECT 5, '' RETURNING profile.id
SELECT users.id, users.password, users.last_login, users.is_superuser, users.username, users.email, users.slug, users.is_staff, users.is_active, FROM users WHERE users.email = 'tester5@test.com' LIMIT 21

SELECT django_session.session_key, django_session.session_data, django_session.expire_date FROM django_session WHERE (django_session.expire_date > 'yyyy-mm-dd hh:mm:ss.000000' AND django_session.session_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx') LIMIT 21
SELECT django_session.session_key, django_session.session_data, django_session.expire_date FROM django_session WHERE django_session.session_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' LIMIT 21
DELETE FROM django_session WHERE django_session.session_key IN ('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

UPDATE users SET last_login = 'yyyy-mm-dd hh:mm:ss.000000' WHERE users.id = 5

SELECT (1) AS a FROM django_session WHERE django_session.session_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' LIMIT 1
BEGIN
INSERT INTO django_session (session_key,  session_data,  expire_date)SELECT 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'yyyy-mm-dd hh:mm:ss.000000'
```

# Accounts

## ProfileView

```python
User.objects.filter(slug=self.kwargs["slug"])
    .select_related("profile")
    .annotate(
        tweet_num=Count("tweets", distinct=True),
        following_num=Count("followers", distinct=True),
        follower_num=Count("following_users", distinct=True),
    )
```

```SQL
SELECT users.id, users.password, users.last_login, users.is_superuser, users.username, users.email, users.slug, users.is_staff, users.is_active,
       COUNT(DISTINCT tweets.id) AS tweet_num,
       COUNT(DISTINCT friendship.id) AS following_num,
       COUNT(DISTINCT T4.id) AS follower_num,
       profile.id, profile.user_id, profile.bio
FROM users
LEFT OUTER JOIN tweets ON (users.id = tweets.user_id) LEFT OUTER JOIN friendship ON (users.id = friendship.follower_id)
LEFT OUTER JOIN friendship T4 ON (users.id = T4.following_id)
LEFT OUTER JOIN profile ON (users.id = profile.user_id)
WHERE (users.slug = 'tester' AND users.slug = 'tester')
GROUP BY users.id, users.password, users.last_login, users.is_superuser, users.username, users.email, users.slug, users.is_staff, users.is_active,
         profile.id, profile.user_id, profile.bio
LIMIT 21
```

```python
FriendShip.objects.filter(
    following=self.object, follower=self.request.user
).exists()
```

```SQL
SELECT (1) AS a
FROM friendship
WHERE (friendship.follower_id = 3 AND friendship.following_id = 1)
LIMIT 1
```

```python
self.object.tweets.prefetch_related("likes").all()
{% for tweet in tweets %}
```

```SQL
SELECT tweets.id, tweets.content, tweets.user_id, tweets.created_at
FROM tweets
WHERE tweets.user_id = 1
ORDER BY tweets.created_at DESC
```

```python
Like.objects.filter(user=self.request.user).values_list(
    "tweet", flat=True
)
{% for tweet in tweets %}
```

```SQL
SELECT like.id, like.tweet_id, like.user_id
FROM like
WHERE like.tweet_id IN (10,  1)
```

```python
{% tweet.id in liked_list %}
```

```SQL
SELECT like.tweet_id
FROM like
WHERE like.user_id = 3
```

```python
get_object_or_404(User, slug=kwargs["slug"])
```

```SQL
SELECT users.id, users.password, users.last_login, users.is_superuser, users.username, users.email, users.slug, users.is_staff, users.is_active
FROM users
WHERE users.slug = 'tester4'
LIMIT 21
```

```python
FriendShip.objects.filter(follower=follower, following=following).exists()
```

```SQL
SELECT (1) AS a
FROM friendship
WHERE (friendship.follower_id = 3 AND friendship.following_id = 4)
LIMIT 1
```

```python
FriendShip(follower=follower, following=following).save()
```

```SQL
INSERT INTO friendship (following_id,  follower_id)
SELECT 4, 3
RETURNING friendship.id
```

## ProfileEditView

```SQL
SELECT users.id,  users.password,  users.last_login,  users.is_superuser,  users.username,  users.email,  users.slug,  users.is_staff,  users.is_active,  profile.id,  profile.user_id,  profile.bio
FROM users
LEFT OUTER JOIN profile ON (users.id = profile.user_id)
WHERE users.slug = 'tester7'
LIMIT 21

UPDATE profile SET user_id = 7,  bio = 'Hi' WHERE profile.id = 7
```

## FollowView

```SQL
SELECT users.id,  users.password,  users.last_login,  users.is_superuser,  users.username,  users.email,  users.slug,  users.is_staff,  users.is_active
FROM users
WHERE users.slug = 'tester'
LIMIT 21

SELECT (1) AS a
FROM friendship
WHERE (friendship.follower_id = 7
  AND friendship.following_id = 1)
LIMIT 1

INSERT INTO friendship (following_id,  follower_id) SELECT 1,  7 RETURNING friendship.id
```

## UnFollowView

```SQL
SELECT users.id,  users.password,  users.last_login,  users.is_superuser,  users.username,  users.email,  users.slug,  users.is_staff,  users.is_active
FROM users
WHERE users.slug = 'tester'
LIMIT 21

SELECT (1) AS a
FROM friendship
WHERE (friendship.follower_id = 7
  AND friendship.following_id = 1)
LIMIT 1

BEGIN

DELETE FROM friendship
WHERE (friendship.follower_id = 7
  AND friendship.following_id = 1)
```

## FollowingListView

```python
get_object()
```

```SQL
SELECT users.id,  users.password,  users.last_login,  users.is_superuser,  users.username,  users.email,  users.slug,  users.is_staff,  users.is_active
FROM users
WHERE users.slug = 'tester3'
LIMIT 21
```

```python
following_users = FriendShip.objects.filter(follower=self.object).values_list(
    "following"
)
User.objects.filter(id__in=following_users)
```

```SQL
SELECT users.id,  users.password,  users.last_login,  users.is_superuser,  users.username,  users.email,  users.slug,  users.is_staff,  users.is_active
FROM users
WHERE users.id
  IN (
    SELECT U0.following_id
    FROM friendship U0
    WHERE U0.follower_id = 3
  )
```

```python
following_users_by_login_user = (
    FriendShip.objects.select_related("follower")
    .filter(follower=self.request.user)
    .values_list("following")
)
User.objects.filter(id__in=following_users_by_login_user)
```

```SQL
SELECT users.id,  users.password,  users.last_login,  users.is_superuser,  users.username,  users.email,  users.slug,  users.is_staff,  users.is_active
FROM users
WHERE users.id
  IN (
    SELECT U0.following_id
    FROM friendship U0
    WHERE U0.follower_id = 7
  )
```

## FollowerListView

```python
get_object()
```

```SQL
SELECT users.id, users.password, users.last_login, users.is_superuser, users.username, users.email, users.slug, users.is_staff, users.is_active
FROM users
WHERE users.slug = 'tester3'
LIMIT 21
```

```python
followers = FriendShip.objects.filter(following=self.object).values_list(
    "follower"
)
User.objects.filter(id__in=followers)
```

```SQL
SELECT users.id, users.password, users.last_login, users.is_superuser, users.username, users.email, users.slug, users.is_staff, users.is_active
FROM users
WHERE users.id IN (
  SELECT U0.follower_id
  FROM friendship U0
  WHERE U0.following_id = 3
)
```

```python
following_users_by_login_user = FriendShip.objects.filter(
    follower=self.request.user
).values_list("following")
User.objects.filter(id__in=following_users_by_login_user)
```

```SQL
SELECT users.id, users.password, users.last_login, users.is_superuser, users.username, users.email, users.slug, users.is_staff, users.is_active
FROM users
WHERE users.id IN (
  SELECT U0.following_id
  FROM friendship U0
  WHERE U0.follower_id = 3
)
```

# Home

## HomeView

```python
User.objects.annotate(
    tweet_num=Count("tweets", distinct=True),
    following_num=Count("followers", distinct=True),
    follower_num=Count("following_users", distinct=True),
).get(username=self.request.username)
```

```SQL
SELECT users.id,  users.password,  users.last_login,  users.is_superuser,  users.username,  users.email,  users.slug,  users.is_staff,  users.is_active,
       COUNT(DISTINCT tweets.id) AS tweet_num,
       COUNT(DISTINCT friendship.id) AS following_num,
       COUNT(DISTINCT T4.id) AS follower_num
FROM users
LEFT OUTER JOIN tweets ON (users.id = tweets.user_id)
LEFT OUTER JOIN friendship ON (users.id = friendship.follower_id)
LEFT OUTER JOIN friendship T4 ON (users.id = T4.following_id)
WHERE users.username = 'TESTER7'
GROUP BY users.id,  users.password,  users.last_login,  users.is_superuser,  users.username,  users.email,  users.slug,  users.is_staff,  users.is_active
LIMIT 21
```

```python
Tweet.objects.select_related("user").prefetch_related("likes").all()
```

```SQL
SELECT tweets.id,  tweets.content,  tweets.user_id,  tweets.created_at,  users.id,  users.password,  users.last_login,  users.is_superuser,  users.username,  users.email,  users.slug,  users.is_staff,  users.is_active
FROM tweets
INNER JOIN users ON (tweets.user_id = users.id)
ORDER BY tweets.created_at DESC
```

```python
{% for tweet in tweet_list %}
```

```SQL
SELECT like.id,  like.tweet_id,  like.user_id
FROM like
WHERE like.tweet_id
IN (13,  12,  10,  8,  6,  5,  4,  2,  1)
```

```python
Like.objects.filter(user=self.request.user).values_list(
    "tweet", flat=True
)
{% if tweet.id in liked_list %}
```

```SQL
SELECT like.tweet_id
FROM like
WHERE like.user_id = 7
```

# Tweets

## TweetCreateView

```SQL
INSERT INTO tweets (content,  user_id,  created_at) SELECT 'content',  7,  'yyyy-mm-dd hh:mm:ss.000000' RETURNING tweets.id
```

## TweetEditView

```python
# django/views/generic/detail.py in get_object(53)
obj = queryset.get()
```

```SQL
SELECT tweets.id,  tweets.content,  tweets.user_id,  tweets.created_at,  users.id,  users.password,  users.last_login,  users.is_superuser,  users.username,  users.email,  users.slug,  users.is_staff,  users.is_active
FROM tweets
INNER JOIN users ON (tweets.user_id = users.id)
WHERE tweets.id = 14
LIMIT 21
```

```python
# backend_sample_demo/tweets/views.py in test_func(62)
tweet = self.get_object()
# django/views/generic/detail.py in get_object(53)
obj = queryset.get()
```

```SQL
SELECT tweets.id,  tweets.content,  tweets.user_id,  tweets.created_at,  users.id,  users.password,  users.last_login,  users.is_superuser,  users.username,  users.email,  users.slug,  users.is_staff,  users.is_active
FROM tweets
INNER JOIN users ON (tweets.user_id = users.id)
WHERE tweets.id = 14
LIMIT 21
```

```python
# django/forms/models.py in save(548)
self.instance.save()
```

```SQL
UPDATE tweets SET content = 'content!',  user_id = 7,  created_at = 'yyyy-mm-dd hh:mm:ss.000000' WHERE tweets.id = 14
```

## TweetDeleteView

```python
# django/views/generic/detail.py in get(108)
self.object = self.get_object()
# django/views/generic/detail.py in get_object(53)
obj = queryset.get()
```

```SQL
SELECT tweets.id,  tweets.content,  tweets.user_id,  tweets.created_at,  users.id,  users.password,  users.last_login,  users.is_superuser,  users.username,  users.email,  users.slug,  users.is_staff,  users.is_active
FROM tweets
INNER JOIN users ON (tweets.user_id = users.id)
WHERE tweets.id = 14
LIMIT 21
```

```python
# backend_sample_demo/tweets/views.py in test_func(83)
tweet = self.get_object()
# django/views/generic/detail.py in get_object(53)
obj = queryset.get()
```

```SQL
SELECT tweets.id,  tweets.content,  tweets.user_id,  tweets.created_at,  users.id,  users.password,  users.last_login,  users.is_superuser,  users.username,  users.email,  users.slug,  users.is_staff,  users.is_active
FROM tweets
INNER JOIN users ON (tweets.user_id = users.id)
WHERE tweets.id = 14
LIMIT 21
```

```python
# django/views/generic/edit.py in form_valid(284)
self.object.delete()
```

```SQL
BEGIN

DELETE FROM like WHERE like.tweet_id IN (14)

DELETE FROM tweets WHERE tweets.id IN (14)
```

## LikeView

```SQL
SELECT tweets.id,  tweets.content,  tweets.user_id,  tweets.created_at
FROM tweets
WHERE tweets.id = 12
LIMIT 21

SELECT like.id,  like.tweet_id,  like.user_id
FROM like
WHERE (like.tweet_id = 12 AND like.user_id = 7)
LIMIT 21

BEGIN

INSERT INTO like (tweet_id,  user_id) SELECT 12,  7 RETURNING like.id

SELECT COUNT(*) AS __count FROM like WHERE like.tweet_id = 12
```

## UnLikeView

```SQL
SELECT tweets.id,  tweets.content,  tweets.user_id,  tweets.created_at
FROM tweets
WHERE tweets.id = 8
LIMIT 21

SELECT like.id,  like.tweet_id,  like.user_id
FROM like
WHERE (like.tweet_id = 8 AND like.user_id = 7)

BEGIN

DELETE FROM like WHERE (like.tweet_id = 8 AND like.user_id = 7)

SELECT COUNT(*) AS __count FROM like WHERE like.tweet_id = 8
```

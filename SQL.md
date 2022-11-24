## SQL

#### session チェック

```python
# django/contrib/sessions/backends/db.py in _get_session_from_db(32)
self.model.objects.get(
  session_key=self.session_key, expire_date__gt=timezone.now()
)
```

```SQL
SELECT django_session.session_key,
       django_session.session_data,
       django_session.expire_date
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
SELECT users.id,
       users.password,
       users.last_login,
       users.is_superuser,
       users.username,
       users.email,
       users.slug,
       users.is_staff,
       users.is_active
FROM users
WHERE users.id = 1
LIMIT 21
```

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
SELECT users.id,
       users.password,
       users.last_login,
       users.is_superuser,
       users.username,
       users.email,
       users.slug,
       users.is_staff,
       users.is_active,
       COUNT(DISTINCT tweets.id) AS tweet_num,
       COUNT(DISTINCT friendship.id) AS following_num,
       COUNT(DISTINCT T4.id) AS follower_num,
       profile.id,
       profile.user_id,
       profile.bio
FROM users
LEFT OUTER JOIN tweets
  ON (users.id = tweets.user_id) LEFT OUTER JOIN friendship ON (users.id = friendship.follower_id)
LEFT OUTER JOIN friendship T4
  ON (users.id = T4.following_id)
LEFT OUTER JOIN profile
  ON (users.id = profile.user_id)
WHERE (users.slug = 'tester' AND users.slug = 'tester')
GROUP BY users.id,
         users.password,
         users.last_login,
         users.is_superuser,
         users.username,
         users.email,
         users.slug,
         users.is_staff,
         users.is_active,
         profile.id,
         profile.user_id,
         profile.bio
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
WHERE (friendship.follower_id = 3
  AND friendship.following_id = 1)
LIMIT 1
```

```python
self.object.tweets.prefetch_related("likes").all()
{% for tweet in tweets %}
```

```SQL
SELECT tweets.id,
       tweets.content,
       tweets.user_id,
       tweets.created_at
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
SELECT like.id,
       like.tweet_id,
       like.user_id
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

## FollowView

```python
get_object_or_404(User, slug=kwargs["slug"])
```

```SQL
SELECT users.id,
       users.password,
       users.last_login,
       users.is_superuser,
       users.username,
       users.email,
       users.slug,
       users.is_staff,
       users.is_active
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

```python

```

```SQL

```

## FollowingListView

```python
get_object()
```

```SQL
SELECT users.id,
       users.password,
       users.last_login,
       users.is_superuser,
       users.username,
       users.email,
       users.slug,
       users.is_staff,
       users.is_active
FROM users
WHERE users.slug = 'tester'
LIMIT 21
```

```python
following_users = FriendShip.objects.filter(follower=self.object).values_list(
    "following"
)
User.objects.filter(id__in=following_users)
```

```SQL
SELECT users.id,
       users.password,
       users.last_login,
       users.is_superuser,
       users.username,
       users.email,
       users.slug,
       users.is_staff,
       users.is_active
FROM users
WHERE users.id IN (
  SELECT U0.following_id
  FROM friendship U0
  WHERE U0.follower_id = 1
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
SELECT users.id,
       users.password,
       users.last_login,
       users.is_superuser,
       users.username,
       users.email,
       users.slug,
       users.is_staff,
       users.is_active
FROM users
WHERE users.id IN (
  SELECT U0.following_id
  FROM friendship U0
  WHERE U0.follower_id = 3
)
```

## FollowerListView

```python
get_object()
```

```SQL
SELECT users.id,
       users.password,
       users.last_login,
       users.is_superuser,
       users.username,
       users.email,
       users.slug,
       users.is_staff,
       users.is_active
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
SELECT users.id,
       users.password,
       users.last_login,
       users.is_superuser,
       users.username,
       users.email,
       users.slug,
       users.is_staff,
       users.is_active
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
SELECT users.id,
       users.password,
       users.last_login,
       users.is_superuser,
       users.username,
       users.email,
       users.slug,
       users.is_staff,
       users.is_active
FROM users
WHERE users.id IN (
  SELECT U0.following_id
  FROM friendship U0
  WHERE U0.follower_id = 3
)
```

```python

```

```SQL

```

```python

```

```SQL

```
